import typer
from epic.models.models import Contract, Client, User
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
    name = typer.prompt("Enter contract name:")
    client_id = typer.prompt("Enter client ID:", type=int)
    total_amount = typer.prompt("Enter total amount:", type=float)
    due_amount = typer.prompt("Enter due amount:", type=float)
    signed = typer.prompt("Is the contract signed? (True/False):", type=bool)

    try:
        client = Client.get(Client.id == client_id)
        contract = Contract.create(
            name=name,
            client=client,
            total_amount=total_amount,
            due_amount=due_amount,
            signed=signed,
        )
        typer.echo(f"Contract {contract.name} created successfully.")
    except DoesNotExist:
        typer.echo("Client does not exist.")


@app.command("list")
@authenticated_command
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
@authenticated_command
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
    function_name = inspect.currentframe().f_code.co_name
    if user_info["role"] in method_allowed[filename + "." + function_name]:
        contract_id = typer.prompt("Enter contract ID to delete:", type=int)
        try:
            contract = Contract.get(Contract.id == contract_id)
            if contract.client.sales_contact.id == user_info["user_id"]:
                contract.delete_instance()
                typer.echo(f"Contract {contract.name} deleted successfully.")
            else:
                typer.echo("You do not have permission to delete this contract.")
        except DoesNotExist:
            typer.echo(f"Contract with ID {contract_id} does not exist.")
    else:
        print("User not allowed")


@app.command("update")
@authenticated_command
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
    function_name = inspect.currentframe().f_code.co_name
    if user_info["role"] in method_allowed[filename + "." + function_name]:
        contract_id = typer.prompt("Enter contract ID to update:")
        try:
            contract = Contract.get(Contract.id == contract_id)

            if (
                contract.client.sales_contact.id == user_info["user_id"]
                or user_info["role"] == "admin"
            ):
                typer.echo(
                    f"Contract ID: {contract.id}, Name: {contract.name}, Client ID: {contract.client.id}, Signed: {contract.signed}"
                )
            else:
                typer.echo(f"Contract {contract.name} does not belong to you.")
                return None
        except DoesNotExist:
            typer.echo(f"Contract with ID {contract_id} does not exist.")

        name = typer.prompt("Enter new name or press 'Enter':", default=contract.name)
        signed = typer.prompt(
            "Is the contract signed? (True/False):", type=bool, default=contract.signed
        )
        total_amount = typer.prompt(
            "Enter new total amount:", type=float, default=contract.total_amount
        )
        due_amount = typer.prompt(
            "Enter new due amount:", type=float, default=contract.due_amount
        )

        contract.name = name
        contract.signed = signed
        contract.total_amount = total_amount
        contract.due_amount = due_amount

        contract.save()
        typer.echo(f"Contract {contract.name} updated successfully.")
    else:
        print("User not allowed")


@app.command("my_contracts")
@authenticated_command
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
    function_name = inspect.currentframe().f_code.co_name
    user = User.get_by_id(user_info["user_id"])
    if user_info["role"] in method_allowed[filename + "." + function_name]:
        clients = (
            user.clients
        )  # Access events through the relationship defined in models
        for client in clients:
            if client.sales_contact.id == user_info["user_id"]:
                contracts = client.contracts
                for contract in contracts:
                    typer.echo(
                        f"Contract ID: {contract.id}, Name: {contract.name}, Client ID: {client.id}, Signed: {contract.signed}"
                    )
    else:
        typer.echo("User not allowed to view events.")


if __name__ == "__main__":
    app()
