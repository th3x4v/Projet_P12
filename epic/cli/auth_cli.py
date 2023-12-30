import typer
from epic.models.models import User
from epic.utils import get_input
import os

user_auth = None


def check_auth(ctx: typer.Context):
    """
    This function is used to check if the user is authenticated and has the permission to execute the given command.

    Args:
        ctx (typer.Context): The context object that contains information about the current command, including its name and parent.

    Returns:
        None

    """
    command = ctx.invoked_subcommand
    print(ctx.invoked_subcommand)
    if command in ["login", "logout", "list"]:
        return
    global user_auth
    user_auth = User.is_auth()
    if user_auth is None:
        exit()

    permission_to_check = f"{ctx.info_name}-{command}"
    check_permissions(user_auth, permission_to_check)


def check_permissions(user: User, permission: str):
    """Check if the user have permission. Exit the app if not"""
    if not user.has_perm(permission):
        print(f"You don't have the permission ({permission}) to do this action")
        exit()


app = typer.Typer(callback=check_auth)

SESSION_FILE = "jwt_token.txt"

SECRET_KEY = "your-secret-key"


@app.command("login")
def login():
    """
    Logs in the user with the given email and password.

    Parameters:
    email (str): The email of the user.
    password (str): The password of the user.

    Returns:
    str: The JWT token if the login is successful, None otherwise.

    """
    email = get_input("Enter email", "email")
    password = get_input("Enter password", str, hide_input=True)
    token = authenticate(email, password)
    if token:
        store_token(token)
        typer.echo(f"Login successful. JWT Token: {token}")
    else:
        typer.echo("Login failed.")


@app.command("logout")
def logout():
    """
    Removes the JWT token file from the system and displays a message indicating that the user has been logged out.

    Returns:
        None

    """
    try:
        os.remove(SESSION_FILE)
        typer.echo("Logout successful.")
    except FileNotFoundError:
        typer.echo("No active session. Please run 'login' command.")


def authenticate(email: str, password: str):
    user = User.authenticate(email, password)
    if user:
        return user.generate_jwt_token()
    else:
        typer.echo("Invalid credentials. Authentication failed.")
        return None


def store_token(token):
    with open(SESSION_FILE, "w") as token_file:
        token_file.write(token)


if __name__ == "__main__":
    app()
