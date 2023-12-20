import pytest
from typer.testing import CliRunner
from epic.cli.auth_cli import app
import os

runner = CliRunner()


def test_login_success(mocker):
    mocker.patch("epic.cli.auth_cli.authenticate", return_value="test_token")
    mocker.patch("epic.cli.auth_cli.store_token")

    result = runner.invoke(app, ["login"], input="test@example.com\ntest_password\n")
    assert result.exit_code == 0
    assert "Login successful. JWT Token: test_token" in result.output


def test_login_failure(mocker):
    mocker.patch("epic.cli.auth_cli.authenticate", return_value=None)

    result = runner.invoke(app, ["login"], input="test@example.com\ntest_password\n")
    assert result.exit_code == 0
    assert "Login failed." in result.output


def test_logout_success(monkeypatch, temp_token_file):
    # Mock the SESSION_FILE with the path to the temporary token file
    monkeypatch.setattr("epic.cli.auth_cli.SESSION_FILE", str(temp_token_file))

    # Call the logout function, assuming 'app' and 'runner' are previously defined
    result = runner.invoke(app, ["logout"])

    # Verify the temporary file is deleted
    # You can include a print statement to check what files are present in the directory just for debugging purposes
    # Print all files in directory of temp_token_file
    print("Files in temp directory:", os.listdir(temp_token_file.parent))

    # Assertions for the result
    assert result.exit_code == 0, "The exit code should be 0 indicating success"
    assert (
        "Logout successful." in result.output
    ), "The success message should be in the output"
    assert not temp_token_file.is_file(), "The temp token file should be deleted"
