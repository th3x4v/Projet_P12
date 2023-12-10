import typer
from epic.models.models import Client, User
from peewee import DoesNotExist
from epic.cli.auth_cli import authenticated_command
from epic.cli.user_cli import method_allowed
from epic.cli.auth_cli import user_info
import inspect
import os

# Get the filename of the module
filename, _ = os.path.splitext(os.path.basename(os.path.abspath(__file__)))


app = typer.Typer()


@app.command("create")
@authenticated_command
def create_client():
    """Create a new client

    This function prompts the user to enter the client's name, email, phone, company, and sales contact ID, and then creates a new client with the provided information.

    Args:
        None

    Returns:
        None

    Raises:
        DoesNotExist: If the sales contact ID provided does not exist

    Example:
        To create a new client with the name "John Doe", email "<EMAIL>", phone "1234567890", company "ABC Corp", and sales contact ID "1", you can run the following command:
        $ python app.py client create
        Enter client name: John Doe
        Enter client email: <EMAIL>
        Enter client phone: 1234567890
        Enter client company: ABC Corp
        Enter sales contact ID: 1
        Client John Doe created successfully.
    """
    function_name = inspect.currentframe().f_code.co_name
    if user_info["role"] in method_allowed[filename + "." + function_name]:
        name = typer.prompt("Enter client name:")
        email = typer.prompt("Enter client email:")
        phone = typer.prompt("Enter client phone:")
        company = typer.prompt("Enter client company:")
        sales_contact_id = typer.prompt("Enter sales contact ID:")
        try:
            sales_contact = User.get(User.id == int(sales_contact_id))
            client = Client.create(
                name=name,
                email=email,
                phone=phone,
                company=company,
                sales_contact=sales_contact,
            )
            typer.echo(f"Client {client.name} created successfully.")
        except DoesNotExist:
            typer.echo("Sales contact does not exist.")
    else:
        print("User not allowed")


@app.command("delete-client")
@authenticated_command
def delete_client(client_id: int):
    try:
        client = Client.get(Client.id == client_id)
        client.delete_instance()
        typer.echo(f"Client {client.name} deleted successfully.")
    except DoesNotExist:
        typer.echo(f"Client with ID {client_id} does not exist.")


@app.command("update-client")
@authenticated_command
def update_client(
    client_id: int,
    name: str,
    email: str,
    phone: str,
    company: str,
    sales_contact_id: int,
):
    try:
        client = Client.get(Client.id == client_id)
        sales_contact = User.get(User.id == sales_contact_id)

        client.name = name
        client.email = email
        client.phone = phone
        client.company = company
        client.sales_contact = sales_contact

        client.save()
        typer.echo(f"Client {client.name} updated successfully.")
    except DoesNotExist:
        typer.echo(f"Client with ID {client_id} or Sales contact does not exist.")


if __name__ == "__main__":
    app()
