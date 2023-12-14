import pytest
from epic.cli.initialize_cli import create_tables, app, initialize_roles
from epic.models.models import User, Client, Contract, Event, Role
from typer.testing import CliRunner


runner = CliRunner()


def test_connects_and_creates_tables(database, monkeypatch):
    monkeypatch.setattr("epic.cli.initialize_cli.db", database)
    create_tables()
    assert User.table_exists() == True
    assert Client.table_exists() == True
    assert Contract.table_exists() == True
    assert Event.table_exists() == True
    assert Role.table_exists() == True


def test_initialize_roles(database, monkeypatch):
    monkeypatch.setattr("epic.cli.initialize_cli.db", database)
    create_tables()
    initialize_roles()
    assert Role.select().count() == 4
    assert Role.select().where(Role.name == "admin").exists() == True
    assert Role.select().where(Role.name == "sales").exists() == True
    assert Role.select().where(Role.name == "support").exists() == True
    assert Role.select().where(Role.name == "super_admin").exists() == True


def test_initialize(database, monkeypatch):
    monkeypatch.setattr("epic.cli.initialize_cli.db", database)
    result = runner.invoke(app)
    print("result")
    print(result.output)
    assert User.select().where(User.name == "admin").exists() == True

    # Check if the success message is printed
    assert "Project initialized successfully." in result.output
