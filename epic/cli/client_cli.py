import typer
from models.models import Client, User
from peewee import DoesNotExist
from cli.auth_cli import authenticated_command


app = typer.Typer()


@app.command("create-client")
@authenticated_command
def create_client(
    name: str, email: str, phone: str, company: str, sales_contact_id: int
):
    try:
        sales_contact = User.get(User.id == sales_contact_id)
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


@app.command("list-clients")
@authenticated_command
def list_clients():
    clients = Client.select()
    for client in clients:
        typer.echo(
            f"Client ID: {client.id}, Name: {client.name}, Email: {client.email}, Sales Contact ID: {client.sales_contact.id}"
        )


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
