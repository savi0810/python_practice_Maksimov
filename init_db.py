from form_manager import FormManager
from constants import SUCCESSFUL_INIT_DB

def init_database(db_path='forms_db.json'):
    manager = FormManager(db_path)
    
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
    
    manager.db.truncate()
    for template in templates:
        manager.add_template(template)
    
    print(SUCCESSFUL_INIT_DB)

if __name__ == "__main__":
    init_database()
