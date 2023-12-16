import typer
from email.utils import parseaddr
from rich.console import Console
from rich.table import Table
from epic.cli.initialize_cli import roles_data
import re


# Function to get user input with Typer prompt
def get_input(prompt: str, hide_input: bool = False) -> str:
    return typer.prompt(prompt, hide_input=hide_input)


# Function to validate email address
def validate_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


# Function to validate name (string)
def validate_name(name: str) -> bool:
    return bool(name and name.strip())  # Name is valid if it's not empty


# Function to validate role name
def validate_role_name(role_name: str) -> bool:
    return (
        role_name.lower() in roles_data
    )  # Role name is valid if it's one of the allowed roles


# Function to get and validate user input for different field types
def get_validated_input(field_type: str, prompt: str, hide_input: bool = False) -> str:
    while True:
        value = get_input(prompt, hide_input)
        if field_type == "email":
            if validate_email(value):
                return value
            else:
                typer.echo("Invalid email address. Please try again.")
        elif field_type == "name":
            if validate_name(value):
                return value
            else:
                typer.echo("Invalid name. Please enter a valid name.")
        elif field_type == "role_name":
            if validate_role_name(value):
                return value
            else:
                typer.echo(
                    f"Invalid role name. Please choose from: {', '.join(roles_data)}"
                )
        else:  # Password or other string
            return value


def display_list(title: str, items: list):
    "Display a list of records"

    # Voir https://rich.readthedocs.io/en/stable/protocol.html?highlight=__rich__#console-customization

    table = Table(
        title=title,
        padding=(0, 1),
        header_style="blue bold",
        title_style="purple bold",
        title_justify="center",
        width=50,
    )

    try:
        headers = items[0].keys()

    except IndexError:
        headers = ["Liste vide"]

    for title in headers:
        table.add_column(title, style="cyan", justify="center")

    for item in items:
        # rich render only str
        values = [str(value) for value in item.values()]
        table.add_row(*values)

    console = Console()
    print("")
    console.print(table)
