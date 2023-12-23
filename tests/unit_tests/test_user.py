from unittest import mock
import pytest
from typer.testing import CliRunner
from epic.cli.user_cli import app
from functools import wraps
from epic.models.models import Role, User
import bcrypt
from unittest.mock import Mock

runner = CliRunner()


def test_create_user(
    mock_get_auth,
    mock_user_info_admin,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(
        side_effect=["Test1 User", "test1@example.com", "password123", "admin"]
    )
    monkeypatch.setattr(
        "epic.cli.user_cli.get_input", mock_get_input
    )  # Replace with actual module name

    monkeypatch.setattr(
        "epic.cli.user_cli.method_allowed", {"user_cli.create_user": ["admin"]}
    )
    monkeypatch.setattr("epic.cli.user_cli.user_info", mock_user_info_admin)
    result = runner.invoke(app, ["create"])

    assert result.exit_code == 0
    assert "User Test1 User created successfully." in result.output


role = "admin"


def test_update_user(
    mock_get_auth,
    mock_user_info_admin,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(side_effect=[2, "Test2 User", "admin@example.com", "admin"])
    monkeypatch.setattr(
        "epic.cli.user_cli.get_input", mock_get_input
    )  # Replace with actual module name

    monkeypatch.setattr(
        "epic.cli.user_cli.method_allowed", {"user_cli.update_user": ["admin"]}
    )
    monkeypatch.setattr("epic.cli.user_cli.user_info", mock_user_info_admin)
    result = runner.invoke(app, ["update"])

    assert result.exit_code == 0
    assert "User Test2 User updated successfully." in result.output


def test_update_password(
    mock_get_auth,
    mock_user_info_admin,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(side_effect=[2, "passwordtest"])
    monkeypatch.setattr(
        "epic.cli.user_cli.get_input", mock_get_input
    )  # Replace with actual module name

    monkeypatch.setattr(
        "epic.cli.user_cli.method_allowed", {"user_cli.update_password": ["admin"]}
    )
    monkeypatch.setattr("epic.cli.user_cli.user_info", mock_user_info_admin)
    result = runner.invoke(app, ["update-password"])
    user = User.get_by_id(2)

    assert result.exit_code == 0
    assert "Password for user Admin User updated successfully." in result.output
    assert (
        bcrypt.checkpw("passwordtest".encode("utf-8"), user.password.encode("utf-8"))
        is True
    )


def test_delete_user(
    mock_get_auth,
    mock_user_info_admin,
    setup_database,
    monkeypatch,
):
    mock_get_input = Mock(side_effect=[2])
    monkeypatch.setattr(
        "epic.cli.user_cli.get_input", mock_get_input
    )  # Replace with actual module name

    monkeypatch.setattr(
        "epic.cli.user_cli.method_allowed", {"user_cli.delete_user": ["admin"]}
    )
    monkeypatch.setattr("epic.cli.user_cli.user_info", mock_user_info_admin)
    user = User.get_by_id(2)
    result = runner.invoke(app, ["delete"])

    assert result.exit_code == 0
    assert "User deleted successfully." in result.output
    # Check that the user was deleted from the database
    with pytest.raises(User.DoesNotExist):
        User.get_by_id(2)


# @pytest.fixture
# def mock_authenticated_command(monkeypatch):
#     """
#     This fixture will mock the authenticated_command decorator
#     """

#     def mock_decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             return func(*args, **kwargs)

#         return wrapper

#     monkeypatch.setattr("epic.cli.auth_cli.authenticated_command", mock_decorator)


# def test_create_user(
#     mock_get_auth,
#     mock_user_info,
#     mock_get_input,
#     setup_database,
#     monkeypatch,
# ):
#     """
#     Test the create_user function
#     """
#     monkeypatch.setattr(
#         "epic.cli.user_cli.method_allowed", {"user_cli.create_user": ["admin"]}
#     )
#     monkeypatch.setattr("epic.cli.user_cli.user_info", mock_user_info)

#     result = runner.invoke(app, ["create"])

#     assert result.exit_code == 0
#     assert "User Test User created successfully." in result.output
