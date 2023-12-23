from epic.models.models import User, Role
import typer
from peewee import DoesNotExist
from epic.cli.auth_cli import authenticated_command
import os
from epic.cli.auth_cli import user_info
import inspect
import bcrypt
from epic.utils import get_input, display_list
from epic.cli.user_cli import method_allowed


app = typer.Typer()
# Get the filename of the module
filename, _ = os.path.splitext(os.path.basename(os.path.abspath(__file__)))


@app.callback()
def check_auth(ctx: typer.Context):
    print(ctx.invoked_subcommand)
    if ctx.invoked_subcommand in ["login", "logout", "list"]:
        return
    global user_auth
    user_auth = User.is_auth()
    if user_auth is None:
        exit()


@app.command("create")
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
        name = get_input("Enter name:", str)
        role = Role.create(name=name)
        typer.echo(f"Role {role.name} created successfully.")
    else:
        print("User not allowed")


@app.command("list")
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


@app.command("delete")
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
        role_id = get_input("Enter role ID to delete role", int)
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
