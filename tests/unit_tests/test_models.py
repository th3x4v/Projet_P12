import pytest
from epic.models.models import User, Role
import bcrypt
import jwt
from epic.models.models import Client
import time


def test_create_superuser(setup_database):
    """
    Creates a superuser with the given name, email, and password.

    Args:
        name (str): The name of the user.
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        User: The created user.

    Raises:
        ValueError: If the password is not secure enough.
    """
    role = Role.create(name="super_admin")
    User.create_superuser(
        name="test_admin", email="test_admin@example.com", password="test_password"
    )
    user = User.get(User.email == "test_admin@example.com")
    assert user.name == "test_admin"
    assert user.email == "test_admin@example.com"
    assert bcrypt.checkpw(
        "test_password".encode("utf-8"), user.password.encode("utf-8")
    )


def test_authenticate(setup_database):
    """
    Tests the authenticate method of the User class.
    """
    role = Role.create(name="super_admin")
    User.create_superuser(
        name="test_admin", email="test_admin@example.com", password="test_password"
    )
    user = User.get(User.email == "test_admin@example.com")

    # Tests authentication with correct password
    authenticated_user = User.authenticate(
        email="test_admin@example.com", password="test_password"
    )
    assert authenticated_user == user

    # Tests authentication with incorrect password
    authenticated_user = User.authenticate(
        email="test_admin@example.com", password="wrong_password"
    )
    assert authenticated_user is None

    # Tests authentication with incorrect email
    authenticated_user = User.authenticate(
        email="wrong_email@example.com", password="test_password"
    )
    assert authenticated_user is None


# TestGenerateJwtToken:
def test_valid_jwt_token():
    """
    Tests that a valid JWT token is generated with the correct user ID and role.

    Returns:
        None

    Raises:
        AssertionError: If the JWT token is not valid.
    """
    user = User()
    user.id = 1
    user.role = Role(name="admin")
    token = user.generate_jwt_token()
    decoded_token = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
    assert decoded_token["user_id"] == 1
    assert decoded_token["role"] == "admin"


def test_return_type():
    """
    Tests that the return type of the generate_jwt_token method is a string.

    Returns:
        None

    Raises:
        AssertionError: If the return type is not a string.
    """
    user = User()
    user.id = 1
    user.role = Role(name="admin")
    token = user.generate_jwt_token()
    assert isinstance(token, str)


def test_save_updates_date(setup_database):
    """
    Tests that the save method of the Client model updates the date_updated field.

    Args:
        setup_database (func): A function that sets up the test database.

    Returns:
        None

    Raises:
        AssertionError: If the date_updated field is not updated.
    """
    role = Role.create(name="sales")
    user = User.create(
        name="Henry",
        email="henry@example.com",
        password="password",
        role=Role.get(Role.name == "sales"),
    )
    # Wait for a second to ensure the user is created
    time.sleep(1)

    client = Client.create(
        name="John",
        email="john@example.com",
        phone="1234567890",
        company="ABC Corp",
        sales_contact=user,
    )
    original_date_updated = client.date_updated

    # Wait for a second to ensure the date_updated will be different
    time.sleep(1)

    client.save()
    assert client.date_updated is not None
    assert client.date_updated > original_date_updated
