from tkinter import *
from tkinter import messagebox, simpledialog
import json
import random
import pyperclip

class PasswordManager:

    def __init__(self, window,canvas,logo_img):
        self.window=window
        self.canvas=canvas
        self.logo_img=logo_img
        self.create_gui()

    def create_gui(self):
        self.email = simpledialog.askstring(title="Username/Email Address", prompt="Enter your default username",
                                            parent=self.window)
        image = self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.grid(column=2, row=1)

        Label(width=20, height=5, text="Website:").grid(column=1, row=3)

        self.website_entry = Entry(width=35)
        self.website_entry.grid(column=2, row=3, columnspan=2)

        Label(width=20, height=5, text="Email/Username:").grid(column=1, row=4)

        self.username_entry = Entry(width=35)
        self.username_entry.insert(0, self.email)
        self.username_entry.grid(column=2, row=4, columnspan=2)

        Label(width=20, height=5, text="Password:").grid(column=1, row=5)

        self.password_entry = Entry(width=21)
        self.password_entry.grid(column=2, row=5)

        Button(text="Generate Password", command=self.generate).grid(column=4, row=4)

        Button(text="Add", command=self.add, width=18, highlightthickness=0).grid(column=4, row=7,
                                                                                               columnspan=2)

        Button(text="View All", command=self.view_all, width=18).grid(column=4, row=5, columnspan=2)

        Button(text="Search", command=self.search, width=18, highlightthickness=0).grid(column=4, row=3)

        Button(text="Delete credentials", command=self.delete_entries, width=18).grid(column=4, row=9)

        self.var1 = StringVar(self.window)
        self.var1.set("Delete all entries")
        OptionMenu(self.window, self.var1, "Delete all entries", "Delete assigned entry").grid(column=1, row=9)

        self.var2 = StringVar(self.window)
        self.var2.set("Random amount of characters for generated password")
        OptionMenu(self.window, self.var2, "Random amount of characters for generated password",
                              "Assign number of characters").grid(column=2, row=10)


    def write_data(self, data):
        '''Writes the supplied dictionary file to the json file'''
        with open("login_data.json", "w") as file:
            json.dump(data, file)

    def load_data(self):
        '''try to load data. if file is not found it creates it and returns empty dictionary'''
        empty_dict = {}
        try:
            with open("login_data.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            self.write_data(empty_dict)
            return {}
        except json.decoder.JSONDecodeError:
            return {}

    def nums_of_char(self):
        '''returns values for number of letters/numbers and symbols to be added to the generated password'''
        number_upper=simpledialog.askinteger(title="Amount of Uppercase letters",
                                             prompt="Choose how many uppercase letters there will be in the password",
                                             parent=self.window,minvalue=2,maxvalue=8)
        number_lower = simpledialog.askinteger(title="Amount of lowercase letters",
                                                 prompt="Choose how many lower case letters to use in password: ", parent=self.window,
                                                 minvalue=2, maxvalue=8)
        number_numbers = simpledialog.askinteger(title="Amount of numbers",
                                                 prompt="Choose how many numbers to use in password: ", parent=self.window,
                                                 minvalue=4, maxvalue=12)
        number_symbols = simpledialog.askinteger(title="Amount of symbols",
                                                 prompt="Choose how many symbols to use in password: ", parent=self.window,
                                                 minvalue=4, maxvalue=12)
        return number_upper,number_lower, number_numbers, number_symbols

    def delete_entries(self):
        '''this function deletes either a specific entry or all entries based on the optionmenu selected item'''
        try:
            website = self.website_entry.get()
        except AttributeError:
            messagebox.showerror(title="Oooops",
                                 message=f"There is no value in website.\nPlease choose a website to delete the data")
        # input is checked in order to delete all entries or a specific one
        else:
            if self.var1.get() == "Delete assigned entry":
                data = self.load_data()
                if website in data.keys():
                    if messagebox.askokcancel(title=f"{website.title()}",
                                              message="Want to delete the saved credentials?"):
                        data.pop(website)
                        self.write_data(data)
                    else:
                        return None
                else:
                    messagebox.showinfo(title=f"{website.title()} Credentials",
                                        message=f"There are no saved credentials for {website}")


            else:
                data = self.load_data()
                data.clear()
                self.write_data(data)

    def view_all(self):
        '''View all credentials one by one'''
        data = self.load_data()
        # if data file is empty it outputs an appropriate message otherwise it loops through the data file and outputs all credentials
        if len(data) == 0:
            messagebox.showerror(title="Oops", message="There are no saved credentials")
        else:
            for key in data.keys():
                messagebox.showinfo(title=f"{key.title()} credentials",
                                    message=f"Website: {key.title()}\nUsername: {data[key]['Username']}\nPassword: {data[key]['Password']}")

    def search(self):
        '''Search for a specific websites credentials in all of the saved credentials'''
        website = self.website_entry.get()
        if bool(website):
            data = self.load_data()

            if website in data:
                messagebox.showinfo(title=f"{website.title()} credentials",
                                    message=f"Username: {data[website]['Username']}\nPassword: {data[website]['Password']}")
            else:
                messagebox.showerror(title="Error", message="There are no credentials that match your search parameter")

        else:
            messagebox.showerror(title="Oops", message="You haven't entered a website to search for")

    def generate(self):
        '''letters numbers and symbols lists in order to generate random elements from each list to generate a password.Also copies password to clipboard
            You can either choose how many letters,numbers or symbols to use within a range of 4-12 or you can randomly generate the amount of characters'''
        upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                   'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        lower=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z' ]

        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
        password_list = []
        # if option menu 2's option is random amount of characters randomly generate the amount of characters to be created in the password

        num_up,num_low, num_num, num_sym = self.nums_of_char() if self.var2.get() == "Assign number of characters" else (
        random.randint(2, 8),random.randint(2, 8), random.randint(4, 12), random.randint(4, 12))
        password_list.extend(random.choice(upper) for _ in range(num_up))
        password_list.extend(random.choice(lower) for _ in range(num_low))

        password_list.extend(random.choice(numbers) for _ in range(num_num))
        password_list.extend(random.choice(symbols) for _ in range(num_sym))
        # reorganizes the password list
        random.shuffle(password_list)
        # convert to string
        password_str = "".join(password_list)
        # empty all entries and fill the password entry with the new password
        self.password_entry.delete(0, END)
        self.password_entry.insert(0, password_str)
        # copy password to clipboard
        pyperclip.copy(password_str)


    def add(self):
        '''saves or updates credentials. if entries are vacant it outputs an appropriate message'''
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        new_data = {website: {"Username": username, "Password": password}}
        if bool(website) and bool(password) and bool(username):
            data = self.load_data()
            # checks to see if there is already a password for the website. nif there is then the previous entry gets deleted and the new information is saved
            if website in data:
                del data[website]
                data.update(new_data)
                self.write_data(data)
            else:
                data.update(new_data)
                self.write_data(data)
        else:
            messagebox.showerror(title="Error", message="You have not submitted all of the credentials")


def main():
    window = Tk()
    canvas = Canvas(width=200, height=200)
    logo_img = PhotoImage(file="./logo.png")
    app = PasswordManager(window,canvas,logo_img)
    window.mainloop()

if __name__ == "__main__":
    main()