import pytest
from form_manager import validate_date, validate_phone, validate_email, get_field_type, FormManager
from init_db import init_database
from constants import (
    DATE_FORMATS, PHONE_PATTERN, EMAIL_PATTERN,
    NO_TEMPLATE_FOUND, OUTPUT_FORMAT, RESULT_FORMAT, 
    SUCCESSFUL_INIT_DB, INVALID_COMMAND
)
import tinydb
import os
from unittest.mock import patch
import sys

# Фикстуры для тестов
@pytest.fixture(scope="function")
def test_db(tmp_path):
    """Фикстура для временной базы данных"""
    db_path = tmp_path / "test_forms_db.json"
    return str(db_path)

@pytest.fixture
def form_manager(test_db):
    """Фикстура менеджера форм с чистой базой"""
    manager = FormManager(test_db)
    manager.db.truncate()
    yield manager
    # Явно закрываем соединение с базой после теста
    manager.db.close()

@pytest.fixture
def populated_manager(form_manager):
    """Фикстура с заполненной базой шаблонов"""
    templates = [
        {"name": "UserForm", "username": "text", "email": "email"},
        {"name": "OrderForm", "product": "text", "order_date": "date", "phone": "phone"}
    ]
    for template in templates:
        form_manager.add_template(template)
    yield form_manager
    # Явно закрываем соединение с базой после теста
    form_manager.db.close()

# Тесты валидаторов
class TestValidators:
    @pytest.mark.parametrize("date_str, valid", [
        ("31.12.2022", True),
        ("2022-12-31", True),
        ("31/12/2022", False),
        ("2022.31.12", False),
        ("invalid", False)
    ])
    def test_validate_date(self, date_str, valid):
        assert validate_date(date_str) == valid

    @pytest.mark.parametrize("phone, valid", [
        ("+79001234567", True),
        ("+7 900 123 45 67", True),
        ("+7-900-123-45-67", False),
        ("89001234567", False),
        ("invalid", False)
    ])
    def test_validate_phone(self, phone, valid):
        assert validate_phone(phone) == valid

    @pytest.mark.parametrize("email, valid", [
        ("test@example.com", True),
        ("user.name+tag@domain.co", True),
        ("invalid@", False),
        ("@domain.com", False),
        ("no_at_symbol.com", False)
    ])
    def test_validate_email(self, email, valid):
        assert validate_email(email) == valid

    @pytest.mark.parametrize("value, expected_type", [
        ("2023-10-05", "date"),
        ("+79161234567", "phone"),
        ("user@domain.org", "email"),
        ("plain text", "text"),
        ("", "text")
    ])
    def test_get_field_type(self, value, expected_type):
        assert get_field_type(value) == expected_type

# Тесты FormManager
class TestFormManager:
    def test_add_template(self, form_manager):
        template = {"name": "TestForm", "field1": "text"}
        form_manager.add_template(template)
        assert form_manager.db.count(tinydb.Query().name == "TestForm") == 1

    def test_add_template_missing_name(self, form_manager):
        with pytest.raises(ValueError):
            form_manager.add_template({"field": "text"})

    def test_find_template_exact_match(self, populated_manager):
        fields = {"username": "John", "email": "john@example.com"}
        assert populated_manager.find_template(fields) == "UserForm"

    def test_find_template_extra_fields(self, populated_manager):
        fields = {
            "username": "Alice", 
            "email": "alice@mail.com",
            "extra_field": "value"
        }
        assert populated_manager.find_template(fields) == "UserForm"

    def test_find_template_partial_match(self, populated_manager):
        fields = {"username": "Bob"}
        assert populated_manager.find_template(fields) == NO_TEMPLATE_FOUND

    def test_find_template_no_match(self, populated_manager):
        fields = {"unknown_field": "value"}
        assert populated_manager.find_template(fields) == NO_TEMPLATE_FOUND

    def test_process_query_with_match(self, populated_manager):
        query = {
            "username": "test_user",
            "email": "user@test.com"
        }
        assert populated_manager.process_query(query) == "UserForm"

    def test_process_query_no_match(self, populated_manager):
        query = {
            "unknown_field": "2023-10-05",
            "another_field": "+79161234567"
        }
        result = populated_manager.process_query(query)
        expected_output = RESULT_FORMAT.format(fields=",\n  ".join([
            OUTPUT_FORMAT.format(key="unknown_field", value="date"),
            OUTPUT_FORMAT.format(key="another_field", value="phone")
        ]))
        assert result == expected_output

# Тесты инициализации БД
def test_init_database(test_db, capsys):
    # Убедимся, что файла нет
    if os.path.exists(test_db):
        os.remove(test_db)
        
    # Инициализируем базу
    init_database(test_db)
    
    # Проверяем заполнение
    manager = FormManager(test_db)
    try:
        assert len(manager.db.all()) == 5
        assert any(t["name"] == "Registration_user" for t in manager.db.all())
    finally:
        # Всегда закрываем соединение после использования
        manager.db.close()
    
    # Проверяем вывод
    captured = capsys.readouterr()
    assert SUCCESSFUL_INIT_DB in captured.out

# Тесты main.py
class TestMain:
    @pytest.mark.parametrize("command, args, expected", [
        # Корректный запрос с совпадением
        (
            "get_tpl", 
            ["--username=John", "--email=john@example.com"],
            "UserForm\n"
        ),
        # Корректный запрос без совпадения
        (
            "get_tpl",
            ["--unknown=2023-10-05"],
            RESULT_FORMAT.format(
                fields=OUTPUT_FORMAT.format(key="unknown", value="date")
            ) + "\n"
        ),
        # Неверная команда
        (
            "wrong_command",
            [],
            INVALID_COMMAND + "\n"
        )
    ])
    def test_main(self, monkeypatch, capsys, command, args, expected):
        # Мокируем FormManager и его метод process_query
        with patch('main.FormManager') as MockFormManager:
            mock_manager = MockFormManager.return_value
            mock_manager.process_query.return_value = expected.strip()
            
            # Подменяем аргументы командной строки
            monkeypatch.setattr("sys.argv", ["main.py", command] + args)
            
            # Запускаем main
            from main import main
            main()
            
            # Проверяем вывод
            captured = capsys.readouterr()
            assert captured.out == expected