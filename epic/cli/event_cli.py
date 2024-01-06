import typer
from epic.models.models import Event, Contract, User, Role
from peewee import DoesNotExist
from epic.cli.auth_cli import check_auth
from epic.utils import get_input


app = typer.Typer(callback=check_auth)


@app.command("create")
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
    from epic.cli.auth_cli import user_auth

    contract_id = get_input("Enter contract ID", int)
    try:
        contract = Contract.get(Contract.id == contract_id)
        if contract.client.sales_contact.id == user_auth.id or user_auth.role.name in [
            "admin",
            "super_admin",
        ]:
            if contract.signed is False:
                typer.echo("Contract is not signed. Not possible to create event.")
                return None
        else:
            typer.echo("Contract does not belong to you.")
            return None
    except Contract.DoesNotExist:
        typer.echo(f"Contract with ID {contract_id} does not exist.")
        return None
    name = get_input("Enter event name", str)

    date_start = get_input("Enter start date (YYYY-MM-DD)", "date")
    date_end = get_input("Enter end date (YYYY-MM-DD)", "date")
    location = get_input("Enter location", str)
    attendees = get_input("Enter number of attendees", int)
    notes = get_input("Enter notes", str)

    try:
        event = Event.create(
            name=name,
            contract=contract,
            date_start=date_start,
            date_end=date_end,
            location=location,
            attendees=attendees,
            notes=notes,
        )
        typer.echo(f"Event {event.name} created successfully.")
    except DoesNotExist:
        typer.echo("Contract does not exist.")


@app.command("list")
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
    from epic.cli.auth_cli import user_auth

    event_id = get_input("Enter event ID to delete", int)
    try:
        event = Event.get(Event.id == event_id)
        if (
            user_auth.id == event.support_contact.id
            or user_auth.id == event.contract.client.sales_contact.id
            or user_auth.role.name in ["admin", "super_admin"]
        ):
            event.delete_instance()
            typer.echo(f"Event {event.name} deleted successfully.")
        else:
            typer.echo("You do not have permission to delete this event.")
    except DoesNotExist:
        typer.echo(f"Event with ID {event_id} does not exist.")


@app.command("update")
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
    from epic.cli.auth_cli import user_auth

    event_id = get_input("Enter event ID to update", int)
    try:
        event = Event.get(Event.id == event_id)
        if user_auth.role.name in [
            "admin",
            "super_admin",
        ]:
            support_contact_id = get_input("Enter support contact ID to update", int)
            try:
                support = Role.get(Role.name == "support")
                support_contact = User.get(
                    (User.id == support_contact_id) & (User.role == support)
                )
                event.support_contact = support_contact
                event.save()
                typer.echo(f"Support contact of {event.name} added successfully.")
            except DoesNotExist:
                typer.echo(
                    f"Support contact with ID '{support_contact_id}' does not exist."
                )
                return None
    except DoesNotExist:
        typer.echo(
            f"Event with ID {event_id} or Contract or support contact does not exist."
        )
        return None

    name = get_input("Enter new name or press 'Enter':", str, default=event.name)
    date_start = get_input(
        "Enter new start date or press 'Enter'", "date", default=event.date_start
    )
    date_end = get_input(
        "Enter new end date or press 'Enter'", "date", default=event.date_end
    )
    location = get_input(
        "Enter new location or press 'Enter'", str, default=event.location
    )
    attendees = get_input(
        "Enter new number of attendees or press 'Enter'",
        int,
        default=event.attendees,
    )
    notes = get_input("Enter new notes or press 'Enter'", str, default=event.notes)

    try:
        event.name = name
        event.date_start = date_start
        event.date_end = date_end
        event.location = location
        event.attendees = attendees
        event.notes = notes

        event.save()
        typer.echo(f"Event {event.name} updated successfully.")
    except DoesNotExist:
        typer.echo(f"Support contact with ID {support_contact_id} does not exist.")


@app.command("read")
def my_events():
    """
    Returns a list of events that the user is associated with or event whitout support for admin user

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
    from epic.cli.auth_cli import user_auth

    if user_auth.role.name == "support":
        events = (
            user_auth.events
        )  # Access events through the relationship defined in models
        for event in events:
            typer.echo(f"Event ID: {event.id}, Name: {event.name}")
    elif user_auth.role.name == "sales":
        events = Event.select()
        for event in events:
            if event.contract.client.sales_contact == user_auth:
                typer.echo(
                    f"Event ID: {event.id}, Name: {event.name}, Contract ID: {event.contract.id}, Location: {event.location}"
                )
    elif user_auth.role.name in ["admin", "super_admin"]:
        events = Event.select().where(Event.support_contact.is_null())
        for event in events:
            typer.echo(f"Event ID: {event.id}, Name: {event.name}")
    else:
        typer.echo("User not allowed to view events.")


if __name__ == "__main__":
    app()
