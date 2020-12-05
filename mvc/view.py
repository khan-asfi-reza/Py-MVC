"""

As this projects follows mvc/mtv pattern

In MVC pattern The controller is the view in MTV pattern

View is the controller, that interacts with the user, takes input/instruction, User tells the controller what to do,
and controller takes the instruction and behave accordingly. Controller takes instruction and gets or interacts with the
model as per the instruction, the model returns some data and the data is rendered in the template

Every view will have one Model Class, that will return certain data or take certain data from the controller. That data
will be rendered in the template

Every view class will have view methods, and those methods will have route
Route is basically the input instruction, Suppose, input_view is assigned to the route '1'
So if the user types 1 in the console he will be able to see input_method running on the console

View methods are basically nested views in one single view

In Django framework, One view is capable of handling 4 request -> GET, POST, PUT, DELETE

As this project is inspired by the system of django, so in one view, there will be 4 default view methods

detail_view() - GET, list_view() - GET, input_view() - POST, update_view() - PUT

Every custom view_method must be in this format

def custom_view(*args, **kwargs):
    code...

Examples are provided in app.py
"""

from mvc.db import Model
from mvc.template import Template


# Every View class must have a referring model class
class View:
    # Name of the model
    model = Model

    # authenticated user
    auth_user = {}

    # View methods
    __view_methods = [

    ]
    # Template class object
    template = Template()

    # For registering custom view method
    def register(self):
        return []

    # For unregistering any default method
    def unregister(self):
        return []

    # Initiating default view methods mentioned above
    def initiate_view_method(self):
        self.__view_methods = [
            {
                'route': '1',
                'method': self.input_view,
                'name': f'Create {self.model.__name__}'
            },
            {
                'route': '2',
                'method': self.list_View,
                'name': f'View {self.model.__name__}'
            },
            {
                'route': '3',
                'method': self.detail_view,
                'name': f'Search {self.model.__name__}'
            },
            {
                'route': '4',
                'method': self.update_view,
                'name': f'Update {self.model.__name__}'
            },
        ]

    # Unregisetring method function that will take place in constructor method
    def unregister_view_method(self):
        # Get methods that needs to be unregistered
        args = self.unregister()
        # Loop through the list of methods
        for each_method in args:
            # Looping through the view methods list
            for each in self.__view_methods:
                if each['method'] == each_method:
                    # Removing the method from the list
                    self.__view_methods.remove(each)

    # Registering method function that will take place in constructor method
    def register_view_method(self):
        args = self.register()
        for each_method in args:
            for each in self.__view_methods:
                if each['method'] == each_method['method']:
                    self.__view_methods.remove(each)
        self.__view_methods = self.__view_methods + args

    # Returns sorted queryset
    def get_queryset(self):
        return self.model().objects.sorted('id')

    # Renders/Prints the information

    # Input From/input form
    def input_form(self):
        return {}

    # Update Form/input form
    def update_form(self):
        return {}

    # Shows all data of the table
    def list_View(self, *args, **kwargs):
        queryset = self.get_queryset()
        return self.template.render(queryset)

    # Shows searched data
    def detail_view(self, *args, **kwargs):
        print("Search: Using ID of data")
        # Getting search id
        inp = input("Search:> ID:>>")
        try:
            # Getting the search data using id
            object_data = self.model().objects.get(id=int(inp))
            self.template.render(object_data)
        except ValueError:
            print("Invalid Search id, please enter a number")

    # Updates data
    def update_view(self, *args, **kwargs):
        # Gets data from update form
        query_data = self.update_form()
        # Getting the data that needs to be updated
        if query_data is not None:
            object_data = self.model().objects.get(id=query_data['id'])
            try:
                # If the data that needs to be updated we will return no data found
                if len(object_data) == 0 or len(object_data > 1):
                    print("Data not found")
                    return ""
                # If the user of the data is not the authenticated user will raise an error
                elif object_data['user']['username'] != self.auth_user['username']:
                    print(f"You are not the owner of this data")
                    return ""

            except (KeyError, ValueError):
                pass

            finally:
                # If no error we will update the data
                print("Data updated successfully")
                # Getting the id of the data
                pk = query_data['id']
                # Removing the id from query data
                del query_data['id']
                return self.model().objects.update(pk, query_data)

    # Input view

    def input_view(self, callback, *args, **kwargs):
        # Gets data from input form
        form_data = self.input_form()
        if form_data != {}:
            # Creates model instance
            model_instance = self.model(**form_data)
            # Gets the saved data
            data = model_instance.save()
            if callback is not None and data is not None:
                # If data is valid we will run the callback function
                callback(data)

    def __init__(self, auth_user):
        # Setting authenticated user for this view
        self.auth_user = auth_user
        # Initiate view methods[default]
        self.initiate_view_method()
        # If any method needs to be unregistered in custom Views it will be unregistered
        self.unregister_view_method()
        # If any method needs to be registered in custom Views it will be registered
        self.register_view_method()

    # This is the controller of the view and the root view method that combines every view method
    def view(self, callback):
        # Event loop
        running = True
        while running:
            for each in self.__view_methods:
                # Looping through every view method
                print(f"{each['route']}:- {each['name']}")

            command = input(f"{self.model.__name__}>>")
            for each in self.__view_methods:
                if command == each['route']:
                    each['method'](callback=callback)
                    break
            running = False
