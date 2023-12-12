import pytest
from peewee import SqliteDatabase, Model
from epic.models.models import User, Client, Contract, Event, Role
from epic.cli.initialize_cli import initialize_roles

# Créer une instance de base de données en mémoire pour les tests
test_db = SqliteDatabase(":memory:")

MODELS = [User, Client, Contract, Event, Role]


class TestModel(Model):
    class Meta:
        database = test_db


@pytest.fixture
def setup_database():
    # Bind model classes to test db. Since we have a complete list of
    # all models, we do not need to recursively bind dependencies.
    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables(MODELS)

    yield

    # Not strictly necessary since SQLite in-memory databases disappear when the connection is closed,
    # but a good practice to close the connection anyway.
    test_db.close()


@pytest.fixture
def user():
    user = User.create(
        name="John Doe", email="johndoe@example.com", password="password123"
    )
    return user


@pytest.fixture
def client():
    client = Client.create(
        name="Acme Corporation",
        email="info@acme.com",
        phone="+1234567890",
        company="Acme Corporation",
    )
    return client


@pytest.fixture
def contract(client):
    contract = Contract.create(
        contract_name="Website Development Contract",
        client=client,
        total_amount=1000.00,
    )
    return contract


@pytest.fixture
def event(contract):
    event = Event.create(
        name="Website Launch Event",
        contract=contract,
        support_contact=None,
        date_start="2023-10-04",
        date_end="2023-10-04",
        location="Acme Corporation HQ",
        attendees=50,
        notes="Please arrange catering and refreshments.",
    )
    return event
