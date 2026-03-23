# Telegram AssemblyAI Bot MVP

Production-like MVP Telegram-бот на Python 3.11+, который принимает `voice`, `audio`, `document` (с аудио), отправляет запись в AssemblyAI (pre-recorded transcription) и возвращает DOCX с транскрипцией.

## Возможности

- `python-telegram-bot 21.x` + long polling
- Поддержка `/start`, `/help`
- Поддержка `voice`, `audio`, `document` (только аудио)
- Проверка размера файла до скачивания
- Временная уникальная папка на каждый запрос
- Загрузка локального файла в AssemblyAI
- Создание transcript job с `speech_models`, `language_detection=true`, `speaker_labels=true`
- Polling результата
- Формирование DOCX через `python-docx`
- Очистка временных файлов после обработки
- Логирование, типизация, модульная структура

## Структура

```text
app/
  main.py
  config.py
  logger.py
  bot/
    handlers.py
    messages.py
  services/
    telegram_files.py
    assemblyai_client.py
    transcript_formatter.py
    docx_builder.py
  utils/
    files.py
    mime.py
tests/
run.py
```

## Запуск локально

1. Создать venv:

```bash
python -m venv .venv
```

2. Активировать venv:

```bash
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate
```

3. Установить зависимости:

```bash
pip install -r requirements.txt
```

4. Заполнить `.env` на основе `.env.example`:

```bash
cp .env.example .env
# затем впишите TELEGRAM_BOT_TOKEN и ASSEMBLYAI_API_KEY
```

5. Запустить бота:

```bash
python -m app.main
# или
python run.py
```

## Тесты

```bash
pytest
```

Покрыты базовые проверки:
- логика определения аудио-документов (`mime`)
- форматирование payload транскрипции
- генерация DOCX с ключевыми разделами
