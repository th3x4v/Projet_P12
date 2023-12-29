import pytest
from epic.cli.initialize_cli import app
from epic.models.models import User
from typer.testing import CliRunner
import time


runner = CliRunner()


def test_initialize(database, monkeypatch):
    monkeypatch.setattr("epic.cli.initialize_cli.db", database)
    result = runner.invoke(app)
    print("result")
    print(result.output)
    assert User.select().where(User.name == "admin").exists() == True

    # Check if the success message is printed
    assert "Project initialized successfully." in result.output
