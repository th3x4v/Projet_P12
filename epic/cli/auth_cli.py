import typer
from epic.models.models import User, db
import jwt
import os

user_auth = User()


# def callback():
#     def check_auth(ctx: typer.Context):
#         print(ctx.invoked_subcommand)
#         if ctx.invoked_subcommand in ["login", "logout", "list"]:
#             return
#         global user
#         user = User.is_auth()
#         print("user")
#         print(user.name)
#         if user is None:
#             print("exit")
#             exit()


app = typer.Typer()


@app.callback()
def check_auth(ctx: typer.Context):
    print(ctx.invoked_subcommand)
    if ctx.invoked_subcommand in ["login", "logout", "list"]:
        return

    global user_auth
    user_auth = User.is_auth()
    print("user_auth")
    print(user_auth.name)
    if user_auth is None:
        print("exit")
        exit()


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
    email = typer.prompt("Enter email:")
    password = typer.prompt("Enter password:", hide_input=True)
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


@app.callback()
def check_auth(ctx: typer.Context):
    print(ctx.invoked_subcommand)
    if ctx.invoked_subcommand in ["login", "logout", "list"]:
        return

    global user
    user = User.is_auth()
    print("user")
    print(user.name)
    if user is None:
        print("exit")
        exit()


# Global dictionary to store user information
user_info = {}


def get_auth():
    try:
        with open("jwt_token.txt", "r") as token_file:
            token = token_file.read().strip()
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Check if the token is not expired and has necessary information
            if "user_id" in decoded_token and "role" in decoded_token:
                # Store user information in the global dictionary
                user_info["user_id"] = decoded_token["user_id"]
                user_info["role"] = decoded_token["role"]
                return True
            else:
                typer.echo("Invalid token. Please reauthenticate.")
    except (
        FileNotFoundError,
        jwt.ExpiredSignatureError,
        jwt.InvalidTokenError,
    ):
        typer.echo("Authentication required. Please run 'login' command.")


def authenticated_command(func):
    def wrapper():
        if not db.table_exists(User._meta.table_name):
            typer.echo("Initialization required. Please run 'initialize' command.")
        else:
            if get_auth() == True:
                return func()

    return wrapper


if __name__ == "__main__":
    app()
