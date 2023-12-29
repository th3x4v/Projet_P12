import typer
from epic.models.models import (
    Event,
    Contract,
    User,
    Client,
    Role,
    db,
    RolePermission,
    Permission,
)
import peewee
from datetime import datetime


app = typer.Typer()
roles_data = ["admin", "sales", "support", "super_admin"]

models_for_permissions = ["user", "contract", "client", "role", "event"]
permissions = ["create", "read", "list", "update", "delete"]
roles_perms = [
    {"role": 1, "permission": 1},  # admin can create user
    {"role": 4, "permission": 1},  # super_admin can create user
    {"role": 1, "permission": 2},  # admin can read user
    {"role": 2, "permission": 2},  # sales can read user
    {"role": 3, "permission": 2},  # support can read user
    {"role": 4, "permission": 2},  # super_admin can read user
    {"role": 1, "permission": 3},  # admin can list users
    {"role": 2, "permission": 3},  # sales can list users
    {"role": 4, "permission": 3},  # super_admin can list users
    {"role": 1, "permission": 4},  # admin can update user
    {"role": 4, "permission": 4},  # super_admin can update user
    {"role": 1, "permission": 5},  # admin can delete user
    {"role": 4, "permission": 5},  # super_admin can delete user
    {"role": 1, "permission": 6},  # admin can create contract
    {"role": 2, "permission": 6},  # sales can create contract
    {"role": 4, "permission": 6},  # super_admin can create contract
    {"role": 1, "permission": 7},  # admin can read contract
    {"role": 2, "permission": 7},  # sales can read contract
    {"role": 3, "permission": 7},  # support can read contract
    {"role": 4, "permission": 7},  # super_admin can read contract
    {"role": 1, "permission": 8},  # admin can list contracts
    {"role": 2, "permission": 8},  # sales can list contracts
    {"role": 4, "permission": 8},  # super_admin can list contracts
    {"role": 1, "permission": 9},  # admin can update contract
    {"role": 2, "permission": 9},  # sales can update contract
    {"role": 4, "permission": 9},  # super_admin can update contract
    {"role": 1, "permission": 10},  # admin can delete contract
    {"role": 2, "permission": 10},  # sales can delete contract
    {"role": 4, "permission": 10},  # super_admin can delete contract
    {"role": 1, "permission": 11},  # admin can create client
    {"role": 2, "permission": 11},  # sales can create client
    {"role": 4, "permission": 11},  # super_admin can create client
    {"role": 1, "permission": 12},  # admin can read client
    {"role": 2, "permission": 12},  # sales can read client
    {"role": 4, "permission": 12},  # super_admin can read client
    {"role": 1, "permission": 13},  # admin can list clients
    {"role": 2, "permission": 13},  # sales can list clients
    {"role": 4, "permission": 13},  # super_admin can list clients
    {"role": 1, "permission": 14},  # admin can update client
    {"role": 2, "permission": 14},  # sales can update client
    {"role": 4, "permission": 14},  # super_admin can update client
    {"role": 1, "permission": 15},  # admin can delete client
    {"role": 2, "permission": 15},  # sales can delete client
    {"role": 4, "permission": 15},  # super_admin can delete client
    {"role": 1, "permission": 16},  # admin can create role
    {"role": 4, "permission": 16},  # super_admin can create role
    {"role": 1, "permission": 17},  # admin can read role
    {"role": 2, "permission": 17},  # sales can read role
    {"role": 3, "permission": 17},  # support can read role
    {"role": 4, "permission": 17},  # super_admin can read role
    {"role": 1, "permission": 18},  # admin can list roles
    {"role": 4, "permission": 18},  # super_admin can list roles
    {"role": 1, "permission": 19},  # admin can update role
    {"role": 4, "permission": 19},  # super_admin can update role
    {"role": 1, "permission": 20},  # admin can delete role
    {"role": 4, "permission": 20},  # super_admin can delete role
    {"role": 1, "permission": 21},  # admin can create event
    {"role": 2, "permission": 21},  # sales can create event
    {"role": 4, "permission": 21},  # super_admin can create event
    {"role": 1, "permission": 22},  # admin can read event
    {"role": 3, "permission": 22},  # support can read event
    {"role": 2, "permission": 22},  # sales can read event
    {"role": 4, "permission": 22},  # super_admin can read event
    {"role": 1, "permission": 23},  # admin can list events
    {"role": 2, "permission": 23},  # sales can list events
    {"role": 3, "permission": 23},  # support can list events
    {"role": 4, "permission": 23},  # super_admin can list events
    {"role": 1, "permission": 24},  # admin can update event
    {"role": 2, "permission": 24},  # sales can update event
    {"role": 3, "permission": 24},  # support can update event
    {"role": 4, "permission": 24},  # super_admin can update event
    {"role": 1, "permission": 25},  # admin can delete event
    {"role": 2, "permission": 25},  # sales can delete event
    {"role": 3, "permission": 25},  # support can delete event
    {"role": 4, "permission": 25},  # super_admin can delete event
    {"role": 1, "permission": 26},  # admin can update password
    {"role": 2, "permission": 26},  # sales can update password
    {"role": 3, "permission": 26},  # support can update password
    {"role": 4, "permission": 26},  # super_admin can update password
]


def create_permissions():
    "create crud permissions for each models"
    models_permissions = []
    # construct a dict for each model with crud permissions
    for model in models_for_permissions:
        model_permissions = [
            {"name": f"{model}-{permission}"} for permission in permissions
        ]
        models_permissions.extend(model_permissions)
    models_permissions.append({"name": "user-password"})
    print(models_permissions)

    with db.atomic():
        Permission.insert_many(models_permissions).execute()
    # associate roles with permissions
    with db.atomic():
        RolePermission.insert_many(roles_perms).execute()


def create_tables():
    """
    Create the database tables for the application.

    This function connects to the database, creates the tables if they do not already exist,
    and initializes the roles table with the default roles.
    """

    # Create tables if they don't already exist
    db.create_tables(
        [User, Client, Contract, Event, Role, Permission],
        safe=True,
    )


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
        super_admin = Role.get(Role.name == "super_admin")
        sales = Role.get(Role.name == "sales")
        support = Role.get(Role.name == "support")
        admin = Role.get(Role.name == "admin")
        User.create_superuser("admin", "admin@epic.com", "password")

        RolePermission.create_table()
        create_permissions()

        # Create users
        User.create(name="ana", email="ana@epic.com", password="password", role=admin)
        User.create(name="tom", email="tom@epic.com", password="password", role=admin)
        User.create(name="bob", email="bob@epic.com", password="password", role=sales)
        User.create(name="pam", email="pam@epic.com", password="password", role=sales)
        User.create(name="max", email="max@epic.com", password="password", role=support)
        User.create(name="val", email="val@epic.com", password="password", role=support)

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
