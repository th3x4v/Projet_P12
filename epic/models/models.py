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
import bcrypt
import typer

SESSION_FILE = "jwt_token.txt"

SECRET_KEY = "your-secret-key"


db = peewee.SqliteDatabase("database.db", pragmas={"foreign_keys": 1})


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Role(BaseModel):
    name = CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return f"Role {self.name}"


class Permission(BaseModel):
    name = CharField(unique=True)


class RolePermission(BaseModel):
    role = ForeignKeyField(Role)
    permission = ForeignKeyField(Permission)


class User(BaseModel):
    name = CharField(max_length=50, null=False)
    email = CharField(max_length=50, unique=True)
    password = CharField(max_length=255, null=False)
    role = ForeignKeyField(Role, backref="users")

    _permissions: list[str] = None

    def __str__(self):
        return f"User {self.name}"

    def has_perm(self, permission: str):
        """Return True if the user has the permission else False"""
        if self._permissions is None:
            query = (
                Permission.select()
                .join(RolePermission)
                .join(Role)
                .where(Role.name == self.role.name)
            )
            self._permissions = [perm.name for perm in query]
            print(self._permissions)
        return permission in self._permissions

    @staticmethod
    def create_superuser(name, email, password):
        """
        Creates a new superuser with the given name and password.

        Args:
            name (str): The name of the new superuser.
            password (str): The password for the new superuser.
        """
        admin_role = Role.get(Role.name == "super_admin")
        User.create(name=name, email=email, password=password, role=admin_role)

    def save(self, *args, **kwargs):
        self.password = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt())
        super().save(*args, **kwargs)

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
        try:
            user = cls.get(cls.email == email)
            if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                return user
            else:
                print("password doesnt match")
                return None
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
        expiration_time = datetime.utcnow() + timedelta(hours=1)

        # Define the payload of the JWT, which includes the user ID, role, and expiration time
        payload = {
            "user_id": self.id,
            "role": self.role.name,
            "exp": expiration_time,
        }

        # Replace 'your-secret-key' with a secure secret key for signing the token
        token = jwt.encode(payload, "your-secret-key", algorithm="HS256")

        return token

    @staticmethod
    def is_auth():
        try:
            with open("jwt_token.txt", "r") as token_file:
                token = token_file.read().strip()
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                # Check if the token is not expired and has necessary information
                if "user_id" in decoded_token and "role" in decoded_token:
                    # Store user information in the instance
                    print("user_id")
                    print(decoded_token["user_id"])
                    user = User.get_by_id(int(decoded_token["user_id"]))
                    return user
                else:
                    typer.echo("Invalid token. Please reauthenticate.")
                    return None
        except (
            FileNotFoundError,
            jwt.ExpiredSignatureError,
            jwt.InvalidTokenError,
        ):
            typer.echo("Authentication required. Please run 'login' command.")
            return None


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
    name = CharField(max_length=255, null=False)
    client = ForeignKeyField(Client, backref="contracts")
    total_amount = FloatField(default=0.0)
    due_amount = FloatField(default=0.0)
    signed = BooleanField(default=False)
    date_created = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Contract {self.id}"


class Event(BaseModel):
    name = CharField(max_length=50, null=False)
    contract = ForeignKeyField(Contract, backref="events")
    support_contact = ForeignKeyField(User, null=True, default=None, backref="events")
    date_start = DateTimeField()
    date_end = DateTimeField()
    location = CharField(max_length=50)
    attendees = IntegerField()
    notes = TextField()

    def __str__(self):
        return f"Event {self.name}"
