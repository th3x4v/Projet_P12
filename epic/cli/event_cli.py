import typer
from epic.models.models import Event, Contract, User
from peewee import DoesNotExist
from epic.cli.auth_cli import authenticated_command
from epic.cli.user_cli import method_allowed
from epic.cli.auth_cli import user_info

import inspect
import os

# Get the filename of the module
filename, _ = os.path.splitext(os.path.basename(os.path.abspath(__file__)))

app = typer.Typer()


@app.command("create-event")
@authenticated_command
def create_event(
    name: str,
    contract_id: int,
    support_contact_id: int,
    date_start: str,
    date_end: str,
    location: str,
    attendees: int,
    notes: str,
):
    try:
        contract = Contract.get(Contract.id == contract_id)
        support_contact = User.get(User.id == support_contact_id)
        event = Event.create(
            name=name,
            contract=contract,
            support_contact=support_contact,
            date_start=date_start,
            date_end=date_end,
            location=location,
            attendees=attendees,
            notes=notes,
        )
        typer.echo(f"Event {event.name} created successfully.")
    except DoesNotExist:
        typer.echo("Contract or support contact does not exist.")


@app.command("list-events")
@authenticated_command
def list_events():
    events = Event.select()
    for event in events:
        typer.echo(
            f"Event ID: {event.id}, Name: {event.name}, Contract ID: {event.contract.id}, Location: {event.location}"
        )


@app.command("delete-event")
@authenticated_command
def delete_event(event_id: int):
    try:
        event = Event.get(Event.id == event_id)
        event.delete_instance()
        typer.echo(f"Event {event.name} deleted successfully.")
    except DoesNotExist:
        typer.echo(f"Event with ID {event_id} does not exist.")


@app.command("update-event")
@authenticated_command
def update_event(
    event_id: int,
    name: str,
    contract_id: int,
    support_contact_id: int,
    date_start: str,
    date_end: str,
    location: str,
    attendees: int,
    notes: str,
):
    try:
        event = Event.get(Event.id == event_id)
        contract = Contract.get(Contract.id == contract_id)
        support_contact = User.get(User.id == support_contact_id)

        event.name = name
        event.contract = contract
        event.support_contact = support_contact
        event.date_start = date_start
        event.date_end = date_end
        event.location = location
        event.attendees = attendees
        event.notes = notes

        event.save()
        typer.echo(f"Event {event.name} updated successfully.")
    except DoesNotExist:
        typer.echo(
            f"Event with ID {event_id} or Contract or support contact does not exist."
        )


@app.command("update")
@authenticated_command
def update_event():
    function_name = inspect.currentframe().f_code.co_name
    if user_info["role"] in method_allowed[filename + "." + function_name]:
        event_id = typer.prompt("Enter event ID to update:")
        try:
            event = Event.get(Event.id == event_id)
            try:
                support_contact = User.get(User.id == event.support_contact.id)
            except DoesNotExist:
                if user_info["role"] == "admin":
                    support_contact_id = typer.prompt(
                        "Enter support contact ID to update:"
                    )
                    try:
                        sales_contact = User.get(User.id == support_contact_id)
                        event.sales_contact = support_contact
                        event.save()
                        typer.echo(f"Event {event.name} updated successfully.")
                    except DoesNotExist:
                        typer.echo(
                            f"Sales contact with ID '{support_contact_id}' does not exist."
                        )
                else:
                    typer.echo(
                        "Support contact does not exist. Contact an administator."
                    )
        except DoesNotExist:
            typer.echo(
                f"Event with ID {event_id} or Contract or support contact does not exist."
            )
            return None

        name = typer.prompt("Enter new name or press 'Enter':", default=event.name)
        contract_id = typer.prompt(
            "Enter new contract ID or press 'Enter':", default=event.contract.id
        )
        support_contact_id = typer.prompt(
            "Enter new support contact ID or press 'Enter':",
            default=event.support_contact.id,
        )
        date_start = typer.prompt(
            "Enter new start date or press 'Enter':", default=event.date_start
        )
        date_end = typer.prompt(
            "Enter new end date or press 'Enter':", default=event.date_end
        )
        location = typer.prompt(
            "Enter new location or press 'Enter':", default=event.location
        )
        attendees = typer.prompt(
            "Enter new number of attendees or press 'Enter':", default=event.attendees
        )
        notes = typer.prompt("Enter new notes or press 'Enter':", default=event.notes)

        try:
            contract = Contract.get(Contract.id == contract_id)
            support_contact = User.get(User.id == support_contact_id)

            event.name = name
            event.contract = contract
            event.support_contact = support_contact
            event.date_start = date_start
            event.date_end = date_end
            event.location = location
            event.attendees = attendees
            event.notes = notes

            event.save()
            typer.echo(f"Event {event.name} updated successfully.")
        except DoesNotExist:
            typer.echo(
                f"Contract with ID {contract_id} or support contact with ID {support_contact_id} does not exist."
            )
    else:
        print("User not allowed")


if __name__ == "__main__":
    app()
