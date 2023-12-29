import typer
from epic.models.models import Contract, Client
from peewee import DoesNotExist
from epic.cli.auth_cli import check_auth
from epic.utils import get_input

app = typer.Typer(callback=check_auth)


@app.command("create")
def create_contract():
    """
    Creates a new contract.

    Args:
        name (str): The name of the contract.
        client_id (int): The ID of the client.
        total_amount (float): The total amount of the contract.
        due_amount (float): The due amount of the contract.
        signed (bool): Whether the contract is signed or not.

    Returns:
        None

    Raises:
        DoesNotExist: If the client with the given ID does not exist.
    Example:
        To create a new contract with the name "Contract 1", client ID "1", total amount "1000", due amount "500", and signed "True", you can run the following command:
        $ python -m epic contract create
        Enter contract name: Contract 1
        Enter client ID: 1
        Enter total amount: 1000
        Enter due amount: 500
        Is the contract signed? (True/False): True
        Contract Contract 1 created successfully.
    """
    from epic.cli.auth_cli import user_auth

    client_id = get_input("Enter client ID for the new contract", int)

    try:
        client = Client.get(Client.id == client_id)
        if client.sales_contact.id == user_auth.id:
            name = get_input("Enter contract name", str)
            signed = get_input("Is the contract signed? (True/False)", bool)
            total_amount = get_input("Enter total amount", float)
            due_amount = get_input("Enter due amount", float)
            contract = Contract.create(
                name=name,
                client=client,
                total_amount=total_amount,
                due_amount=due_amount,
                signed=signed,
            )
            typer.echo(f"Contract {contract.name} created successfully.")
        else:
            typer.echo(f"Client {client.name} does not belong to you.")
    except DoesNotExist:
        typer.echo("Client does not exist.")


@app.command("list")
def list_contracts():
    """Get a list of all contracts

    Args:
    None

    Returns:
    A list of all contracts

    Raises:
    None

    Example:
    To get a list of all contracts, you can run the following command:
    $ python -m epic contract list
    Contract ID: 1, Name: Contract 1, Client ID: 1, Signed: True
    Contract ID: 2, Name: Contract 2, Client ID: 2, Signed: False
    ...
    """
    contracts = Contract.select()
    for contract in contracts:
        typer.echo(
            f"Contract ID: {contract.id}, Name: {contract.name}, Client ID: {contract.client.id}, Signed: {contract.signed}"
        )


@app.command("delete")
def delete_contract():
    """Deletes a contract.

    Args:
        contract_id (int): The ID of the contract to delete.

    Returns:
        None

    Raises:
        DoesNotExist: If the contract with the given ID does not exist.
        Forbidden: If the user does not have permission to delete the contract.

    Example:
        To delete a contract with ID 1, you can run the following command:
        $ python -m epic contract delete
        Enter contract ID to delete: 1
        Contract 1 deleted successfully.
    """
    from epic.cli.auth_cli import user_auth

    contract_id = get_input("Enter contract ID to delete", int)
    try:
        contract = Contract.get(Contract.id == contract_id)

        if contract.client.sales_contact.id == user_auth.id or user_auth.role.name in [
            "admin",
            "super_admin",
        ]:
            contract.delete_instance()
            typer.echo(f"Contract {contract.name} deleted successfully.")
        else:
            typer.echo("You do not have permission to delete this contract.")
    except DoesNotExist:
        typer.echo(f"Contract with ID {contract_id} does not exist.")


@app.command("update")
def update_contract():
    """
    Updates an existing contract.

    Args:
        contract_id (int): The ID of the contract to update.

    Returns:
        None

    Raises:
        DoesNotExist: If the contract with the given ID does not exist.
        Forbidden: If the user does not have permission to update the contract.

    Example:
        To update a contract with ID 1, you can run the following command:
        $ python -m epic contract update
        Enter contract ID to update: 1
        Contract ID: 1, Name: Contract 1, Client ID: 1, Signed: True
        Enter new name or press 'Enter': Contract 1 Updated
        Is the contract signed? (True/False): False
        Enter new total amount: 1000
        Enter new due amount: 500
        Contract Contract 1 Updated updated successfully.
    """
    from epic.cli.auth_cli import user_auth

    contract_id = get_input("Enter contract ID to update", int)
    try:
        contract = Contract.get(Contract.id == contract_id)

        if contract.client.sales_contact.id == user_auth.id or user_auth.role.name in [
            "admin",
            "super_admin",
        ]:
            typer.echo(
                f"Contract ID: {contract.id}, Name: {contract.name}, Client ID: {contract.client.id}, Signed: {contract.signed}"
            )
        else:
            typer.echo(f"Contract {contract.name} does not belong to you.")
            return None
    except DoesNotExist:
        typer.echo(f"Contract with ID {contract_id} does not exist.")

    name = get_input("Enter new name or press 'Enter'", str, default=contract.name)
    signed = get_input(
        "Is the contract signed? (True/False)", bool, default=contract.signed
    )
    total_amount = get_input(
        "Enter new total amount", float, default=contract.total_amount
    )
    due_amount = get_input("Enter new due amount:", float, default=contract.due_amount)

    contract.name = name
    contract.signed = signed
    contract.total_amount = total_amount
    contract.due_amount = due_amount

    contract.save()
    typer.echo(f"Contract {contract.name} updated successfully.")


@app.command("read")
def my_contracts():
    """Get a list of all contracts where the user is the sales contact

    Args:
        None
    Returns:
        A list of all contracts where the user is the sales contact
    Raises:
        None
    Example:
        To get a list of all contracts where the user is the sales contact, you can run the following command:
        $ python -m epic contract my_contracts
        Contract ID: 1, Name: Contract 1, Client ID: 1, Signed: True
        Contract ID: 2, Name: Contract 2, Client ID: 2, Signed: False
        ...
    """
    from epic.cli.auth_cli import user_auth

    clients = (
        user_auth.clients
    )  # Access events through the relationship defined in models
    for client in clients:
        if client.sales_contact.id == user_auth.id:
            contracts = client.contracts
            for contract in contracts:
                typer.echo(
                    f"Contract ID: {contract.id}, Name: {contract.name}, Client ID: {client.id}, Signed: {contract.signed}"
                )


if __name__ == "__main__":
    app()
