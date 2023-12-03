from models.models import create_tables
from epic_events.cli_controllers.user_cli import app as user_app


import typer

app = typer.Typer()

app.add_typer(user_app, name="user")

if __name__ == "__main__":
    """
    Module to launch the application
    """
    create_tables()
    app()
