#!/bin/bash

# Убедитесь, что mpg123 установлен
if ! command -v mpg123 &> /dev/null; then
    echo "mpg123 не найден. Пожалуйста, установите его перед запуском этого скрипта."
    exit 1
fi

# Файл с радиостанциями в формате JSON
INPUT_FILE="stations.json"
# Файл для сохранения рабочих станций
OUTPUT_FILE="working_stations.json"

# Проверяем существование входного файла
if [ ! -f "$INPUT_FILE" ]; then
    echo "Файл $INPUT_FILE не найден."
    exit 1
fi

# Функция для проверки работоспособности ссылки
check_stream() {
    local url="$1"
    local log_file=$(mktemp)
    
    # Запускаем mpg123 с таймаутом и сохраняем вывод
    timeout 15 mpg123 --timeout 10 -q "$url" > "$log_file" 2>&1
    local exit_code=$?
    
    rm "$log_file"
    
    # Коды выхода:
    # 0 - успешное воспроизведение
    # 124 - таймаут команды timeout
    # 1 - ошибка mpg123
    if [[ $exit_code -eq 0 || $exit_code -eq 124 ]]; then
        return 0
    else
        return 1
    fi
}

# Создаем временный файл для хранения рабочих станций
temp_file=$(mktemp)

# Читаем JSON и проверяем каждую станцию (исправлен разделитель)
jq -r 'to_entries[] | "\(.key)\t\(.value)"' "$INPUT_FILE" | while IFS=$'\t' read -r name url; do
    echo "Проверяем станцию: $name"
    if check_stream "$url"; then
        echo "Станция $name работает."
        # Добавляем рабочую станцию во временный файл
        echo "{\"$name\": \"$url\"}," >> "$temp_file"
    else
        echo "Станция $name не работает."
    fi
done

# Формируем окончательный JSON с рабочими станциями
echo "{" > "$OUTPUT_FILE"
# Удаляем последнюю запятую и добавляем закрывающую скобку
sed '$ s/,$//' "$temp_file" >> "$OUTPUT_FILE"
echo "}" >> "$OUTPUT_FILE"

# Удаляем временный файл
rm "$temp_file"

echo "Проверка завершена. Рабочие станции сохранены в $OUTPUT_FILE."
