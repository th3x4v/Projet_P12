from models.models import create_tables
from cli.user_cli import app as user_app
from cli.event_cli import app as event_app
from cli.contract_cli import app as contract_app
from cli.client_cli import app as client_app
from cli.auth_cli import app as auth_app


import typer

app = typer.Typer()

app.add_typer(user_app, name="user")
app.add_typer(event_app, name="event")
app.add_typer(contract_app, name="contract")
app.add_typer(client_app, name="client")
app.add_typer(auth_app, name="auth")

if __name__ == "__main__":
    """
    Module to launch the application
    """
    create_tables()
    app()
