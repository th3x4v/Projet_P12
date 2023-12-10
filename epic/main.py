from epic.cli.user_cli import app as user_app
from epic.cli.event_cli import app as event_app
from epic.cli.contract_cli import app as contract_app
from epic.cli.client_cli import app as client_app
from epic.cli.auth_cli import app as auth_app
from epic.cli.initialize_cli import app as init_app
import typer


def main_function():
    """
    Main function to launch the application
    """
    app = typer.Typer()

    app.add_typer(init_app, name="init")
    app.add_typer(user_app, name="user")
    app.add_typer(event_app, name="event")
    app.add_typer(contract_app, name="contract")
    app.add_typer(client_app, name="client")
    app.add_typer(auth_app, name="auth")

    app()


if __name__ == "__main__":
    main_function()
