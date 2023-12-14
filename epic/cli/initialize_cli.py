import typer
from epic.models.models import Event, Contract, User, Client, Role, db
import peewee

app = typer.Typer()


def create_tables():
    """
    Create the database tables for the application.

    This function connects to the database, creates the tables if they do not already exist,
    and initializes the roles table with the default roles.
    """
    db.connect()
    # Create tables if they don't already exist
    db.create_tables([User, Client, Contract, Event, Role], safe=True)


def initialize_roles():
    """
    Initializes the roles table with the default roles.

    This function creates the default roles (admin, sales, and support) if they do not already exist.
    """
    roles_data = ["admin", "sales", "support", "super_admin"]

    for role_name in roles_data:
        try:
            Role.create(name=role_name)
        except peewee.IntegrityError:
            # Role already exists, ignore the error
            pass


@app.command("initialize")
def initialize():
    """
    Initialize the database
    """
    create_tables()
    initialize_roles()
    User.create_superuser("admin", "admin@epic.com", "password")
    typer.echo(f"Project initialized successfully.")
