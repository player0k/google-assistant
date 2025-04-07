import os
import json
import time
import requests
from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

CREDENTIALS_PATH = os.path.expanduser('~/.config/google-oauthlib-tool/credentials.json')
DEVICE_MODEL_ID = 'your_device_model_id'
NODE_RED_URL = 'http://localhost:1880/assistant'

def process_event(event):
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print("Начало разговора")
    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        if event.args and 'text' in event.args:
            print("Распознанная речь:", event.args['text'])
            try:
                requests.post(NODE_RED_URL, json={'command': event.args['text']})
                print("Команда отправлена в Node-RED")
            except Exception as e:
                print(f"Ошибка отправки в Node-RED: {e}")
    elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
        print("Разговор завершён")

def start_assistant():
    # Проверка существования файла учетных данных
    if not os.path.exists(CREDENTIALS_PATH):
        raise Exception("Файл учетных данных не найден. Выполните аутентификацию.")

    # Чтение и проверка JSON
    try:
        with open(CREDENTIALS_PATH, 'r') as f:
            creds_data = json.load(f)
    except json.JSONDecodeError:
        raise Exception("Неверный формат файла учетных данных")

    # Создание учетных данных с обработкой отсутствующих полей
    credentials = Credentials(
        token=creds_data.get('token'),
        refresh_token=creds_data.get('refresh_token'),
        token_uri=creds_data.get('token_uri'),
        client_id=creds_data.get('client_id'),
        client_secret=creds_data.get('client_secret'),
        scopes=creds_data.get('scopes')
    )

    # Обновление токена при необходимости
    if credentials and credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
            # Сохраняем обновленные учетные данные
            with open(CREDENTIALS_PATH, 'w') as f:
                f.write(credentials.to_json())
        except Exception as e:
            print(f"Ошибка обновления токена: {e}")

    last_check = time.time()
    with Assistant(credentials, device_model_id=DEVICE_MODEL_ID) as assistant:
        for event in assistant.start():
            current_time = time.time()
            if current_time - last_check > 60:
                last_check = current_time
            process_event(event)

if __name__ == '__main__':
    try:
        start_assistant()
    except Exception as e:
        print(f"Фатальная ошибка: {e}")
        print("Проверьте файл учетных данных и настройки аутентификации")
