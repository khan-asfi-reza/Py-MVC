"""

Database, model and objects

Our json data structure

{

"table_1":[],
"table_2":[]

}

Each object in the database json file will represent a table
here table_1 array is a table - Model

"""

import json
from abc import ABC, abstractmethod

from mvc.dsa import Sort, Stack

# This class is for printing statement with colors
class BCOLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# This is database class, it will handle database read and write functionality
class DB:
    __filename = None

    # Mutator method to set the database file name
    def set_filename(self, filename):
        self.__filename = filename
        return self.__filename

    # Getter method to get the name of the database
    def get_file(self):
        return self.__filename

    # Constructor method
    def __init__(self, filename):
        # Setting the database file name
        self.set_filename(filename)

    def read(self):
        # Open the database
        __db = open(self.get_file(), 'r')
        # Read the database and save it inside info variable
        __info = __db.read()
        # Closes the db connection
        __db.close()
        return __info

    def write(self, data):
        # Opens
        __db = open(self.get_file(), 'w')
        __info = __db.write(data)
        __db.close()
        return ""


# In this project we will save our data in a json file, use this as a database
# In single responsibility pattern, every class is responsible for one thing

# Here database class will be responsible for handing data with our json database
# Abstract base class
class DatabaseManager(ABC):
    # Name of the json file
    __filename = ''
    # Name of the object/table
    table = ""

    # This method takes json data and converts it to python dictionary
    @staticmethod
    def deserialize(data):
        return json.loads(data)

    # This method takes python dictionary/array and converts it into json format and dumps data in the database
    @staticmethod
    def serialize(data):
        return json.dumps(data, indent=2)

    # Sets the name of the databse/json file
    @classmethod
    def set_filename(cls, filename):
        cls.__filename = filename
        return cls.__filename

    # This method returns data in stack
    @abstractmethod
    def get_all_stack(self):
        pass

    # This method returns data in python list
    @abstractmethod
    def get_all(self):
        pass

    # Returns the name of the file
    def get_filename(self):
        return self.__filename

    # If the json file is corrupted, this method will reset the json file
    def create_safe_database(self):
        # Open the json file
        if len(self.db.read()) == 0:
            # If json file is empty we will make a proper json file
            data = json.dumps({})
            self.db.write(data)

    # This method returns python dictionary from the json file
    def get_database_data(self):
        data = self.deserialize(self.db.read())
        return data

    # This method creates table in the json file if that table does not exist in the json file
    def check_or_create_table(self, data):
        try:
            # Check if instance table is in database if not then we will create and empty table inside the json database
            if self.table not in data.keys():
                # Creating empty table
                data[f"{self.table}"] = []
                # Using serialize method
                self.db.write(self.serialize(data))
        except Exception as E:
            print(E)

    # This method sets the table attribute of the instance object and creates table if that does not exist
    def set_table(self, table):
        # Set the instance table
        self.table = table
        # Checks if database is corrupted or not, if corrupted it will fix the database
        self.create_safe_database()
        # If the table does not exist, it will create a table
        self.check_or_create_table(self.get_database_data())
        return self.table

    # Constructor method - json file
    def __init__(self, filename):
        # setting the database file name
        self.set_filename(filename)
        # db open close class
        self.db = DB(self.get_filename())
        # Checking if database is clean
        self.create_safe_database()

    # Updates the table
    def update_table(self, data, table=None):
        # Gets the table in stack data structure format
        table_data = self.get_all_stack() if table is None else table
        # Insert unique serial id in the data dictionary
        try:
            __id = table_data.peek()['id'] + 1
        except Stack.EmptyStackError:
            __id = 1
        _data = {**{"id": __id}, **data}
        # Pushes the data in the stack
        table_data.push(_data)
        # Returns the table in list format and created data
        return [table_data.toList(), _data]

    def update_database(self, database_data, table):
        # Updates database
        database_data[self.table] = table
        db = self.db
        # Insert new data in the database
        db.write(self.serialize(database_data))

    def insert(self, data):
        try:
            # Getting the database data from the json file
            database_data = self.get_database_data()
            # Getting the updated table
            table = self.update_table(data)
            # Update database
            self.update_database(database_data, table[0])
            # Returning the data
            return table[1]
        except Exception as E:
            raise E

    def modify(self, table, data):
        try:
            # Getting the database data from the json file
            database_data = self.get_database_data()
            # Update database
            self.update_database(database_data, table)
            # Returning the data
            return data
        except Exception as E:
            raise E

    def destroy(self, table):
        try:
            # Getting the database data from the json file
            database_data = self.get_database_data()
            # Update database
            self.update_database(database_data, table)
            # Returning the data
            return "Data deleted"
        except Exception as E:
            raise E


