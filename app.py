from models import Posts, User, Books
from mvc.view import View
from mvc.main import App
from mvc.template import Form


# Auth view
class AccountView(View):
    # This view will handle model
    model = User

    # Unregistering default view methods
    def unregister(self):
        return [self.update_view, self.list_View, self.detail_view, self.input_view]

    # Registering custom view method
    def register(self):
        return [
            {
                'route': '1',
                'method': self.input_view,
                'name': 'Login'
            },
            {
                'route': '2',
                'method': self.creation_view,
                'name': 'Create Account'
            }
        ]

    # Creation view
    # This is a custom view method, It will handle account creation
    def creation_view(self, *args, **kwargs):
        # Using the Template Form Class to render input in the bash/terminal and getting input data
        form_data = Form(file_form=False, title="Create Account",
                         fields={'username': str, 'age': int, 'password': str}).render()
        # Setting user model
        user = self.model(form_data['password'], form_data['age'])
        # Setting user password
        user.set_password(form_data['age'])
        # Save the user and saving user data
        created = user.save()
        # If user save method returns empty dictionary, it means the account is created
        if created != {}:
            print("Account created please login")
        else:
            print("Account creation failed")

    # Account Login Form
    def input_form(self):
        # Using the Template Form Class to render input in the bash/terminal and getting input data
        form_data = Form(file_form=False, title="Login",
                         fields={'username': str, 'password': str}).render()
        # Authenticating user
        user = self.model.authenticate(form_data['username'], form_data['password'])
        if user is not None:
            return user
        print("Incorrect username and password")

    # Custom input view
    def input_view(self, callback, *args, **kwargs):
        form_data = self.input_form()
        callback(form_data)


class PostView(View):
    # View method for post model
    model = Posts
    # Text file for taking input
    file_name = 'post.txt'
    # Form of the view
    form = Form(title="Create Post",
                file_name=file_name,
                file_example="[Title]///\n[Body]",
                fields={
                    'title': str,
                    'body': str
                }).render()

    # This form handles post update
    def update_form(self):
        # Handles update form
        print("Update Post")
        try:
            # Taking the id of the data, that needs to be updated
            update_data_id = int(input("Updating Data ID: "))
            # Form class
            form = self.form()
            # Changing the title to Update
            form.title = 'Update Post'
            # Rendering the form
            form_data = form.render()
            # Adding user and id in the form data
            form_data.update(dict(user=self.auth_user['username'], id=update_data_id))
            return form_data
        except ValueError:
            print("Invalid id, please enter a number")
            return None

    def input_form(self):
        # Post creation form
        form = self.form()
        # Changing the title to post create
        form.title = 'Create Post'
        # Rendering the form
        form_data = form.render()
        # Adding user in the form data
        form_data.update(dict(user=self.auth_user['username']))
        return form_data

    def __str__(self):
        return f"Posts View"


class BookView(View):
    # View for the book model
    model = Books
    # Text file
    filename = 'book.txt'
    # Form class object
    form = Form(title='Create Book', file_name=filename,
                file_example="[Book Name]///\n[Publisher]\n///[Writer]",
                fields={
                    "name": str,
                    "publisher": str,
                    "writer": str
                }
                )

    # Update form
    def update_form(self):
        print("Update Book")
        try:
            pk = int(input("Update data id>>"))
            self.form.title = "Update Book"
            form_data = self.form.render()
            form_data.update({'id': pk})
            return form_data
        except ValueError:
            print("Invalid id, please enter a number")
            return None

    # Input form
    def input_form(self):
        self.form.title = "Create Book"
        form_data = self.form.render()
        return form_data

    def __str__(self):
        return f"Books View"


if __name__ == '__main__':
    # Getting app instance
    app = App()
    # Setting auth view
    app.set_auth_view(AccountView)
    # Registering the view in the app object with route
    app.register('1', PostView)
    app.register('2', BookView)
    app.run()
