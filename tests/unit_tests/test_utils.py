# test_utils.py
import pytest
from epic.utils import get_input, validate_input
from typer.testing import CliRunner
from epic.utils import display_list
import unittest
from unittest.mock import patch, call
from rich.console import Console
from rich.table import Table

runner = CliRunner()


def test_get_input(monkeypatch):
    # Mock the typer.prompt function to return 'John Doe'
    monkeypatch.setattr("typer.prompt", lambda _: "John Doe")

    # Call the get_input function
    result_str = get_input("Enter your name: ", str)

    # Check the result
    assert result_str == "John Doe"

    monkeypatch.setattr("typer.prompt", lambda _: "john.doe@email.com")
    result_email = get_input("Enter your email: ", "email")
    # Check the result
    assert result_email == "john.doe@email.com"


def test_validate_input(mock_roles_data, monkeypatch):
    # Mock the roles_data variable
    monkeypatch.setattr("epic.utils.roles_data", mock_roles_data)

    # Call the validate_input function with different types of input
    assert validate_input("John Doe", str) == "John Doe"
    assert validate_input("42", int) == 42
    assert validate_input("3.14", float) == 3.14
    assert validate_input("True", "status") == True
    assert validate_input("False", "status") == False
    assert validate_input("john.doe@example.com", "email") == "john.doe@example.com"
    assert validate_input("1234567890", "phone") == 1234567890
    assert validate_input("admin", "role_name") == "admin"

    # Test invalid input
    with pytest.raises(ValueError):
        validate_input("invalid", "email")
    with pytest.raises(ValueError):
        validate_input("invalid", "phone")
    with pytest.raises(ValueError):
        validate_input("invalid", "role_name")
