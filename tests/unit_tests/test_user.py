import pytest
import unittest
from unittest.mock import ANY, MagicMock, patch
from epic.models.models import User, Role  # Import the Role class
from epic.cli.user_cli import app
from typer.testing import CliRunner
from epic.cli.auth_cli import authenticated_command


runner = CliRunner()


def test_create_user(
    mock_authenticated_command, mocker, mock_user_info, mock_get_input, setup_database
):
    """
    Test the create_user function
    """

    result = runner.invoke(app, ["create"])

    assert result.exit_code == 0
    assert "User test_user created successfully." in result.output
