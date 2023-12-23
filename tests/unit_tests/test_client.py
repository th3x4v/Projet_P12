from unittest import mock
import pytest
from typer.testing import CliRunner
from epic.cli.client_cli import app
from functools import wraps
from epic.models.models import Role, User, Client
import bcrypt
from unittest.mock import Mock

runner = CliRunner()


def test_create_client(
    mock_get_auth,
    mock_user_info_sales,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(
        side_effect=["Test Client", "client1@example.com", 1234567890, "Test Company"]
    )
    monkeypatch.setattr(
        "epic.cli.client_cli.get_input", mock_get_input
    )  # Replace with actual module name

    monkeypatch.setattr(
        "epic.cli.client_cli.method_allowed", {"client_cli.create_client": ["sales"]}
    )
    monkeypatch.setattr("epic.cli.client_cli.user_info", mock_user_info_sales)
    result = runner.invoke(app, ["create"])

    assert result.exit_code == 0
    assert "Client Test Client created successfully." in result.output
