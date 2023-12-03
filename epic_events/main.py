from models.models import create_tables
from cli_controllers.users_cli import app as user_app


import typer

app = typer.Typer()

app.add_typer(user_app, name="user")

if __name__ == "__main__":
    """
    Point d'entrée principal de l'application CLI CRM.

    Ce module intègre les sous-commandes des différents domaines :
    - l'authentification
    - le commercial
    - l'administration
    - le support.
    """
    create_tables()
    app()
