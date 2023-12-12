import pytest
from epic.models.models import User, Role
import bcrypt
import jwt
from epic.models.models import Client
import time


def test_create_superuser(setup_database):
    role = Role.create(name="super_admin")
    User.create_superuser(name="admin", email="admin@example.com", password="password")
    user = User.get(User.email == "admin@example.com")
    assert user.name == "admin"
    assert user.email == "admin@example.com"
    assert bcrypt.checkpw("password".encode("utf-8"), user.password.encode("utf-8"))


def test_authenticate(setup_database):
    """
    Tests the authenticate method of the User class.
    """
    role = Role.create(name="super_admin")
    User.create_superuser(name="admin", email="admin@example.com", password="password")
    user = User.get(User.email == "admin@example.com")

    # Tests authentication with correct password
    authenticated_user = User.authenticate(
        email="admin@example.com", password="password"
    )
    assert authenticated_user == user

    # Tests authentication with incorrect password
    authenticated_user = User.authenticate(
        email="admin@example.com", password="wrong_password"
    )
    assert authenticated_user is None

    # Tests authentication with incorrect email
    authenticated_user = User.authenticate(
        email="wrong_email@example.com", password="password"
    )
    assert authenticated_user is None


def test_authenticate(setup_database):
    role = Role.create(name="super_admin")
    User.create_superuser(name="admin", email="admin@example.com", password="password")
    user = User.get(User.email == "admin@example.com")

    authenticated_user = User.authenticate(
        email="admin@example.com", password="password"
    )
    assert authenticated_user == user

    authenticated_user = User.authenticate(
        email="admin@example.com", password="wrong_password"
    )
    assert authenticated_user is None

    authenticated_user = User.authenticate(
        email="wrong_email@example.com", password="password"
    )
    assert authenticated_user is None


# TestGenerateJwtToken:


# Generates a JWT token with a valid expiration time, user ID, and role.
def test_valid_jwt_token():
    user = User()
    user.id = 1
    user.role = Role(name="admin")
    token = user.generate_jwt_token()
    decoded_token = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
    assert decoded_token["user_id"] == 1
    assert decoded_token["role"] == "admin"


# Returns the generated JWT token as a string.
def test_return_type():
    user = User()
    user.id = 1
    user.role = Role(name="admin")
    token = user.generate_jwt_token()
    assert isinstance(token, str)


# Test update client:


def test_save_updates_date(setup_database):
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