# Object Interface
# Abstract base class
class ObjectInterface(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def sorted(self, key, sorting_type='bubble'):
        pass

    @abstractmethod
    def get(self):
        pass


# Object class is the connector between model, view and database, object class handles data, query data and sends
# data from model to database or view to database, it simply connects database with model or view
class Objects(DatabaseManager, ObjectInterface):

    # Each model represents a table, object class handles data and sends data to the database manager class
    def __init__(self, table):
        super().__init__('db.json')
        self.set_table(table)
        # Sort algorithm class
        self.sort = Sort()

    # Returns data in stack structure form
    def get_all_stack(self, *args):
        try:
            # Fetch data from database and convert it into stack
            table_data = Stack(*self.get_database_data()[self.table])
            return table_data
        # If database table is not in the database, we will show the following message
        except KeyError:
            print("Database Table not Found")

    # Returns data in python list format
    def get_all(self):
        try:
            database_data = self.get_database_data()[self.table]
            return database_data

        except KeyError:
            print("Database Table not Found")

    # Gets the data from database, sorts it and returns the sorted data
    def sorted(self, key, sorting_type='bubble_sort'):
        try:
            # Gets listed data
            # Gets data in list format
            listed_data = self.get_all()
            # if sorting type is bubble
            try:
                # Returns the sorting function
                sorting_function = getattr(self.sort, sorting_type)
                # Sorts data and returns data using
                return sorting_function(listed_data, key)
            # If there is no method named 'sorting_type' We will show error
            except AttributeError:
                print(
                    f"{BCOLORS.FAIL}No attribute named {sorting_type}, options are - bubble_sort, insertion_sort {BCOLORS.ENDC}")
                return listed_data

        except (KeyError, ValueError):
            print('Invalid database key')

    # Creates data in the database
    def create(self, **kwargs):
        try:
            return self.insert(kwargs)
        except Exception as e:
            raise e

    # Getting data from table using key and value
    def get(self, **kwargs):
        # Gets listed data
        data = self.get_all()
        # Query data which we will return from this function
        query_data = []
        # Linear search through the data

        for each_data in data:
            # All provided query condition
            condition = True
            # Checks if any key not available in the table data
            false_key = False
            # The key that is not available
            unavailable_key = None
            # Looping through all provided query keywords
            for each_search_key in kwargs:
                # If a searched key|field is not in the database table we will rise the false key and break the loop
                if each_search_key not in each_data.keys():
                    false_key = True
                    unavailable_key = each_search_key
                    break
                # If any condition mismatches we will break the loop
                if each_data[each_search_key] != kwargs[each_search_key]:
                    condition = False
                    break
            # If false key is true
            if false_key:
                print(f"{BCOLORS.FAIL}"
                      f"There is no field named '{unavailable_key}' in the table '{self.table}' \
                       {BCOLORS.ENDC}")
                return []

            # If all condition matches we will put the data in returning query data list
            if condition is True:
                query_data.append(each_data)

        # Sort the data
        return self.sort.insertion_sort(query_data, 'id')

    # Delete data from database
    def delete(self, pk):
        # Gets all data from database
        data = self.get_all()
        # Removes the data selected from the list
        new_data = list(filter(lambda each: each['id'] != pk, data))
        # Destroying the data
        return self.destroy(new_data)

    # Updating data in the database of an existing data
    def update(self, pk, **kwargs):
        # Getting the data using get method and id of that data
        data = self.get(id=pk)
        # If query length is 0 we will return the error message
        if len(data) == 0:
            return "Data with given id not found"
        else:
            # Getting the data from the list
            data = data[0]
            # Updating the data
            data.update(**kwargs)
            # Getting all data
            data_list = self.get_all()
            for each in data_list:
                try:
                    # Updating the table with the updated data
                    if each['id'] == pk:
                        each.update(data)
                except KeyError:
                    print("Id not found")
            return self.modify(data_list, data)


# Abstract base class
# Model Base Class

# Every model must have __init__(**kwargs) method
#
# Examples provided in models.py


class Model(ABC):
    # Child model name
    model_name = ''

    # Model fields

    # Constructor method setting model name to it's child model name
    def __init__(self, **kwargs):
        self.model_name = self.__class__.__name__

    # Saves model information into database
    def save(self):
        dictionary = self.__dict__
        return self.objects.create(**dictionary)

    # The connector between model and database
    @property
    def objects(self):
        return Objects(self.__class__.__name__)
