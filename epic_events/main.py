from models.models import create_tables
from cli_controllers.user_cli import user_app
from cli_controllers.event_cli import event_app
from cli_controllers.contract_cli import contract_app
from cli_controllers.client_cli import client_app


import typer

app = typer.Typer()

app.add_typer(user_app, name="user")
app.add_typer(event_app, name="event")
app.add_typer(contract_app, name="contract")
app.add_typer(client_app, name="client")

if __name__ == "__main__":
    """
    Module to launch the application
    """
    create_tables()
    app()
