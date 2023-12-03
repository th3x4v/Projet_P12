from models.models import User, Role, create_tables
import typer
from peewee import DoesNotExist


user_app = typer.Typer()
app = user_app


@app.command("create-user")
def create_user(name: str, email: str, password: str, role_name: str):
    try:
        role = Role.get(Role.name == role_name)
    except DoesNotExist:
        typer.echo(f"Role '{role_name}' does not exist.")
        return

    user = User.create(name=name, email=email, password=password, role=role)
    typer.echo(f"User {user.name} created successfully.")


@app.command("list-users")
def list_users():
    users = User.select()
    for user in users:
        typer.echo(
            f"User ID: {user.id}, Name: {user.name}, Email: {user.email}, Role: {user.role.name}"
        )


@app.command("delete-user")
def delete_user(user_id: int):
    try:
        user = User.get(User.id == user_id)
        user.delete_instance()
        typer.echo(f"User {user.name} deleted successfully.")
    except DoesNotExist:
        typer.echo(f"User with ID {user_id} does not exist.")


@app.command("update-user")
def update_user(user_id: int, name: str, email: str, password: str, role_name: str):
    try:
        user = User.get(User.id == user_id)
        role = Role.get(Role.name == role_name)
        user.name = name
        user.email = email
        user.password = password
        user.role = role
        user.save()
        typer.echo(f"User {user.name} updated successfully.")
    except DoesNotExist:
        typer.echo(f"User with ID {user_id} does not exist.")
    except DoesNotExist:
        typer.echo(f"Role '{role_name}' does not exist.")


@app.command("create-role")
def create_role(name: str):
    role = Role.create(name=name)
    typer.echo(f"Role {role.name} created successfully.")


@app.command("list-roles")
def list_roles():
    roles = Role.select()
    for role in roles:
        typer.echo(f"Role ID: {role.id}, Name: {role.name}")


@app.command("delete-role")
def delete_role(role_id: int):
    try:
        role = Role.get(Role.id == role_id)
        role.delete_instance()
        typer.echo(f"Role {role.name} deleted successfully.")
    except DoesNotExist:
        typer.echo(f"Role with ID {role_id} does not exist.")


@app.command("update-role")
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
    user_app()
