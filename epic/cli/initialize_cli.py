import typer
from epic.models.models import Event, Contract, User, Client, Role, db
import peewee
from datetime import datetime

app = typer.Typer()
roles_data = ["admin", "sales", "support", "super_admin"]


def create_tables():
    """
    Create the database tables for the application.

    This function connects to the database, creates the tables if they do not already exist,
    and initializes the roles table with the default roles.
    """

    # Create tables if they don't already exist
    db.create_tables([User, Client, Contract, Event, Role], safe=True)


def initialize_roles():
    """
    Initializes the roles table with the default roles.

    This function creates the default roles (admin, sales, and support) if they do not already exist.
    """

    for role_name in roles_data:
        try:
            Role.create(name=role_name)
        except peewee.IntegrityError:
            # Role already exists, ignore the error
            pass


@app.command("initialize")
def initialize():
    """
    Initialize the database
    """
    with db:
        if db.is_closed() == True:
            db.connect()
        create_tables()
        initialize_roles()
        User.create_superuser("admin", "admin@epic.com", "password")
        sales = Role.get(Role.name == "sales")
        support = Role.get(Role.name == "support")
        admin = Role.get(Role.name == "admin")

        # Create users
        User.create(name="ana", email="ana@epic.com", password="password", role=admin)
        User.create(name="tom", email="tom@epic.com", password="password", role=admin)
        User.create(name="bob", email="bob@epic.com", password="password", role=sales)
        User.create(name="pam", email="pam@epic.com", password="password", role=sales)
        User.create(name="max", email="max@epic.com", password="password", role=support)
        User.create(name="val", email="val@epic.com", password="password", role=support)

        # ... (your existing code)

        # Create clients
        client1 = Client.create(
            name="John Doe",
            email="john.doe@company1.com",
            phone="123-456-7890",
            company="Company1",
            sales_contact=User.get(
                User.name == "bob"
            ),  # Assuming "bob" is the sales user
        )

        client2 = Client.create(
            name="Jane Smith",
            email="jane.smith@company2.com",
            phone="987-654-3210",
            company="Company2",
            sales_contact=User.get(
                User.name == "pam"
            ),  # Assuming "pam" is the sales user
        )

        # Create contracts for client1
        contract1_client1 = Contract.create(
            name="Contract1 for John Doe",
            client=client1,
            total_amount=5000.0,
            due_amount=2500.0,
            signed=True,
        )

        contract2_client1 = Contract.create(
            name="Contract2 for John Doe",
            client=client1,
            total_amount=8000.0,
            due_amount=4000.0,
            signed=False,
        )

        # Create events for contract1_client1
        event1_contract1_client1 = Event.create(
            name="Event1 for Contract1",
            contract=contract1_client1,
            support_contact=User.get(
                User.name == "max"
            ),  # Assuming "max" is the support user
            date_start=datetime(2023, 1, 1, 12, 0),
            date_end=datetime(2023, 1, 1, 18, 0),
            location="Venue1",
            attendees=100,
            notes="Lorem ipsum dolor sit amet.",
        )

        event2_contract1_client1 = Event.create(
            name="Event2 for Contract1",
            contract=contract1_client1,
            support_contact=User.get(
                User.name == "val"
            ),  # Assuming "val" is the support user
            date_start=datetime(2023, 2, 1, 12, 0),
            date_end=datetime(2023, 2, 1, 18, 0),
            location="Venue2",
            attendees=150,
            notes="Lorem ipsum dolor sit amet.",
        )

        # Create contracts for client2
        contract1_client2 = Contract.create(
            name="Contract1 for Jane Smith",
            client=client2,
            total_amount=6000.0,
            due_amount=3000.0,
            signed=True,
        )

        contract2_client2 = Contract.create(
            name="Contract2 for Jane Smith",
            client=client2,
            total_amount=9000.0,
            due_amount=4500.0,
            signed=False,
        )

        # Create events for contract1_client2
        event1_contract1_client2 = Event.create(
            name="Event1 for Contract1",
            contract=contract1_client2,
            support_contact=User.get(
                User.name == "max"
            ),  # Assuming "max" is the support user
            date_start=datetime(2023, 3, 1, 12, 0),
            date_end=datetime(2023, 3, 1, 18, 0),
            location="Venue3",
            attendees=120,
            notes="Lorem ipsum dolor sit amet.",
        )

        event2_contract1_client2 = Event.create(
            name="Event2 for Contract1",
            contract=contract1_client2,
            support_contact=User.get(
                User.name == "val"
            ),  # Assuming "val" is the support user
            date_start=datetime(2023, 4, 1, 12, 0),
            date_end=datetime(2023, 4, 1, 18, 0),
            location="Venue4",
            attendees=200,
            notes="Lorem ipsum dolor sit amet.",
        )

        typer.echo(f"Project initialized successfully.")
