import pytest
from peewee import SqliteDatabase
from epic.models.models import User, Client, Contract, Event, Role
from unittest.mock import patch, MagicMock
from epic.cli.auth_cli import user_info

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
        signed=True,
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
def mock_create_permissions(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("epic.cli.initialize_cli.create_permissions", mock)
    return mock


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
def mock_is_auth_admin(monkeypatch):
    def mock_return():
        return User.get_by_id(2)

    monkeypatch.setattr("epic.cli.auth_cli.User.is_auth", mock_return)


@pytest.fixture
def mock_is_auth_sales(monkeypatch):
    def mock_return():
        return User.get_by_id(3)

    monkeypatch.setattr("epic.cli.auth_cli.User.is_auth", mock_return)


@pytest.fixture
def mock_is_auth_support(monkeypatch):
    def mock_return():
        return User.get_by_id(4)

    monkeypatch.setattr("epic.cli.auth_cli.User.is_auth", mock_return)


@pytest.fixture
def roles_data():
    return ["admin", "sales", "support"]
