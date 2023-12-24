import typer
from email.utils import parseaddr
from rich.console import Console
from rich.table import Table
from epic.cli.initialize_cli import roles_data
import re
from datetime import datetime


def get_input(prompt: str, input_type, **kwargs):
    """
    Get input using typer.prompt and validate based on input_type.
    """
    while True:
        try:
            user_input = typer.prompt(prompt, **kwargs)
            validated_input = validate_input(user_input, input_type)
            return validated_input
        except ValueError as e:
            typer.echo(f"Invalid input. {e}")


def validate_input(value, input_type):
    """
    Validate input based on input_type.
    """
    if input_type == str:
        return value
    elif input_type == int:
        return int(value)
    elif input_type == float:
        return float(value)
    elif input_type == bool:
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        else:
            raise ValueError("Invalid boolean value. Enter 'True' or 'False'.")
    elif input_type == "email":
        if re.match(r"[^@]+@[^@]+\.[^@]+", value):
            return value
        else:
            raise ValueError("Invalid email address.")
    elif input_type == "phone":
        if re.match(r"\d{10}", value):
            return int(value)
        else:
            raise ValueError("Invalid phone number. Must be a 10-digit integer.")
    elif input_type == "role_name":
        if value.lower() in roles_data:
            return value
    elif input_type == "date":
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date. The format should be 'YYYY-MM-DD'.")
        else:
            raise ValueError(
                "Invalid role name. Choose from 'admin', 'sales', or 'support'."
            )
    else:
        raise ValueError("Invalid input type.")


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
