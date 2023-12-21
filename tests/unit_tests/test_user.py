import pytest
import unittest
from unittest.mock import ANY, MagicMock, patch
from epic.models.models import User, Role  # Import the Role class
from typer.testing import CliRunner
from epic.cli.auth_cli import authenticated_command
from epic.cli.user_cli import app
from functools import wraps

runner = CliRunner()


@pytest.fixture
def mock_authenticated_command(monkeypatch):
    """
    This fixture will mock the authenticated_command decorator
    """

    def mock_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    monkeypatch.setattr("epic.cli.auth_cli.authenticated_command", mock_decorator)


def test_create_user(
    mock_authenticated_command,
    mock_user_info,
    mock_get_input,
    setup_database,
    monkeypatch,
):
    """
    Test the create_user function
    """
    monkeypatch.setattr(
        "epic.cli.user_cli.method_allowed", {"user_cli.create_user": ["admin"]}
    )
    monkeypatch.setattr("epic.cli.user_cli.user_info", mock_user_info)

    result = runner.invoke(app, ["create"])

    assert result.exit_code == 0
    assert "User test_user created successfully." in result.output
