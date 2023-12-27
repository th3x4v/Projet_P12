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
    mock_is_auth_sales,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(
        side_effect=["Test Client", "client1@example.com", 1234567890, "Test Company"]
    )
    monkeypatch.setattr("epic.cli.client_cli.get_input", mock_get_input)

    result = runner.invoke(app, ["create"])

    assert result.exit_code == 0
    assert "Client Test Client created successfully." in result.output


# test_client.py


def test_update_client(
    mock_is_auth_sales,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(
        side_effect=[
            1,
            "Updated Client",
            "updatedclient@example.com",
            9876543210,
            "Updated Company",
            3,
        ]
    )
    monkeypatch.setattr("epic.cli.client_cli.get_input", mock_get_input)

    result = runner.invoke(app, ["update"])

    assert result.exit_code == 0
    assert "Client Updated Client updated successfully." in result.output


def test_delete_client(
    mock_is_auth_sales,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(side_effect=[1])
    monkeypatch.setattr("epic.cli.client_cli.get_input", mock_get_input)

    result = runner.invoke(app, ["delete"])

    assert result.exit_code == 0
    assert "Client deleted successfully." in result.output
    # Check that the client was deleted from the database
    with pytest.raises(Client.DoesNotExist):
        Client.get_by_id(1)


def test_list_client(
    mock_is_auth_sales,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    assert "Client ID" in result.output


def test_read_client(
    mock_is_auth_sales,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    result = runner.invoke(app, ["read"])

    assert result.exit_code == 0
    assert "Client ID:" in result.output
