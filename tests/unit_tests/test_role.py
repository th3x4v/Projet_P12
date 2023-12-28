from unittest.mock import Mock
from typer.testing import CliRunner
import pytest
from epic.cli.role_cli import app

runner = CliRunner()


def test_create_role(
    mock_is_auth_admin,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(side_effect=["Test Role", "Test Description"])
    monkeypatch.setattr("epic.cli.role_cli.get_input", mock_get_input)

    result = runner.invoke(app, ["create"])

    assert result.exit_code == 0
    assert "Role Test Role created successfully." in result.output


def test_delete_role(
    mock_is_auth_admin,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(side_effect=[1])
    monkeypatch.setattr("epic.cli.role_cli.get_input", mock_get_input)

    result = runner.invoke(app, ["delete"])

    assert result.exit_code == 0
    assert "Role deleted successfully." in result.output


def test_list_role(
    mock_is_auth_admin,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    assert "Role ID" in result.output
