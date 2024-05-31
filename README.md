# Nova Test Task

Тестовое задание Nova.

## Clone repo

Склонировать репозиторий.

```bash
git clone https://github.com/LMortes/nova_task.git
```

## Виртуальное окружение и зависимости
### Создание виртуального окружения
```bash
python -m venv venv
```
### Активация venv
Windows:
```bash
source venv/Scripts/activate
```

MacOS/Linux:
```bash
source venv/bin/activate
```
### Установка зависимостей
```bash
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```
## Запуск проекта.
Прогоним миграции
```bash
cd nova_task
python manage.py migrate
```
Запустим сервер
```bash
python manage.py runserver
```

## Пример работы API
```bash
POST /api/create-file - получить список курсов валют за конкретную дату.
```
Тело запроса:
```json
{
    "data": "some_text",
    "name": "file_name.txt"
}
```

Тело ответа:
```json
{
    "file_id": "file_id"
}
```
