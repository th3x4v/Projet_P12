from unittest.mock import Mock
from typer.testing import CliRunner
import pytest
from epic.cli.event_cli import app

runner = CliRunner()


def test_create_event(
    mock_is_auth_sales,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(
        side_effect=[
            1,
            "Test Event",
            "2023-05-01 12:00",
            "2023-05-01 18:00",
            "Sample Location",
            50,
            "Sample Notes",
        ]
    )
    monkeypatch.setattr("epic.cli.event_cli.get_input", mock_get_input)

    result = runner.invoke(app, ["create"])

    assert result.exit_code == 0
    assert "Event Test Event created successfully." in result.output


def test_update_event_support(
    mock_is_auth_support,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(
        side_effect=[
            1,
            "Event Updated",
            4,
            "2023-05-01 12:00",
            "2023-05-01 18:00",
            "Sample Location",
            50,
            "Sample Notes",
        ]
    )
    monkeypatch.setattr("epic.cli.event_cli.get_input", mock_get_input)

    result = runner.invoke(app, ["update"])

    assert result.exit_code == 0
    assert "Event Event Updated updated successfully." in result.output


def test_delete_event(
    mock_is_auth_support,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(side_effect=[1])
    monkeypatch.setattr("epic.cli.event_cli.get_input", mock_get_input)

    result = runner.invoke(app, ["delete"])

    assert result.exit_code == 0
    assert "Event deleted successfully." in result.output


def test_list_event(
    mock_is_auth_support,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    assert "Event ID" in result.output


def test_read_event(
    mock_is_auth_support,
    mock_has_perm,
    setup_database,
    monkeypatch,
):
    result = runner.invoke(app, ["read"])

    assert result.exit_code == 0
    assert "Event ID:" in result.output
