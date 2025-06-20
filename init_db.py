from form_manager import FormManager
from constants import SUCCESSFUL_INIT_DB

def init_database(db_path='forms_db.json'):
    """
    Инициализирует базу данных с шаблонами форм
    
    Args:
        db_path (str): Путь к файлу базы данных
    """
    manager = FormManager(db_path)
    
    # Шаблоны форм
    templates = [
        {
            "name": "Registration_user",
            "username": "text",
            "email": "email",
            "birth_date": "date"
        },
        {
            "name": "Order_form",
            "customer": "text",
            "order_date": "date",
            "delivery_phone": "phone"
        },
        {
            "name": "Contact_information",
            "full_name": "text",
            "contact_phone": "phone",
            "contact_email": "email"
        },
        {
            "name": "Feedback",
            "message": "text",
            "response_email": "email"
        },
        {
            "name": "Booking",
            "event_date": "date",
            "participants": "text",
            "contact_phone": "phone",
            "special_requests": "text"
        }
    ]
    
    # Очистка и заполнение базы данных
    manager.db.truncate()
    for template in templates:
        manager.add_template(template)
    
    # Закрываем соединение с базой
    manager.close()
    
    print(SUCCESSFUL_INIT_DB)

if __name__ == "__main__":
    init_database()