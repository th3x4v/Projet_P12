from datetime import datetime, timedelta
from peewee import (
    CharField,
    IntegerField,
    FloatField,
    ForeignKeyField,
    DateTimeField,
    BooleanField,
    TextField,
)
import peewee
import jwt
from peewee import DoesNotExist


db = peewee.SqliteDatabase("database.db", pragmas={"foreign_keys": 1})


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Role(BaseModel):
    name = CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return f"Role {self.name}"


class User(BaseModel):
    name = CharField(max_length=50, null=False)
    email = CharField(max_length=50, unique=True)
    password = CharField(max_length=255, null=False)
    role = ForeignKeyField(Role, backref="users")

    def __str__(self):
        return f"User {self.name}"

    def create_superuser(name, email, password):
        """
        Creates a new superuser with the given name and password.

        Args:
            name (str): The name of the new superuser.
            password (str): The password for the new superuser.
        """
        admin_role = Role.get(Role.name == "admin")
        User.create(name=name, email=email, password=password, role=admin_role)

    @classmethod
    def authenticate(cls, email, password):
        """
        Authenticates a user with the given email and password.

        Args:
            email (str): The email of the user to authenticate.
            password (str): The password for the user to authenticate.

        Returns:
            User or None: The authenticated user, or None if authentication failed.
        """
        print("cls auhtenticate")
        try:
            user = cls.get(cls.email == email, cls.password == password)
            return user
        except DoesNotExist:
            print("user doenst exist")
            return None

    def generate_jwt_token(self):
        """
        Generate a JSON Web Token (JWT) to authenticate the user.

        Returns:
            str: The JWT token.
        """
        # Set the expiration time for the token (e.g., 1 hour)
        expiration_time = datetime.utcnow() + timedelta(hours=0.1)

        # Define the payload of the JWT, which includes the user ID, role, and expiration time
        payload = {
            "user_id": self.id,
            "role": self.role.name,
            "exp": expiration_time,
        }

        # Replace 'your-secret-key' with a secure secret key for signing the token
        token = jwt.encode(payload, "your-secret-key", algorithm="HS256")

        return token


class Client(BaseModel):
    name = CharField(max_length=50, null=False)
    email = CharField(max_length=50, unique=True)
    phone = CharField(max_length=15, null=False)
    company = CharField(max_length=50, null=False)
    date_created = DateTimeField(default=datetime.now)
    date_updated = DateTimeField(default=datetime.now)
    sales_contact = ForeignKeyField(User, backref="clients")

    def __str__(self):
        return f"Client {self.name}"

    def save(self, *args, **kwargs):
        """
        Save the model instance to the database.

        This method is a wrapper around the `Model.save` method that sets the
        `date_updated` field to the current date and time before saving.

        Args:
            *args: Positional arguments to pass to the `Model.save` method.
            **kwargs: Keyword arguments to pass to the `Model.save` method.

        Returns:
            The saved model instance.
        """
        self.date_updated = datetime.now()
        return super(Client, self).save(*args, **kwargs)


class Contract(BaseModel):
    contract_name = CharField(max_length=255, null=False)
    client = ForeignKeyField(Client, backref="contracts")
    total_amount = FloatField(default=0.0)
    due_amount = FloatField(default=0.0)
    signed = BooleanField(default=False)
    date_created = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Contract {self.contract_id}"


class Event(BaseModel):
    name = CharField(max_length=50, null=False)
    contract = ForeignKeyField(Contract, backref="events")
    support_contact = ForeignKeyField(User, backref="events")
    date_start = DateTimeField()
    date_end = DateTimeField()
    location = CharField(max_length=50)
    attendees = IntegerField()
    notes = TextField()

    def __str__(self):
        return f"Event {self.name}"


def create_tables():
    """
    Create the database tables for the application.

    This function connects to the database, creates the tables if they do not already exist,
    and initializes the roles table with the default roles.
    """
    db.connect()
    # Create tables if they don't already exist
    db.create_tables([User, Client, Contract, Event, Role], safe=True)
    initialize_roles()


def initialize_roles():
    """
    Initializes the roles table with the default roles.

    This function creates the default roles (admin, sales, and support) if they do not already exist.
    """
    roles_data = ["admin", "sales", "support"]

    for role_name in roles_data:
        try:
            Role.create(name=role_name)
        except peewee.IntegrityError:
            # Role already exists, ignore the error
            pass
