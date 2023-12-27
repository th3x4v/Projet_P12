import pytest
from peewee import SqliteDatabase
from epic.models.models import User, Client, Contract, Event, Role
from unittest.mock import patch, MagicMock
from epic.cli.auth_cli import user_info
from epic.cli.auth_cli import authenticated_command
from functools import wraps

MODELS = [User, Client, Contract, Event, Role]


@pytest.fixture(scope="function")
def database():
    test_db = SqliteDatabase(":memory:")
    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    yield test_db
    test_db.close()


@pytest.fixture(scope="function")
def setup_database():
    test_db = SqliteDatabase(":memory:")
    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables(MODELS)
    # Create roles
    for role_name in ["admin", "sales", "support"]:
        Role.create(name=role_name)
    user = User.create(
        name="Henry",
        email="henry@example.com",
        password="password",
        role=Role.get(Role.name == "admin"),
    )
    user_admin = User.create(
        name="Admin User",
        email="admin@example.com",
        password="salespassword",
        role=Role.get(Role.name == "admin"),
    )
    user_sales = User.create(
        name="Sales User",
        email="sales@example.com",
        password="salespassword",
        role=Role.get(Role.name == "sales"),
    )

    user_support = User.create(
        name="Support User",
        email="support@example.com",
        password="supportpassword",
        role=Role.get(Role.name == "support"),
    )
    client = Client.create(
        name="Test Client",
        email="test@example.com",
        phone=1234567890,
        company="Test Company",
        sales_contact=user_sales,
    )
    contract = Contract.create(
        name="Test Contract",
        client=client,
        total_amount=1000,
        due_amount=0.0,
        signed=False,
    )
    event = Event.create(
        name="Test Event",
        contract=contract,
        support_contact=user_support,
        date_start="2021-01-01",
        date_end="2021-01-01",
        location="Sample Location",
        attendees=10,
        notes="Sample Notes",
    )
    yield
    test_db.close()


@pytest.fixture
def temp_token_file(tmp_path):
    token_file = tmp_path / "temp_token.txt"
    token_file.write_text("test_token_content")
    return token_file


@pytest.fixture
def mock_has_perm(monkeypatch):
    def mock_return(self, permission: str):
        return True

    monkeypatch.setattr("epic.cli.auth_cli.User.has_perm", mock_return)


@pytest.fixture
def mock_is_auth(monkeypatch):
    def mock_return():
        return User.get_by_id(2)

    monkeypatch.setattr(
        "epic.cli.auth_cli.User.is_auth", mock_return
    )  # replace 'your_module' with the actual module name


@pytest.fixture
def mock_user_info_admin(monkeypatch):
    # This fixture will mock the user_info dictionary
    return {"user_id": 1, "role": "admin"}


@pytest.fixture
def mock_user_info_sales(monkeypatch):
    return {"user_id": 1, "role": "sales"}


@pytest.fixture
def mock_user_info_support(monkeypatch):
    return {"user_id": 1, "role": "support"}


@pytest.fixture
def roles_data():
    return ["admin", "sales", "support"]


@pytest.fixture
def mock_get_auth(monkeypatch):
    # Mock the get_auth function to always return True
    monkeypatch.setattr("epic.cli.auth_cli.get_auth", lambda: True)


# # list of module and class for each model
# all_models = [
#     {"module": user, "class": "User"},
#     # {"module": contract, "class": "Contract"},
# ]


# def _link_class_to_db(db) -> list:
#     """link the database meta attribut to classes and return the classes list from models"""
#     models = []
#     for item in all_models:
#         model = getattr(item.get("module"), item.get("class"))
#         model._meta.database = db
#         models.append(model)
#     return models


# @pytest.fixture(scope="session")
# def in_memory_db():
#     """Return an in memory SQLite db for the session"""

#     db = SqliteDatabase(":memory:")
#     db.connect()
#     all_models = _link_class_to_db(db)
#     db.create_tables(all_models)

#     yield db
#     db.close()


# @pytest.fixture
# def mock_get_input(monkeypatch):
#     """A fixture for mocking get_input."""

#     def mock_input(*args, **kwargs):
#         if args[0] == "Enter name:":
#             return "Test User"
#         elif args[0] == "Enter email:":
#             return "test@example.com"
#         elif args[0] == "Enter password:":
#             return "password"
#         elif args[0] == "Enter role name:":
#             return "admin"
#         elif args[0] == "Enter phone number:":
#             return "1234567890"
#         elif args[0] == "Enter company name:":
#             return "Test Company"
#         elif args[0] == "Enter contract name:":
#             return "Test Contract"
#         elif args[0] == "Enter total amount:":
#             return "1000"
#         elif args[0] == "Enter due amount:":
#             return "0.0"
#         elif args[0] == "Enter signed (True/False):":
#             return "False"
#         elif args[0] == "Enter event name:":
#             return "Test Event"
#         elif args[0] == "Enter start date (YYYY-MM-DD):":
#             return "2021-01-01"
#         elif args[0] == "Enter end date (YYYY-MM-DD):":
#             return "2021-01-01"
#         elif args[0] == "Enter location:":
#             return "Sample Location"
#         elif args[0] == "Enter number of attendees:":
#             return "10"
#         elif args[0] == "Enter notes:":
#             return "Sample Notes"

#     monkeypatch.setattr("epic.cli.user_cli.get_input", mock_input)
