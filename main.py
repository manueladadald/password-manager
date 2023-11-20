from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
FONT = ("Courier", 12, "normal")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    pass_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)

    pass_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = web_entry.get()
    username = user_entry.get()
    user_password = pass_entry.get()
    new_data = {
        website: {
            "username": username,
            "password": user_password
        }
    }

    if len(website) < 1 or len(username) <1 or len(user_password) < 1:
        messagebox.showerror(title="Ooops...", message="Please don't leave any information empty!")

    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        finally:
            web_entry.delete(0, "end")
            pass_entry.delete(0, "end")
            messagebox.showinfo(title="Success!", message="Your information has been saved!")


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = web_entry.get()

    if len(website) < 1:
        messagebox.showerror(title="Ooops...", message="Please insert a website to search for the password")

    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            messagebox.showerror(title="Ooops...", message="No Data File Found")

        else:
            if website in data:
                username = data[website]["username"]
                password = data[website]["password"]
                messagebox.showinfo(title="Information found", message=f"Username: {username}\nPassword: {password}")

            else:
                messagebox.showerror(title="Ooops...", message=f"No available details for {website}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

image = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

web_label = Label(text="Website:", font=FONT)
web_label.grid(column=0, row=1, sticky="w")

web_entry = Entry(width=30)
web_entry.focus()
web_entry.grid(column=1, row=1, sticky="e")

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1, sticky="e")

user_label = Label(text="Email/Username:", font=FONT)
user_label.grid(column=0, row=2, sticky="w")

user_entry = Entry(width=49)
user_entry.insert(0, string="enter-your-email@line-116.com")
user_entry.grid(column=1, row=2, columnspan=2, sticky="e")

pass_label = Label(text="Password:", font=FONT)
pass_label.grid(column=0, row=3, sticky="w")

pass_entry = Entry(width=30)
pass_entry.grid(column=1, row=3, sticky="e")

generate = Button(text="Generate Password", command=generate_password)
generate.grid(column=2, row=3, sticky="e")

add_button = Button(text="Add", width=42, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="e")

window.mainloop()
