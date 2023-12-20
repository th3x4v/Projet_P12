import pytest
import unittest
from unittest.mock import ANY, MagicMock, patch
from epic.models.models import User, Role  # Import the Role class
from epic.cli.user_cli import app
from typer.testing import CliRunner





def test_create_user(mock_authenticated_command, mocker, mock_user_info):
    """
    Test the create_user function
    """
    # Mock the User.create method
    mocker.patch("epic.cli.user_cli.User.create", return_value=MagicMock(name="test_user"))

    # Mock the Role.get method
    mocker.patch("epic.cli.user_cli.Role.get", return_value=MagicMock(name="test_role"))

    runner = CliRunner()
    result = runner.invoke(app, ["create"], input="test_name\ntest_email\ntest_password\ntest_role\n")

    assert result.exit_code == 0
    assert "User test_user created successfully." in result.output

