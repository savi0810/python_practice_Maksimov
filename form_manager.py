from tinydb import TinyDB, Query
from datetime import datetime
import re
from constants import DATE_FORMATS, PHONE_PATTERN, EMAIL_PATTERN, OUTPUT_FORMAT, RESULT_FORMAT, NO_TEMPLATE_FOUND

def validate_date(value: str) -> bool:
    for fmt in DATE_FORMATS:
        try:
            datetime.strptime(value, fmt)
            return True
        except ValueError:
            continue
    return False

def validate_phone(value: str) -> bool:
    return bool(re.match(PHONE_PATTERN, value))

def validate_email(value: str) -> bool:
    return bool(re.match(EMAIL_PATTERN, value))

def get_field_type(value: str) -> str:
    """Определяет тип поля на основе значения"""
    if validate_date(value):
        return "date"
    if validate_phone(value):
        return "phone"
    if validate_email(value):
        return "email"
    return "text"

class FormManager:
    def __init__(self, db_path='forms_db.json'):
        self.db = TinyDB(db_path)
    
    def close(self):
        """Закрывает соединение с базой данных"""
        self.db.close()
    
    def add_template(self, template: dict):
        """Добавляет шаблон формы в базу данных"""
        if "name" not in template:
            raise ValueError("Шаблон должен содержать поле 'name'")
        self.db.insert(template)
    
    def find_template(self, fields: dict) -> str:
        """Ищет подходящий шаблон формы"""
        Form = Query()
        
        # Поиск шаблонов, где все поля шаблона присутствуют в запросе
        for template in self.db.all():
            template_fields = {k: v for k, v in template.items() if k != 'name'}
            match = True
            
            for field, field_type in template_fields.items():
                if field not in fields or fields[field] != field_type:
                    match = False
                    break
            
            if match:
                return template['name']
        
        return NO_TEMPLATE_FOUND
    
    def process_query(self, query: dict) -> str:
        """Обрабатывает запрос и возвращает результат"""
        # Определяем типы полей
        field_types = {key: get_field_type(value) for key, value in query.items()}
        
        # Пытаемся найти шаблон
        template_name = self.find_template(field_types)
        
        if template_name != NO_TEMPLATE_FOUND:
            return template_name
        
        # Форматируем результат для не найденных шаблонов
        formatted_fields = ',\n  '.join(
            OUTPUT_FORMAT.format(key=key, value=value) 
            for key, value in field_types.items()
        )
        return RESULT_FORMAT.format(fields=formatted_fields)