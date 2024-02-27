import tkinter as t
from tkinter import messagebox as mb
from classes import DataForm

# Directories
# Insert text file destination in the string
loan_directory = ""
inquiry_directory = ""  


# Submit button in main menu
def submit(category, customer_name):
    if category == 1 and customer_name != "" or category == 2 and customer_name != "":
        p_number = 0
        directory = ""
        top = t.Toplevel(main_window)
        top.resizable(False, False)
        top.geometry("250x150")
        option_one = t.StringVar()
        option_two = t.StringVar()
        option_three = t.StringVar()

        if category == 1:   # Loans menu
            top.title("Loans Menu")
            directory = loan_directory
            p_number = get_priority_number("L", directory)
            option_one.set("Short Term Loan")
            option_two.set("Housing Loan")
            option_three.set("Calamity Loan")
        elif category == 2:   # Inquiries menu
            top.title("Inquiries Menu")
            directory = inquiry_directory
            p_number = get_priority_number("I", directory)
            option_one.set("MID Number")
            option_two.set("MP2 Savings")
            option_three.set("Membership OFWs")

        # Base menu
        label_text = t.StringVar()
        label_text2 = t.StringVar()
        label_text.set("Good day, " + customer_name)
        label_text2.set("Your priority number is: " + p_number)
        t.Label(top, textvariable=label_text, anchor="w", justify="left").grid(row=0, column=0, sticky="w")

        selected = t.IntVar()   # Index Value

        t.Label(top, textvariable=label_text2, anchor="w", justify="left").grid(row=1, column=0, sticky="w")

        option1 = t.Radiobutton(top, textvariable=option_one, variable=selected, value=1)
        option1.grid(row=2, column=0, sticky="w")  # Short Term Loan of MID Number

        option2 = t.Radiobutton(top, textvariable=option_two, variable=selected, value=2)
        option2.grid(row=3, column=0, sticky="w")  # Housing Loan or MP2 Savings

        option3 = t.Radiobutton(top, textvariable=option_three, variable=selected, value=3)
        option3.grid(row=4, column=0, sticky="w")  # Calamity Loan or Membership OFWs

        transaction_type = None  # Placeholder to work around making the class in two parts
        customer = DataForm(p_number, customer_name, transaction_type, "Waiting")

        button = t.Button(top, text="Enter", command=lambda: upload(customer, directory, top, category, selected.get()))
        button.grid(row=7, columnspan=2)

    else:
        if customer_name == "":
            mb.showerror("Error", "Please input your name.")
        else:
            mb.showerror("Error", "Please select a valid category.")


# To generate a priority number
def get_priority_number(prefix, directory):
    p_number = prefix + "0000"
    try:
        with open(directory, "r") as f:
            i = f.readlines()
            if i:
                prev = i[-1].split(", ")[0][1:]
                new = str(int(prev) + 1).zfill(4)
                p_number = prefix + new
                return p_number
            else:
                return p_number
    except Exception as e:
        print(f"Error in generatePriorityNumber: {e}")
        return p_number


# To get transaction type
def get_transaction_type(category, key):
    transaction = ""
    if category == 1:
        if key == 1:
            transaction = "Short Term Loan"
        elif key == 2:
            transaction = "Housing Loan"
        elif key == 3:
            transaction = "Calamity Loan"
    elif category == 2:
        if key == 1:
            transaction = "MID Number"
        elif key == 2:
            transaction = "MP2 Savings"
        elif key == 3:
            transaction = "Membership OFWs"

    return transaction


# Upload customer data to text file
def upload(customer, directory, window, category, key):
    customer.transaction = get_transaction_type(category, key)
    f = open(directory, "a")
    f.write(f"{customer.priority}, {customer.name}, {customer.date}, {customer.transaction}, {customer.remarks} \n")
    window.destroy()
    window.update()


# Customer Window
main_window = t.Tk()
main_window.title("Customer Form")
main_window.resizable(False, False)

t.Label(main_window, text="Name: ", anchor="w", justify="left").grid(row=0, column=0, sticky="w")
name_text = t.Entry(main_window)
name_text.grid(row=1, columnspan=2)

category_selected = t.IntVar()
t.Label(main_window, text="Select a category to generate a Priority Number: \n").grid(row=2, column=0)
loan_button = t.Radiobutton(main_window, text="Priority Loans Number", variable=category_selected, value=1)
loan_button.grid(row=3, column=0)
inquiry_button = t.Radiobutton(main_window, text="Priority Inquiry Number", variable=category_selected, value=2)
inquiry_button.grid(row=3, column=1)

submit_button = t.Button(main_window, text="Submit", command=lambda: submit(category_selected.get(), name_text.get()))
submit_button.grid(row=4, columnspan=2)

main_window.mainloop()
