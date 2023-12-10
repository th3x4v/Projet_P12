from models.models import User, Role, create_tables
import typer
from peewee import DoesNotExist
from cli.auth_cli import authenticated_command
import os
from cli.auth_cli import user_info
import inspect


app = typer.Typer()

method_allowed = {
    "user_cli.create_user": ["admin"],
    "user_cli.list_users": ["admin"],
    "user_cli.delete_user": ["admin"],
    "user_cli.update_user": ["admin"],
    "user_cli.create_role": ["admin"],
    "user_cli.list_roles": ["admin"],
    "user_cli.delete_role": ["admin"],
    "user_cli.update_role": ["admin"],
    "event_cli.create_event": ["admin", "sales", "support"],
    "event_cli.list_events": ["admin", "sales", "support"],
    "event_cli.delete_event": ["admin", "sales", "support"],
    "event_cli.update_event": ["admin", "sales", "support"],
    "client_cli.create_client": ["admin", "sales"],
    "client_cli.list_clients": ["admin", "sales"],
    "client_cli.delete_client": ["admin", "sales"],
    "client_cli.update_client": ["admin", "sales"],
    "contract_cli.create_contract": ["admin", "sales"],
    "contract_cli.list_contracts": ["admin", "sales"],
    "contract_cli.delete_contract": ["admin", "sales"],
    "contract_cli.update_contract": ["admin", "sales"],
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
        $ python app.py user create
        Enter name: John Doe
        Enter email: <EMAIL>
        Enter password: password
        Enter role name: admin
        User John Doe created successfully."""
    # Check permission
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
@authenticated_command
def list_users():
    users = User.select()
    for user in users:
        typer.echo(
            f"User ID: {user.id}, Name: {user.name}, Email: {user.email}, Role: {user.role.name}"
        )


@app.command("delete")
@authenticated_command
def delete_user():
    # Check permission
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
    # Check permission
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
def create_role(name: str):
    role = Role.create(name=name)
    typer.echo(f"Role {role.name} created successfully.")


@app.command("list-roles")
@authenticated_command
def list_roles():
    roles = Role.select()
    for role in roles:
        typer.echo(f"Role ID: {role.id}, Name: {role.name}")


@app.command("delete-role")
@authenticated_command
def delete_role(role_id: int):
    try:
        role = Role.get(Role.id == role_id)
        role.delete_instance()
        typer.echo(f"Role {role.name} deleted successfully.")
    except DoesNotExist:
        typer.echo(f"Role with ID {role_id} does not exist.")


@app.command("update-role")
@authenticated_command
def update_role(role_id: int, name: str):
    try:
        role = Role.get(Role.id == role_id)
        role.name = name
        role.save()
        typer.echo(f"Role {role.name} updated successfully.")
    except DoesNotExist:
        typer.echo(f"Role with ID {role_id} does not exist.")


if __name__ == "__main__":
    create_tables()
    app()
