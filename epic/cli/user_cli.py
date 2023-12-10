from epic.models.models import User, Role
import typer
from peewee import DoesNotExist
from epic.cli.auth_cli import authenticated_command
import os
from epic.cli.auth_cli import user_info
import inspect


app = typer.Typer()

method_allowed = {
    "user_cli.create_user": ["admin", "super_admin"],
    "user_cli.list_users": ["admin", "super_admin"],
    "user_cli.delete_user": ["admin", "super_admin"],
    "user_cli.update_user": ["admin", "super_admin"],
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
}


# Get the filename of the module
filename, _ = os.path.splitext(os.path.basename(os.path.abspath(__file__)))


@app.command("create")
@authenticated_command
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
    function_name = inspect.currentframe().f_code.co_name
    if user_info["role"] in method_allowed[filename + "." + function_name]:
        name = typer.prompt("Enter name:")
        email = typer.prompt("Enter email:")
        password = typer.prompt("Enter password:", hide_input=True)
        role_name = typer.prompt("Enter role name:")
        try:
            role = Role.get(Role.name == role_name)
            user = User.create(name=name, email=email, password=password, role=role)
            typer.echo(f"User {user.name} created successfully.")
        except DoesNotExist:
            typer.echo(f"Role '{role_name}' does not exist.")
    else:
        print(" user not allowed")


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
    for user in users:
        typer.echo(
            f"User ID: {user.id}, Name: {user.name}, Email: {user.email}, Role: {user.role.name}"
        )


@app.command("delete")
@authenticated_command
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

    function_name = inspect.currentframe().f_code.co_name
    if user_info["role"] in method_allowed[filename + "." + function_name]:
        user_id = typer.prompt("Enter user ID:")
        try:
            user = User.get(User.id == user_id)
            user.delete_instance()
            typer.echo(f"User {user.name} deleted successfully.")
        except DoesNotExist:
            typer.echo(f"User with ID '{user_id}' does not exist.")
    else:
        print("User not allowed")


@app.command("update")
@authenticated_command
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

    function_name = inspect.currentframe().f_code.co_name
    if user_info["role"] in method_allowed[filename + "." + function_name]:
        user_id = typer.prompt("Enter user ID to update:")
        try:
            user = User.get(User.id == user_id)
            typer.echo(
                f"User ID: {user.id}, Name: {user.name}, Email: {user.email}, Role: {user.role.name}"
            )
        except DoesNotExist:
            typer.echo(f"User with ID {user_id} does not exist.")

        name = typer.prompt("Enter new name or press 'Enter':", default=user.name)
        email = typer.prompt("Enter new email or press 'Enter':", default=user.email)
        password = typer.prompt(
            "Enter new password or press 'Enter':",
            hide_input=True,
            default=user.password,
        )
        role_name = typer.prompt(
            "Enter new role name or press 'Enter':", default=user.role.name
        )

        try:
            role = Role.get(Role.name == role_name)
            user.name = name
            user.email = email
            user.password = password
            user.role = role
            user.save()
            typer.echo(f"User {user.name} updated successfully.")
        except DoesNotExist:
            typer.echo(f"Role '{role_name}' does not exist.")
    else:
        print("User not allowed")


@app.command("create-role")
@authenticated_command
def create_role():
    """Creates a new role.

    This function prompts the user to enter the name of the role to create, and then creates a new role with the provided name.

    Args:
        name (str): The name of the role to create.

    Returns:
        None

    Raises:
        DoesNotExist: If a role with the same name already exists.

    Example:
        To create a new role with the name "manager", you can run the following command:
        $ python -m epic user create-role
        Enter role name: manager
        Role manager created successfully."""
    function_name = inspect.currentframe().f_code.co_name
    if user_info["role"] in method_allowed[filename + "." + function_name]:
        name = typer.prompt("Enter role name:")
        role = Role.create(name=name)
        typer.echo(f"Role {role.name} created successfully.")
    else:
        print("User not allowed")


@app.command("list-roles")
@authenticated_command
def list_roles():
    """Get a list of all roles in the system.

    Args:
        None

    Returns:
        A list of all roles in the system

    Raises:
        None

    Example:
        To get a list of all roles in the system, you can run the following command:
        $ python -m epic user list-roles
        Role ID: 1, Name: admin
        Role ID: 2, Name: support
        ..."""
    roles = Role.select()
    for role in roles:
        typer.echo(f"Role ID: {role.id}, Name: {role.name}")


@app.command("delete-role")
@authenticated_command
def delete_role():
    """Deletes a role from the system.

    Args:
        role_id (int): The ID of the role to delete.

    Returns:
        None

    Raises:
        DoesNotExist: If the role with the specified ID does not exist.

    Example:
        To delete a role with the ID of 1, you can run the following command:
        $ python -m epic user delete-role 1
        Role with ID 1 deleted successfully."""

    function_name = inspect.currentframe().f_code.co_name
    if user_info["role"] in method_allowed[filename + "." + function_name]:
        role_id = typer.prompt("Enter role ID:")
        try:
            role = Role.get(Role.id == role_id)
            role.delete_instance()
            typer.echo(f"Role {role.name} deleted successfully.")
        except DoesNotExist:
            typer.echo(f"Role with ID {role_id} does not exist.")
    else:
        print("User not allowed")


if __name__ == "__main__":
    pass
