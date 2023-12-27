from unittest import mock
import pytest
from typer.testing import CliRunner
from epic.cli.contract_cli import app
from epic.models.models import Role, User, Client, Contract
import bcrypt
from unittest.mock import Mock

runner = CliRunner()


def test_create_contract(
    mock_is_auth_sales,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(
        side_effect=[
            1,
            "Test2 Contract",
            True,
            5000.0,
            2000.0,
        ]
    )
    monkeypatch.setattr("epic.cli.contract_cli.get_input", mock_get_input)

    result = runner.invoke(app, ["create"])

    assert result.exit_code == 0
    assert "Contract Test2 Contract created successfully." in result.output


def test_update_contract(
    mock_is_auth_sales,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(
        side_effect=[
            1,
            "Contract Updated",
            True,
            5000.0,
            2000.0,
        ]
    )
    monkeypatch.setattr("epic.cli.contract_cli.get_input", mock_get_input)

    result = runner.invoke(app, ["update"])

    assert result.exit_code == 0
    assert "Contract Updated updated successfully." in result.output


def test_delete_contract(
    mock_is_auth_sales,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(side_effect=[1])
    monkeypatch.setattr("epic.cli.contract_cli.get_input", mock_get_input)

    result = runner.invoke(app, ["delete"])

    assert result.exit_code == 0
    assert "Contract deleted successfully." in result.output
    # Check that the contract was deleted from the database
    with pytest.raises(Contract.DoesNotExist):
        Contract.get_by_id(1)


def test_list_contract(
    mock_is_auth_sales,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    assert "Contract ID" in result.output


def test_read_contract(
    mock_is_auth_sales,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    result = runner.invoke(app, ["read"])

    assert result.exit_code == 0
    assert "Contract ID:" in result.output
