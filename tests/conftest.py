import pytest
from peewee import SqliteDatabase
from epic.models.models import User, Client, Contract, Event, Role
from unittest.mock import patch, MagicMock
from epic.cli.auth_cli import user_info
from epic.cli.auth_cli import authenticated_command

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
    yield
    test_db.close()


@pytest.fixture
def temp_token_file(tmp_path):
    token_file = tmp_path / "temp_token.txt"
    token_file.write_text("test_token_content")
    return token_file


@pytest.fixture
def mock_user_info(monkeypatch):
    # This fixture will mock the user_info dictionary
    return {"user_id": 1, "role": "admin"}


@pytest.fixture
def mock_authenticated_command(monkeypatch):
    """
    This fixture will mock the authenticated_command decorator
    """

    def mock_decorator(func):
        def wrapper(*args, **kwargs):
            # Simulate a successful authentication by setting user_info
            return func(*args, **kwargs)

        return wrapper

    monkeypatch.setattr("epic.cli.auth_cli.authenticated_command", mock_decorator)


@pytest.fixture
def mock_get_input(monkeypatch):
    """A fixture for mocking get_input."""

    def mock_input(*args, **kwargs):
        if args[0] == "Enter name:":
            return "Test User"
        elif args[0] == "Enter email:":
            return "test@example.com"
        elif args[0] == "Enter password:":
            return "password"
        elif args[0] == "Enter role name:":
            return "admin"

    monkeypatch.setattr("epic.cli.user_cli.get_input", mock_input)


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
