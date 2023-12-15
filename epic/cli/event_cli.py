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


@app.command("create")
@authenticated_command
def create_event():
    """Create a new event

    This function prompts the user to enter the event's name, contract ID, support contact ID, start date, end date, location, number of attendees, and notes, and then creates a new event with the provided information.

    Args:
        None

    Returns:
        None

    Raises:
        DoesNotExist: If the contract ID or support contact ID provided does not exist

    Example:
        To create a new event with the name "Annual Meeting", contract ID "1", support contact ID "2", start date "2022-01-01", end date "2022-01-02", location "New York", number of attendees "100", and notes "Annual meeting of the company", you can run the following command:
        $ python -m epic  event create
        Enter event name: Annual Meeting
        Enter contract ID: 1
        Enter support contact ID: 2
        Enter start date: 2022-01-01
        Enter end date: 2022-01-02
        Enter location: New York
        Enter number of attendees: 100
        Enter notes: Annual meeting of the company
        Event Annual Meeting created successfully.
    """
    name = typer.prompt("Enter event name:")
    contract_id = typer.prompt("Enter contract ID:", type=int)
    support_contact_id = typer.prompt("Enter support contact ID:", type=int)
    date_start = typer.prompt("Enter start date:")
    date_end = typer.prompt("Enter end date:")
    location = typer.prompt("Enter location:")
    attendees = typer.prompt("Enter number of attendees:", type=int)
    notes = typer.prompt("Enter notes:")

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


@app.command("list")
@authenticated_command
def list_events():
    """
    Lists all events in the database.

    Args:
        None

    Returns:
        A list of events

    Raises:
        None

    Example:
        To list all events in the database, you can run the following command:
        $ python -m epic event list
        Event ID: 1, Name: Annual Meeting, Contract ID: 1, Location: New York
        Event ID: 2, Name: Customer Conference, Contract ID: 2, Location: San Francisco
    """
    events = Event.select()
    for event in events:
        typer.echo(
            f"Event ID: {event.id}, Name: {event.name}, Contract ID: {event.contract.id}, Location: {event.location}"
        )


@app.command("delete")
@authenticated_command
def delete_event():
    """Deletes an event based on the given event ID.

    Args:
        event_id (int): The ID of the event to delete.

    Returns:
        None

    Raises:
        DoesNotExist: If the event with the given ID does not exist.
    Example:
        To delete an event with the ID of 1, you can run the following command:
        $ python -m epic event delete
        Enter event ID to delete: 1
        Event Annual Meeting deleted successfully.

    """
    function_name = inspect.currentframe().f_code.co_name
    if user_info["role"] in method_allowed[filename + "." + function_name]:
        event_id = typer.prompt("Enter event ID to delete:")
        try:
            event = Event.get(Event.id == event_id)
            if (
                user_info["role"] == "admin"
                or user_info["user_id"] == event.support_contact.id
            ):
                event.delete_instance()
                typer.echo(f"Event {event.name} deleted successfully.")
            else:
                typer.echo("You do not have permission to delete this event.")
        except DoesNotExist:
            typer.echo(f"Event with ID {event_id} does not exist.")
    else:
        print("User not allowed")


@app.command("update")
@authenticated_command
def update_event():
    """
    Update an existing event.

    This function prompts the user to enter the event ID, new values for the event's name, contract ID, support contact ID, start date, end date, location, number of attendees, and notes, and then updates the event with the provided information.

    Args:
        event_id (int): The ID of the event to update.

    Returns:
        None

    Raises:
        DoesNotExist: If the event ID provided does not exist or if the contract ID or support contact ID provided does not exist.

    Example:
        To update event with ID 1 with the name "Annual Meeting 2023", contract ID "2", support contact ID "3", start date "2023-01-01", end date "2023-01-02", location "New York", number of attendees "150", and notes "Annual meeting of the company", you can run the following command:
        $ python -m epic  event update 1
        Enter event ID to update: 1
        Enter new name or press 'Enter': Annual Meeting 2023
        Enter new contract ID or press 'Enter': 2
        Enter new support contact ID or press 'Enter': 3
        Enter new start date or press 'Enter': 2023-01-01
        Enter new end date or press 'Enter': 2023-01-02
        Enter new location or press 'Enter': New York
        Enter new number of attendees or press 'Enter': 150
        Enter new notes or press 'Enter': Annual meeting of the company
        Event Annual Meeting 2023 updated successfully.
    """
    function_name = inspect.currentframe().f_code.co_name
    if user_info["role"] in method_allowed[filename + "." + function_name]:
        event_id = typer.prompt("Enter event ID to update:")
        try:
            event = Event.get(Event.id == event_id)
            try:
                support_contact = User.get(User.id == event.support_contact.id)
                if (
                    event.support_contact.id == user_info["user_id"]
                    or user_info["role"] == "admin"
                ):
                    typer.echo(
                        f"Contract ID: {event.id}, Name: {event.name}, Contract ID: {event.contract.id}, Location: {event.location}"
                    )
                else:
                    typer.echo(f"Contract {event.name} does not belong to you.")
                    return None
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


@app.command("my_events")
@authenticated_command
def my_events():
    """
    Returns a list of events that the user is associated with.

    Args:
        None

    Returns:
        A list of events

    Raises:
        None

    Example:
        To list all events that the user is associated with, you can run the following command:
        $ python -m epic event my_events
        Event ID: 1, Name: Annual Meeting
        Event ID: 2, Name: Customer Conference
    """
    user = User.get_by_id(user_info["user_id"])
    if user_info["role"] == "support":
        events = user.events  # Access events through the relationship defined in models
        print("events")
        print(events)
        for event in events:
            typer.echo(f"Event ID: {event.id}, Name: {event.name}")
    else:
        typer.echo("User not allowed to view events.")


if __name__ == "__main__":
    app()
