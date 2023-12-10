import typer
from epic.models.models import create_tables, User

app = typer.Typer()


@app.command("initialize")
def initialize():
    """
    Initialize the database
    """
    create_tables()
    User.create_superuser("admin", "admin@epic.com", "password")
    typer.echo(f"Project initialzed successfully.")
