import tkinter as t
from tkinter import messagebox as mb

# Directories
# Insert text file destination in the string
loan_directory = ""
inquiry_directory = ""  


# Process in staff view menu
def process(category):
    directory = ""
    transaction_type = ""
    p_number = ""
    if category == 1:
        directory = loan_directory
        transaction_type = "Loan"
    elif category == 2:
        directory = inquiry_directory
        transaction_type = "Inquiry"

    line_number = find_line_number(directory, "Done")
    if line_number != -1:
        with open(directory, "r+") as f:
            lines = f.readlines()
            if lines:
                prev = lines[line_number].split(", ")[4].strip()
                p_number = lines[line_number].split(", ")[0].strip()
                new_prev = "Done"
                lines[line_number] = lines[line_number].replace(prev, new_prev)
                f.seek(0)
                f.writelines(lines)
                f.truncate()
        mb.showinfo(f"{transaction_type} Processing", f"{transaction_type} {p_number} has been processed.")
    elif line_number == -1:
        mb.showerror("Error", "There are no more transactions to process.")


# For finding the number of the line without the keyword
def find_line_number(directory, keyword):
    with open(directory, "r+") as f:
        lines = f.readlines()
        if lines:
            for i in range(len(lines)):
                prev = lines[i].split(", ")[4].strip()
                if prev != keyword:
                    return i
    return -1


# View history
def view_history(category):
    directory = ""
    if category == 1:
        directory = loan_directory
    elif category == 2:
        directory = inquiry_directory

    with open(directory, "r") as f:
        content = f.read()

    top = t.Toplevel()
    top.title("History")

    text_w = t.Text(top)
    text_w.pack(fill=t.BOTH, expand=True)

    text_w.insert(t.END, content)


# View Queue
def view_queue(category):
    current_queue = []
    line_number = 0
    directory = ""
    transaction_type = ""
    if category == 1:
        directory = loan_directory
        line_number = find_line_number(directory, "Done")
        transaction_type = "loans"
    elif category == 2:
        directory = inquiry_directory
        line_number = find_line_number(directory, "Done")
        transaction_type = "inquiries"

    if line_number > -1:
        with open(directory, "r+") as f:
            lines = f.readlines()
            if lines:
                for i in range(line_number, len(lines)):
                    num = lines[i].split(", ")[0].strip()
                    current_queue.append(num)
        # Queue Menu
        top = t.Toplevel()
        top.title("View Queue")
        top.resizable(False, False)
        top.geometry("250x150")

        list_b = t.Listbox(top)
        list_b.pack(fill=t.BOTH, expand=True)
        for i in current_queue:
            list_b.insert(t.END, i)
    else:
        mb.showerror("Error", f"There are no {transaction_type} in queue.")


# Staff view window
root = t.Tk()
root.title("Staff View")
root.resizable(False, False)
root.geometry("250x150")

category_selected = t.IntVar()
t.Label(root, text="Please select a category:").grid(row=0, column=0)
loan_button = t.Radiobutton(root, text="Loans", variable=category_selected, value=1)
loan_button.grid(row=1, column=0)
inquiry_button = t.Radiobutton(root, text="Inquiry", variable=category_selected, value=2)
inquiry_button.grid(row=1, column=1)

history_button = t.Button(root, text="View History", command=lambda: view_history(category_selected.get()))
history_button.grid(row=3, column=0)
queue_button = t.Button(root, text="View Queue", command=lambda: view_queue(category_selected.get()))
queue_button.grid(row=3, column=1)
process_button = t.Button(root, text="Process", command=lambda: process(category_selected.get()))
process_button.grid(row=5, columnspan=2)

root.mainloop()
