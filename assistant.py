import os
import json
import time
from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Путь к файлу с учетными данными OAuth 2.0
CREDENTIALS_PATH = os.path.expanduser('~/.config/google-oauthlib-tool/credentials.json')
# Замените 'your_device_model_id' на ваш реальный идентификатор модели устройства
DEVICE_MODEL_ID = 'your_device_model_id'

def process_event(event):
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print("Начало разговора")
    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        if event.args and 'text' in event.args:
            print("Распознанная речь:", event.args['text'])
    elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
        print("Разговор завершён")

def start_assistant():
    # Загрузка учетных данных
    with open(CREDENTIALS_PATH, 'r') as f:
        credentials = Credentials(token=None, **json.load(f))
    
    # Если токен просрочен и есть refresh token, обновляем его
    if credentials.expired and credentials.refresh_token:
        print("Обновление access token...")
        credentials.refresh(Request())
    
    # Запуск ассистента с device_model_id
    last_check = time.time()
    with Assistant(credentials, device_model_id=DEVICE_MODEL_ID) as assistant:
        for event in assistant.start():
            current_time = time.time()
            if current_time - last_check > 60:
                if credentials.expired and credentials.refresh_token:
                    print("Refreshing token...")
                    credentials.refresh(Request())
                    with open(CREDENTIALS_PATH, 'w') as f:
                        f.write(credentials.to_json())
                last_check = current_time
            process_event(event)


if __name__ == '__main__':
    start_assistant()
