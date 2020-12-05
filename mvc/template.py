class Template:
    @staticmethod
    def render(queryset):
        print("----------------------")
        print("")
        if len(queryset) == 0:
            print("No Data found")
        # Looping through all the data in the queryset
        for each_query in queryset:
            print("...............")
            for each_key in each_query.keys():
                if each_key == 'user':
                    if each_query['user'] is None:
                        print("User:- None")
                    else:
                        print(f"{each_key} :- {each_query[each_key]}")
                elif each_key == 'model_name':
                    continue
                elif each_key == 'password':
                    continue
                else:
                    print(f"{each_key} :- {each_query[each_key]}")
            print("...............")
        print("")
        print("----------------------")
        return ""


class Form:

    # Reusable form header text
    def form_header(self):
        print(self.title)
        if self.file_form:
            print("1| Use Text File  -> If you want to import your post from a text file")
            print("Write your post in this format to import your post from text file")
            print(self.file_example)
            print(f"Write your post in the '{self.file_name}' file")
            print("2| Use Input")

    # Method for creating form that will take input from bash/terminal
    def create_form(self):
        # Takes input field and their data type respectively
        # Input data will be returned from the function after taking all required inputs
        input_data = {}
        # Looping through each fields
        # Taking input in the required data type
        for each in self.fields:
            while True:
                try:
                    inp = self.fields[each](input(f"{each.capitalize()} :"))
                    break
                except ValueError:
                    print("Invalid data type, try again")
            # If field data type is string, we will remove unwanted whitespaces
            if type(inp) == str:
                inp = inp.rstrip('\n')
            # Insert input data in input data dictionary
            input_data.update({f"{each}": inp})
        return input_data

    # Method of file form that will take data from a text file
    def create_file_form(self):
        form_data = {}
        # Opens the file
        with open(self.file_name, 'r') as file:
            # Splits the file into list using delimiter
            data = file.read().split(self.delimiter)
            for index, each in self.fields.keys():
                ins_data = data[index]
                # Remove unwanted whitespace
                if type(ins_data) == str:
                    ins_data = ins_data.rsplit('\n')
                # Inserts data taken from the text file
                form_data.update({
                    f"{each}": ins_data
                })
            file.close()
        # Returns data
        return form_data

    # Form template renderer
    def render(self):
        post = {}
        self.form_header()
        if self.file_form:
            while True:
                inp = input(">>")
                if inp == "1":
                    post = self.create_file_form()
                    break
                elif inp == '2':
                    post = self.create_form()
                    break
        else:
            post = self.create_form()
        print("------------------------------------------")
        return post

    # Constructor method
    def __init__(self, file_form=True, file_name='', delimiter='///', title='', file_example='', fields=None):
        if fields is None:
            fields = {}
        # If form has text file input system
        self.file_form = file_form
        # Name of the text file form
        self.file_name = file_name
        # Delimiter to separate data from text file
        self.delimiter = delimiter
        # Input fields
        self.fields = fields
        # Form Title
        self.title = title
        # Example of Text file data system
        self.file_example = file_example

