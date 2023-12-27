import typer
from epic.models.models import Client, User
from peewee import DoesNotExist
from epic.cli.auth_cli import check_auth
from epic.utils import get_input


app = typer.Typer(callback=check_auth)


@app.command("create")
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
    from epic.cli.auth_cli import user_auth

    name = get_input("Enter client name", str)
    email = get_input("Enter client email", "email")
    phone = get_input("Enter client phone", "phone")
    company = get_input("Enter client company:", str)
    try:
        sales_contact = User.get(User.id == user_auth.id)
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


@app.command("list")
def list_clients():
    """Get a list of all clients in the system

    Args:
    None

    Returns:
    A list of all clients in the system

    Raises:
    None

    Example:
    To get a list of all clients in the system, you can run the following command:
    $ python -m epic client list_clients
    Client ID: 1, Name: Acme Corp, Email: <EMAIL>, Phone: <PHONE>, Company: Acme Corp, Sales Contact ID: 1
    Client ID: 2, Name: Globex Corp, Email: <EMAIL>, Phone: <PHONE>, Company: Globex Corp, Sales Contact ID: 2
    ..."""
    clients = Client.select()
    for client in clients:
        typer.echo(
            f"Client ID: {client.id}, Name: {client.name}, Email: {client.email}, Phone: {client.phone}, Company: {client.company}, Sales Contact ID: {client.sales_contact.id}"
        )


@app.command("delete")
def delete_client():
    """Deletes an existing client.

    This function prompts the user to enter the ID of the client to delete, and then deletes the client if the user is the sales contact for the client or if they are an administrator.

    Args:
        client_id (int): The ID of the client to delete.

    Returns:
        None

    Raises:
        DoesNotExist: If the client with the specified ID does not exist.

    Example:
        To delete a client with the ID of 1, you can run the following command:
        $ python -m epic client delete
        1
        Client 1 deleted successfully.
    """
    from epic.cli.auth_cli import user_auth

    client_id = get_input("Enter client ID to delete", int)
    try:
        client = Client.get(Client.id == client_id)
        if client.sales_contact.id == user_auth.id or user_auth.role.name in [
            "admin",
            "super_admin",
        ]:
            client.delete_instance()
            typer.echo(f"Client {client.name} deleted successfully.")
        else:
            typer.echo(f"Client {client.name} does not belong to you.")
    except DoesNotExist:
        typer.echo(f"Client with ID '{client_id}' does not exist.")


@app.command("update")
def update_client():
    """
    Updates an existing client.

    This function prompts the user to enter the ID of the client to update, and then displays information about the client if the user is the sales contact for the client or if they are an administrator. The user can then update the client's information by entering new values for the client's name, email, phone, company, and sales contact.

    Args:
        client_id (int): The ID of the client to update.

    Returns:
        None

    Raises:
        DoesNotExist: If the client with the specified ID does not exist.

    Example:
        To update a client with the ID of 1, you can run the following command:
        $ python -m epic client update
        1
        Client ID: 1, Name: John Doe, Email: <EMAIL>, Phone: 1234567890, Company: ABC Corp, Sales Contact ID: 1
        Enter new name or press 'Enter':
        Enter new email or press 'Enter':
        Enter new phone or press 'Enter':
        Enter new company or press 'Enter':
        Enter new sales contact ID or press 'Enter':
        2
        Client John Doe updated successfully.
    """
    from epic.cli.auth_cli import user_auth

    client_id = get_input("Enter client ID to update:", int)
    try:
        client = Client.get(Client.id == client_id)
        try:
            sales_contact = User.get(User.id == client.sales_contact.id)
        except DoesNotExist:
            typer.echo("Sales contact does not exist. Contact an administator.")

        if client.sales_contact.id == user_auth.id or user_auth.role.name in [
            "admin",
            "super_admin",
        ]:
            typer.echo(
                f"Client ID: {client.id}, Name: {client.name}, Email: {client.email}, Phone: {client.phone}, Company: {client.company}, Sales Contact ID: {client.sales_contact.id}"
            )
        else:
            typer.echo(f"Client {client.name} does not belong to you.")
            return None
    except DoesNotExist:
        typer.echo(f"Client with ID {client_id} does not exist.")

    name = get_input("Enter new name or press 'Enter'", str, default=client.name)
    email = get_input("Enter new email or press 'Enter'", "email", default=client.email)
    phone = get_input("Enter new phone or press 'Enter'", "phone", default=client.phone)
    company = get_input(
        "Enter new company or press 'Enter'", str, default=client.company
    )
    sales_contact_id = get_input(
        "Enter new sales contact ID or press 'Enter'",
        int,
        default=client.sales_contact.id,
    )

    try:
        sales_contact = User.get(User.id == sales_contact_id)
        client.name = name
        client.email = email
        client.phone = phone
        client.company = company
        client.sales_contact = User.get(User.id == sales_contact_id)
        client.save()
        typer.echo(f"Client {client.name} updated successfully.")
    except DoesNotExist:
        typer.echo(f"Sales contact with ID '{sales_contact_id}' does not exist.")


@app.command("read")
def my_clients():
    """Get a list of all clients where the user is the sales contact

    Args:
    None

    Returns:
    A list of all clients where the user is the sales contact

    Raises:
    None

    Example:
    To get a list of all clients where the user is the sales contact, you can run the following command:
    $ python -m epic client my_clients
    Client ID: 1, Name: Acme Corp, Email: <EMAIL>, Phone: <PHONE>, Company: Acme Corp, Sales Contact ID: 1
    Client ID: 2, Name: Globex Corp, Email: <EMAIL>, Phone: <PHONE>, Company: Globex Corp, Sales Contact ID: 1
    ...
    """
    from epic.cli.auth_cli import user_auth

    clients = Client.select().where(Client.sales_contact == user_auth.id)
    for client in clients:
        typer.echo(
            f"Client ID: {client.id}, Name: {client.name}, Email: {client.email}, Phone: {client.phone}, Company: {client.company}, Sales Contact ID: {client.sales_contact.id}"
        )


if __name__ == "__main__":
    pass
