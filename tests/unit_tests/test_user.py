import pytest
import unittest
from unittest.mock import ANY, MagicMock, patch
from epic.models.models import User, Role  # Import the Role class
from epic.cli.user_cli import app
from typer.testing import CliRunner
import os


def test_create_user(monkeypatch, mock_user_info, setup_database):
    """
    Test the create_user function
    """
    os.environ["TESTING"] = "True"
    inputs = ["John Doe", "john.doe@example.com", "password", "admin"]
    monkeypatch.setattr(
        "epic.cli.user_cli.get_input", lambda _, __, hide_input=False: inputs.pop(0)
    )

    runner = CliRunner()
    result = runner.invoke(app, ["create"])

    assert result.exit_code == 0
    assert "User test_user created successfully." in result.output
    del os.environ["TESTING"]
