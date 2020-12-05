## **Project Name : MVC**

##### **Language: Python**

This project is built upon the MVC Architecture, 
and this project works quite like the Django Framework, which is a web framework and works on the web
except this project/library only works on the terminal to demonstrate it's workability.
This project shadows some of the small features of the Django Framework. Again, this project only
works on the terminal/bash/command line. 

As this project is inspired by the features and the architecture of Django Framework,
this project also follows system like, Model, View, and Controller.

**What is MVC Pattern?**

Model–view–controller (usually known as MVC) is a software design pattern commonly used for developing User interface that divides the related program logic into three interconnected elements.
 
For this project our UI is the command line.
In Django the MVC is referred as MTV - Model Template View, Model is Model, Template is the view, And View is the controller 

**Model**

The central component of the pattern. It is the application's dynamic data structure, independent of the user interface It directly manages the data, logic and rules of the application.

**View / Template**

Any representation of information such as a chart, diagram or table. Multiple views of the same information are possible, such as a bar chart for management and a tabular view for accountants.

**Controller / View**

Accepts input and converts it to commands for the model or view

***
**How mvc library will work**


This project uses mvc architecture, and also follows some feature of django framework.

In django framework, every model represents a table in the database, and in django some can use several databases.
For example: SQLite, PostgreSQL, MySQL, MongoDB, MariaDB etc

In our mvc library we will use json as our database, as it is easy to manage and there is a 
built in module 'json' for handling json files and json data. This project has no dependencies,
Only the built in functionality and modules are used.

Our database file is `db.json`

In regular database, there is table and every table has fields
As we are using json, there will be a root object, and inside that object there will be list/array of objects,
those list/array of objects will represent a table/model

db.json


    {
        "table1":[
            {
            "id":1, 
            "name":"FIELD"
            }
        ]
    }

`Model` Class represents a table in the database

So here model represents a table in the database, model handles data, set data logic and clean check the data.
Model class is capable of validating data with custom methods and with the help of `Object` class. 
Every model has a object property that does several thing with the data of the model.

`Object` class has a composition association with `Model` class.
`Model` class gets data and sends the data to the `Object` class.
`Object` class performs, data creation, update, delete, keyword query, getting sorted data list, getting stacked data list.
`Object` class inherits from the `DatabaseManager` class.

`DatabaseManager` class takes the data of the table and inserts/replaces/deletes that table in the database.
`DatabaseManager` class has an Aggregation Association  with the `DB` Class, `DB` class represents the database.
`DB` class opens a connection with the database, writes data and closes the connection.

Instead of setting, opening and closing the database every single time of a certain action, we created a different class,
that will handle data writing and reading from the json file. 

As we are using json as database, it is not possible to insert data without changing the whole json object.
So to change a particular table, we will get the whole json object, then from that json object we will get our 
required table as per the operation, then we will change our table as per the action we will perform

For example: We want to insert a new user into a table named 'users', so first we will get the entire object from the json file
Then we will get the `user` array from that object, then we will insert our new user in the user array, then we will insert the new 
array into the json object.

    

Database manager class gets the json object from the json file using the DB class.
Then DatabaseManager class deserialize or convert json into python dictionary, serializes any python dictionary into json format,

`View` is the controller(mvc)/view(mtv), between model and template

There is a main `View` class, that has some default view methods
 1. Input view -> Takes input data from user , saves the data and store it in the database
 2. List View  -> Shows list of all data of that particular table
 3. Update View -> Update a single data
 4. Detail view  -> Returns query data

In the view class, one can register new view methods or delete default view methods


`Template` class is the template(mtv)/view(mvc), that shows/renders data in the interface

`Form` class is a class that takes data/input from user

`App` class is the main UI class, or the main class container of the app
To run and use the app, user has to make a app object then register created Views, and then use the run method to run the app
 
Project Structure

****
    |----db.json
    |    post.txt
    |    book.txt
    |    app.py
    |    models.py
    |    mvc -----
    |            |
    |            |_____ db.py 
    |                   dsa.py     
    |                   hash.py
    |                   main.py
    |                   template.py
    |                   view.py
                      

mvc directory is the root library. 

db.py

1. DB Class --- This class can be used to read and write in a particular file

2. DatabaseManager Class(Abstract Class) --- Has aggregation with DB Class, to write into the json file and read from the json file. DatabaseManager Class has serialize method and deserialize method, that is used to convert py dictionary to json or json to py dictionary.
   update_table() method is used to update a table with a new data, update_database() method to insert a new/updated table into the database,
   modify() method to modify a table, destroy() method to delete a data from the table,      

3. Object Class (Inherited from DatabaseManager) --- get() method to search certain data with key and value, create() method to create new data and insert into the database, update() method to update a certain data, delete() method to delete data from the table, get_all() method to get all data of the table, get_all_stacked() to get all data in stack data structure
    sorted() to get data in sorted form
4. Model Class (Parent Class) --- This class must be used to create any model for the app
                                  This class is customizable, save() method to save a data  
                                  

dsa.py
1. Sort Class --- Sort class has 2 sorting algorithm, bubble_sort(), sorts array in bubble sort algorithm, insertion_sort() sorts array in insertion_sort algorithm
2. Stack --- Custom Stack Data Structure Class with Linked List Format, push() method to push data in the beginning, pop() to pop data from the front, getSize() to get size of the stack, 
   toList() converts stack into dynamic list, peek() returns the first item of the stack

hash.py
1. Encryption Class --- This class encrypts and decrypts a text/data, using keyed Caesar Cipher 

main.py
1. App Class --- This is the main app ui class, that runs all the controllers[views], set_auth_view() takes auth View Class
if there is any created auth view class, it can be added using this method, there must be only one auth view, 
auth view is a controller that controls User Authentication and Account Creation, if there is a auth view controller present in the app object, then without user authentication user will not be able to see other routes and views(controllers)
This class has register() method to register User Created View Classes, run() method to run the app created by the user     

template.py
1. Template Class --- This is template[mtv] / view[mvc] class.  render() method to render a queryset/data       
2. Form Class --- This is form class, to create input form, it takes input from the user   

view.py
1. View Class --- This is the Controller [mvc] / view[mtv] class. Every View must have a model attribute referring to a certain User Created Model
As Controllers in MVC connects with the model and then the model returns data and View renders those data. Every View Class has 4 Default view method, that performs certain task
It's like nested Controllers, 1 Main Controller and it has it's child controller. Those child Controller performs certain task. register() method to register custom view methods, unregister() method to unregister any view method. input_form() method is to create custom input form, update_form() method is used to create custom update form. view() method to run all the controllers        


In The Root folder There must be 2 files
1. app.py
2. models.py [without this file, app will not run]

models.py 

This file will have all custom created models

app.py[Can use any name]

    # To run the app, import App from mvc.main
    from mvc.main import App
    from mvc.view import View
    class View(View):
        ...
    
    app = App()
    app.register('1', CustomView) # Register takes 2 arguments, 1 is input route and another The View Class
    app.run()
                                     