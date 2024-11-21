#!/bin/bash

# Проверка наличия необходимых аргументов
if [ $# -lt 3 ]; then
    echo "Использование: $0 <DB_NAME> <DB_USER> <DB_PASSWORD> <SQL_FILE>"
    exit 1
fi

# Получаем аргументы
DB_NAME=$1
DB_USER=$2
DB_PASSWORD=$3
SQL_FILE=$4

# Проверка существования SQL файла
if [ ! -f "$SQL_FILE" ]; then
    echo "SQL файл не найден: $SQL_FILE"
    exit 1
fi

# Установка переменной окружения для пароля
export PGPASSWORD=$DB_PASSWORD

# Выполнение SQL файла
echo "Запуск SQL файла $SQL_FILE на базе данных $DB_NAME..."
psql -U $DB_USER -d $DB_NAME -f $SQL_FILE

# Проверка на успешное выполнение
if [ $? -eq 0 ]; then
    echo "SQL файл успешно выполнен!"
else
    echo "Ошибка при выполнении SQL файла!"
    exit 1
fi
