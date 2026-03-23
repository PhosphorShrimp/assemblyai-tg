"""User-facing message templates for Telegram bot responses."""

WELCOME = (
    "Привет! Отправьте voice/audio или document с аудиофайлом, "
    "и я верну DOCX с транскрипцией через AssemblyAI."
)

HELP = (
    "Поддерживаются типы: voice, audio и document (только аудио).\n"
    "Ограничение размера файла задаётся в MAX_FILE_SIZE_MB."
)

UNSUPPORTED = (
    "Неподдерживаемый тип сообщения. Отправьте voice, audio "
    "или document с аудиофайлом."
)

TOO_LARGE = "Файл слишком большой (лимит: {max_mb} MB). Отправьте файл поменьше."
DOWNLOAD_ERROR = "Не удалось скачать файл. Попробуйте ещё раз."
UPLOAD_ERROR = "Ошибка загрузки в AssemblyAI. Попробуйте позже."
POLLING_ERROR = "Ошибка получения результата транскрипции. Попробуйте позже."
DOCX_ERROR = "Ошибка сборки DOCX-файла. Попробуйте позже."
GENERIC_ERROR = "Что-то пошло не так. Попробуйте ещё раз позже."

FILE_RECEIVED = "Файл получен, начинаю обработку."
AUDIO_SENT = "Аудио отправлено на распознавание."
TRANSCRIPT_READY = "Транскрипция готова, формирую DOCX."
