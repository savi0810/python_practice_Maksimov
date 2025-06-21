COMMAND_NAME = "get_tpl"
OUTPUT_FORMAT = "{key}: {value}"
DATE_FORMATS = ["%d.%m.%Y", "%Y-%m-%d"]
PHONE_PATTERN = r"^\+7 \d{3} \d{3} \d{2} \d{2}$"
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

INVALID_COMMAND = "Неверная команда. Используйте: get_tpl"
SUCCESSFUL_INIT_DB = "База данных успешно инициализирована!"
NO_TEMPLATE_FOUND = "Шаблон не найден"
RESULT_FORMAT = """{{
  {fields}
}}"""
