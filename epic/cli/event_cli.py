import typer
from models.models import Event, Contract, User
from peewee import DoesNotExist
from cli.auth_cli import authenticated_command

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


if __name__ == "__main__":
    app()
