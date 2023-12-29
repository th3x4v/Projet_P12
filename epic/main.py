from epic.cli.user_cli import app as user_app
from epic.cli.event_cli import app as event_app
from epic.cli.contract_cli import app as contract_app
from epic.cli.client_cli import app as client_app
from epic.cli.auth_cli import app as auth_app
from epic.cli.initialize_cli import app as init_app
from epic.cli.role_cli import app as role_app
import typer
import logging
from epic.models.models import User
from epic.init_sentry import sentry_sdk


def main_function():
    """
    Main function to launch the application
    """
    try:
        # result = 1 / 0

        app = typer.Typer()

        app.add_typer(init_app, name="init")
        app.add_typer(user_app, name="user")
        app.add_typer(event_app, name="event")
        app.add_typer(contract_app, name="contract")
        app.add_typer(client_app, name="client")
        app.add_typer(auth_app, name="auth")
        app.add_typer(role_app, name="role")

        app()

        logger = logging.getLogger("peewee")
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

    except Exception as e:
        sentry_sdk.capture_exception(e)


if __name__ == "__main__":
    main_function()
