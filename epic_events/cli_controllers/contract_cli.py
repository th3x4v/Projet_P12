import typer
from models.models import Contract, Client
from peewee import DoesNotExist
from cli_controllers.auth_cli import authenticated_command

app = typer.Typer()


@app.command("create-contract")
@authenticated_command
def create_contract(
    contract_name: str,
    client_id: int,
    total_amount: float,
    due_amount: float,
    signed: bool,
):
    try:
        client = Client.get(Client.id == client_id)
        contract = Contract.create(
            contract_name=contract_name,
            client=client,
            total_amount=total_amount,
            due_amount=due_amount,
            signed=signed,
        )
        typer.echo(f"Contract {contract.contract_name} created successfully.")
    except DoesNotExist:
        typer.echo("Client does not exist.")


@app.command("list-contracts")
@authenticated_command
def list_contracts():
    contracts = Contract.select()
    for contract in contracts:
        typer.echo(
            f"Contract ID: {contract.id}, Name: {contract.contract_name}, Client ID: {contract.client.id}, Signed: {contract.signed}"
        )


@app.command("delete-contract")
@authenticated_command
def delete_contract(contract_id: int):
    try:
        contract = Contract.get(Contract.id == contract_id)
        contract.delete_instance()
        typer.echo(f"Contract {contract.contract_name} deleted successfully.")
    except DoesNotExist:
        typer.echo(f"Contract with ID {contract_id} does not exist.")


@app.command("update-contract")
@authenticated_command
def update_contract(
    contract_id: int,
    contract_name: str,
    client_id: int,
    total_amount: float,
    due_amount: float,
    signed: bool,
):
    try:
        contract = Contract.get(Contract.id == contract_id)
        client = Client.get(Client.id == client_id)

        contract.contract_name = contract_name
        contract.client = client
        contract.total_amount = total_amount
        contract.due_amount = due_amount
        contract.signed = signed

        contract.save()
        typer.echo(f"Contract {contract.contract_name} updated successfully.")
    except DoesNotExist:
        typer.echo(f"Contract with ID {contract_id} or Client does not exist.")


if __name__ == "__main__":
    app()
