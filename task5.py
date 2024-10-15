import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("contacts.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT)''')
conn.commit()

class ContactManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Contact Manager")
        self.master.geometry("500x500")

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()

        self.create_widgets()
        self.load_contacts()

    def create_widgets(self):
        # Create input fields
        tk.Label(self.master, text="Name:").pack()
        tk.Entry(self.master, textvariable=self.name_var).pack()

        tk.Label(self.master, text="Phone:").pack()
        tk.Entry(self.master, textvariable=self.phone_var).pack()

        tk.Label(self.master, text="Email:").pack()
        tk.Entry(self.master, textvariable=self.email_var).pack()

        tk.Label(self.master, text="Address:").pack()
        tk.Entry(self.master, textvariable=self.address_var).pack()

        # Create buttons
        tk.Button(self.master, text="Add Contact", command=self.add_contact).pack(pady=5)
        tk.Button(self.master, text="View Contacts", command=self.view_contacts).pack(pady=5)
        tk.Button(self.master, text="Search Contact", command=self.search_contact).pack(pady=5)
        tk.Button(self.master, text="Update Contact", command=self.update_contact).pack(pady=5)
        tk.Button(self.master, text="Delete Contact", command=self.delete_contact).pack(pady=5)

    def add_contact(self):
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        address = self.address_var.get()

        if name and phone:
            c.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)", 
                      (name, phone, email, address))
            conn.commit()
            messagebox.showinfo("Success", "Contact added successfully")
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Name and Phone are required")

    def view_contacts(self):
        c.execute("SELECT * FROM contacts")
        contacts = c.fetchall()

        contacts_list = "\n".join([f"{contact[1]} - {contact[2]}" for contact in contacts])
        if contacts_list:
            messagebox.showinfo("Contacts", contacts_list)
        else:
            messagebox.showinfo("Contacts", "No contacts found")

    def search_contact(self):
        name_or_phone = simpledialog.askstring("Search", "Enter name or phone:")
        c.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?", 
                  ('%' + name_or_phone + '%', '%' + name_or_phone + '%'))
        results = c.fetchall()

        if results:
            contacts_list = "\n".join([f"{contact[1]} - {contact[2]}" for contact in results])
            messagebox.showinfo("Search Results", contacts_list)
        else:
            messagebox.showinfo("Search Results", "No contacts found")

    def update_contact(self):
        name = simpledialog.askstring("Update", "Enter the name of the contact to update:")
        c.execute("SELECT * FROM contacts WHERE name = ?", (name,))
        contact = c.fetchone()

        if contact:
            new_phone = simpledialog.askstring("Update", "Enter new phone number:", initialvalue=contact[2])
            new_email = simpledialog.askstring("Update", "Enter new email:", initialvalue=contact[3])
            new_address = simpledialog.askstring("Update", "Enter new address:", initialvalue=contact[4])

            c.execute("UPDATE contacts SET phone = ?, email = ?, address = ? WHERE id = ?",
                      (new_phone, new_email, new_address, contact[0]))
            conn.commit()
            messagebox.showinfo("Success", "Contact updated successfully")
        else:
            messagebox.showerror("Error", "Contact not found")

    def delete_contact(self):
        name = simpledialog.askstring("Delete", "Enter the name of the contact to delete:")
        c.execute("DELETE FROM contacts WHERE name = ?", (name,))
        conn.commit()
        if c.rowcount > 0:
            messagebox.showinfo("Success", "Contact deleted successfully")
        else:
            messagebox.showerror("Error", "Contact not found")

    def clear_fields(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")

    def load_contacts(self):
        pass  # Optional: Load contacts on startup if needed

if __name__ == "__main__":
    root = tk.Tk()
    contact_manager = ContactManager(root)
    root.mainloop()

    # Close the database connection when done
    conn.close()
