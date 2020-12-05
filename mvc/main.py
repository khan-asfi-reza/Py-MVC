import os
import sys
import inspect
import importlib
from .db import Model


# This is our main app interface
class App:
    # Checks if user is authenticated
    __authenticated = False
    # Authenticated user information
    __authenticated_user = {}
    # Authentication view
    __auth_view = None
    # Model List
    models = []
    # View list
    views = []

    # Authenticate user
    def set_authentication(self, auth_user):
        if auth_user is not None:
            self.__authenticated = True
            self.__authenticated_user = auth_user

    # Checks if user is authenticated
    @property
    def isAuthenticated(self):
        return self.__authenticated

    # Get authenticated user
    def authenticated_user(self):
        return self.__authenticated_user

    # Sets the authentication view
    def set_auth_view(self, instance):
        self.__auth_view = instance

    # Gets authentication view
    @property
    def auth_view(self):
        return self.__auth_view

    # Get all models
    def get_models(self):
        for name, cls in inspect.getmembers(importlib.import_module("models"), inspect.isclass):
            # If the imported model is the subclass of model
            if issubclass(cls, Model) and cls != Model:
                self.models.append(cls)

    def __init__(self):
        # Gets all model
        self.get_models()

    # Registers views and routes
    def register(self, route, view):
        self.views.append(
            {
                "route": route,
                "view": view
            })

    # This is the run method that will run the application in the bash/terminal
    def run(self):

        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        os.chdir(dir_path)
        while True:
            if not self.isAuthenticated and self.auth_view is not None:
                self.auth_view(self.authenticated_user()).view(self.set_authentication)
            else:
                print("------------------------------------------------")
                print(f"Welcome to the system, {self.authenticated_user()['username']}")
                print("------------------------------------------------")
                while True:
                    for each_view in self.views:
                        print(f"{each_view['route']}. {each_view['view']({}).__str__()}")
                    inp = input("Run>>")
                    try:
                        for __each_view in self.views:
                            if inp == __each_view['route']:
                                __each_view['view'](self.__authenticated_user).view(None)
                    except Exception:
                        continue
