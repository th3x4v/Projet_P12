from epic.models.models import User, Role
import typer
from peewee import DoesNotExist
from epic.cli.auth_cli import check_auth
from epic.utils import get_input, display_list


app = typer.Typer(callback=check_auth)


method_allowed = {
    "user_cli.create_user": ["admin", "super_admin"],
    "user_cli.list_users": ["admin", "super_admin"],
    "user_cli.delete_user": ["admin", "super_admin"],
    "user_cli.update_user": ["admin", "super_admin"],
    "user_cli.update_password": ["admin", "super_admin"],
    "user_cli.create_role": ["super_admin"],
    "user_cli.list_roles": ["super_admin"],
    "user_cli.delete_role": ["super_admin"],
    "user_cli.update_role": ["super_admin"],
    "event_cli.create_event": ["admin", "sales", "support", "super_admin"],
    "event_cli.list_events": ["admin", "sales", "support", "super_admin"],
    "event_cli.delete_event": ["admin", "sales", "support", "super_admin"],
    "event_cli.update_event": ["admin", "sales", "support", "super_admin"],
    "client_cli.create_client": ["admin", "sales", "super_admin"],
    "client_cli.list_clients": ["admin", "sales", "super_admin"],
    "client_cli.delete_client": ["admin", "sales", "super_admin"],
    "client_cli.update_client": ["admin", "sales", "super_admin"],
    "contract_cli.create_contract": ["admin", "sales", "super_admin"],
    "contract_cli.list_contracts": ["admin", "sales", "super_admin"],
    "contract_cli.delete_contract": ["admin", "sales", "super_admin"],
    "contract_cli.update_contract": ["admin", "sales", "super_admin"],
    "contract_cli.my_contracts": ["admin", "sales", "super_admin"],
    "event_cli.my_events": ["admin", "support", "super_admin"],
    "client_cli.my_clients": ["admin", "sales", "super_admin"],
}


@app.command("create")
def create_user():
    """Create a new user

    This function prompts the user to enter their name, email, password, and role name, and then creates a new user with the provided information.

    Args:
        None

    Returns:
        None

    Raises:
        DoesNotExist: If the role name provided does not exist

    Example:
        To create a new user with the name "John Doe", email "<EMAIL>", password "password", and role "admin", you can run the following command:
        $ python -m epic user create
        Enter name: John Doe
        Enter email: <EMAIL>
        Enter password: password
        Enter role name: admin
        User John Doe created successfully."""
    name = get_input("Enter name", str)
    email = get_input("Enter email", "email")
    password = get_input("Enter password", str, hide_input=True)
    role_name = get_input("Enter role name", "role_name")
    try:
        role = Role.get(Role.name == role_name)

        user = User.create(name=name, email=email, password=password, role=role)
        typer.echo(f"User {user.name} created successfully.")
    except DoesNotExist:
        typer.echo(f"Role '{role_name}' does not exist.")


@app.command("list")
def list_users():
    """Get a list of all users in the system

    Args:
    None

    Returns:
    A list of all users in the system

    Raises:
    None

    Example:
    To get a list of all users in the system, you can run the following command:
    $ python -m epic user list
    User ID: 1, Name: John Doe, Email: <EMAIL>, Role: admin
    User ID: 2, Name: Jane Doe, Email: <EMAIL>, Role: user
    ..."""
    users = User.select()
    users_data = [
        {"ID": user.id, "Name": user.name, "Email": user.email, "Role": user.role.name}
        for user in users
    ]
    display_list("Users", users_data)


@app.command("delete")
def delete_user():
    """Deletes a user from the system.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        None

    Raises:
        DoesNotExist: If the user with the specified ID does not exist.

    Example:
        To delete a user with the ID of 1, you can run the following command:
        $ python -m epic user delete
        1
        User John Doe deleted successfully."""

    user_id = get_input("Enter user ID to delete", int)
    try:
        user = User.get(User.id == user_id)
        user.delete_instance()
        typer.echo(f"User {user.name} deleted successfully.")
    except DoesNotExist:
        typer.echo(f"User with ID '{user_id}' does not exist.")


@app.command("update")
def update_user():
    """Updates an existing user.

    This function prompts the user to enter the ID of the user to update, their new name, email, password, and role name, and then updates the user with the provided information.

    Args:
        None

    Returns:
        None

    Raises:
        DoesNotExist: If the user with the specified ID does not exist.

    Example:
        To update a user with the ID of 1 with the name "John Doe", email "<EMAIL>", password "password", and role "admin", you can run the following command:
        $ python -m epic user update
        1
        Enter new name or press 'Enter':
        John Doe
        Enter new email or press 'Enter':
        <EMAIL>
        Enter new password or press 'Enter':
        password
        Enter new role name or press 'Enter':
        admin
        User John Doe updated successfully."""

    user_id = get_input("Enter user ID to update", int)
    try:
        user = User.get(User.id == user_id)
        typer.echo(
            f"User ID: {user.id}, Name: {user.name}, Email: {user.email}, Role: {user.role.name}"
        )
    except DoesNotExist:
        typer.echo(f"User with ID {user_id} does not exist.")
    name = get_input("Enter new name or press 'Enter'", str, default=user.name)
    email = get_input("Enter email", "email", default=user.email)
    role_name = get_input("Enter role name", "role_name", default=user.role.name)
    try:
        role = Role.get(Role.name == role_name)
        user.name = name
        user.email = email
        user.role = role
        user.save()
        typer.echo(f"User {user.name} updated successfully.")
    except DoesNotExist:
        typer.echo(f"Role '{role_name}' does not exist.")


@app.command("password")
def update_password():
    """Updates the password of a user.

    Args:
        user_id (int): The ID of the user to update the password for.

    Returns:
        None

    Raises:
        DoesNotExist: If the user with the specified ID does not exist.

    Example:
        To update the password of a user with the ID of 1, you can run the following command:
        $ python -m epic user update-password
        1
        Enter new password:
        Confirm password:
        Password for user John Doe updated successfully."""
    from epic.cli.auth_cli import user_auth

    user_id = get_input("Enter user ID to update password", int)
    if user_id == int(user_auth.id) or user_auth.role.name in [
        "admin",
        "super_admin",
    ]:
        new_password = get_input("Enter new password", str, hide_input=True)
        try:
            user = User.get(User.id == user_id)
            user.password = new_password
            user.save()
            typer.echo(f"Password for user {user.name} updated successfully.")
        except DoesNotExist:
            typer.echo(f"User with ID {user_id} does not exist.")

    else:
        typer.echo("You do not have permission to update this user password.")


if __name__ == "__main__":
    pass
