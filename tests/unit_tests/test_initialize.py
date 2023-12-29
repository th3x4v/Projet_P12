import pytest
from epic.cli.initialize_cli import (
    create_tables,
    app,
    initialize_roles,
    create_permissions,
)
from epic.models.models import (
    User,
    Client,
    Contract,
    Event,
    Role,
    RolePermission,
    Permission,
)
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


def test_initialize_permission(database, monkeypatch):
    monkeypatch.setattr("epic.cli.initialize_cli.db", database)
    create_tables()
    initialize_roles()
    create_permissions()

    assert Role.select().count() == 4
    assert Permission.select().count() == 26
    assert RolePermission.select().count() == 79
