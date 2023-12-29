from epic.models.models import Role
import typer
from peewee import DoesNotExist
from epic.cli.auth_cli import check_auth
from epic.utils import get_input


app = typer.Typer(callback=check_auth)


@app.command("create")
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
    # function_name = inspect.currentframe().f_code.co_name
    # if user_info["role"] in method_allowed[filename + "." + function_name]:
    name = get_input("Enter name", str)
    role = Role.create(name=name)
    typer.echo(f"Role {role.name} created successfully.")
    # else:
    #     print("User not allowed")


@app.command("list")
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

    role_id = get_input("Enter role ID to delete role", int)
    try:
        role = Role.get(Role.id == role_id)
        role.delete_instance()
        typer.echo("Role deleted successfully.")
    except DoesNotExist:
        typer.echo(f"Role with ID {role_id} does not exist.")


if __name__ == "__main__":
    pass
