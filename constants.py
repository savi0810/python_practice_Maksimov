# Константы приложения
COMMAND_NAME = "get_tpl"
OUTPUT_FORMAT = "{key}: {value}"
DATE_FORMATS = ["%d.%m.%Y", "%Y-%m-%d"]
PHONE_PATTERN = r"^\+7\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}$"
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

# Сообщения
INVALID_COMMAND = "Неверная команда. Используйте: get_tpl"
SUCCESSFUL_INIT_DB = "Базаданных успешно инициализирована!"
NO_TEMPLATE_FOUND = "Шаблон не найден"
RESULT_FORMAT = """{{
  {fields}
}}"""