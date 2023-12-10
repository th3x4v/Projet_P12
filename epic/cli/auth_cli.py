import typer
from epic.models.models import User, db, Client, Contract, Event, Role
import jwt
import os

app = typer.Typer()

SESSION_FILE = "jwt_token.txt"

SECRET_KEY = "your-secret-key"  # to eplace with a secure secret key


@app.command("login")
def login():
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
    with open("jwt_token.txt", "w") as token_file:
        token_file.write(token)


# Global dictionary to store user information
user_info = {}


def authenticated_command(func):
    def wrapper():
        if not db.table_exists(User._meta.table_name):
            typer.echo("Initialization required. Please run 'initialize' command.")
        else:
            try:
                with open("jwt_token.txt", "r") as token_file:
                    token = token_file.read().strip()
                    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                    # Check if the token is not expired and has necessary information
                    if "user_id" in decoded_token and "role" in decoded_token:
                        # Store user information in the global dictionary
                        user_info["user_id"] = decoded_token["user_id"]
                        user_info["role"] = decoded_token["role"]
                        return func()
                    else:
                        typer.echo("Invalid token. Please reauthenticate.")
            except (
                FileNotFoundError,
                jwt.ExpiredSignatureError,
                jwt.InvalidTokenError,
            ):
                typer.echo("Authentication required. Please run 'login' command.")

    return wrapper


if __name__ == "__main__":
    app()
