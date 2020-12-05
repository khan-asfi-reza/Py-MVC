from mvc.db import Model
from mvc.hash import Encryption
import datetime


# User Model of the app
class User(Model):
    verbose_name = 'Users'
    password = None
    created = None

    # This method is used to hash password
    @staticmethod
    def hash_password(password):
        # Using the Encryption Class
        encryption = Encryption(password)
        # Returns hashed password
        return encryption.encrypt()

    # Set hashed password
    def set_password(self, password):
        if password is not None:
            self.password = self.hash_password(password)

    # Gets hashed password
    def get_hashed_password(self):
        return self.password

    # Every model for the app must have this method and required fields must be declared in this manner
    def __init__(self, username="", age=0, **kwargs):
        super().__init__()
        self.username = username
        self.age = age

    # Custom Save method for user model
    def save(self):
        # Sets account creation time
        self.created = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        # Getting fields and values
        dictionary = self.__dict__
        # Checking if user with this username already exists or not
        user = self.objects.get(**{'username': self.username})
        # If user with this username exists then we will return empty dictionary
        if len(user) > 0:
            print("User account with that username already exist")
            return {}
        else:
            # If username is not used we will create the account
            return self.objects.create(**dictionary)

    # This class method is used to authenticate user with username and password
    @classmethod
    def authenticate(cls, username, password):
        # Checks if user with that username is available or not
        user = cls().objects.get(**{'username': username})
        if len(user) == 0:
            print("Username does not exist")
            return None
        # if user is available then we will check if password matches or not
        if password == Encryption(user[0]['password']).decrypt():
            return user[0]
        else:
            print("Invalid credentials")
            return None


# Post Model will use default Model methods
class Posts(Model):

    def __init__(self, title="", body="", user=None, **kwargs):
        super().__init__()
        self.title = title
        self.body = body
        self.user = user


# Book model
class Books(Model):
    def __init__(self, name="", publisher="", writer="", **kwargs):
        super().__init__()
        self.name = name
        self.publisher = publisher
        self.writer = writer
