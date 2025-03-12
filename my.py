import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def connect_db():
    try:
        return mysql.connector.connect(host="localhost", user="root", password="dharshini@12345", database="amusement_db")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def save_to_db(name, contact, ride, date, tickets, total_cost):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO bookings (name, contact, ride, date, tickets, total_cost) VALUES (%s, %s, %s, %s, %s, %s)",
                           (name, contact, ride, date, tickets, total_cost))
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            conn.close()

def next_page(current, next_frame):
    current.pack_forget()
    next_frame.pack(pady=20)

def prev_page(current, prev_frame):
    current.pack_forget()
    prev_frame.pack(pady=20)

def calculate_total():
    try:
        num_tickets = int(tickets_var.get())
        total_cost = num_tickets * ticket_price
        total_label.config(text=f"Total Cost: ${total_cost:.2f}")
    except ValueError:
        total_label.config(text="Total Cost: $0.00")

def submit_details():
    name, contact, ride, date, tickets = name_var.get(), contact_var.get(), ride_var.get(), date_var.get(), tickets_var.get()
    total_cost = int(tickets) * ticket_price
    details_table.insert("", tk.END, values=(name, contact, ride, date, tickets, f"${total_cost:.2f}"))
    save_to_db(name, contact, ride, date, tickets, total_cost)
    messagebox.showinfo("Success", "Booking Successful!")
    reset_fields()

def reset_fields():
    name_var.set("")
    contact_var.set("")
    ride_var.set("")
    date_var.set("")
    tickets_var.set("1")
    total_label.config(text="Total Cost: $0.00")

def increment():
    current_value = int(tickets_var.get())
    tickets_var.set(str(current_value + 1))
    calculate_total()

def decrement():
    current_value = int(tickets_var.get())
    if current_value > 1:
        tickets_var.set(str(current_value - 1))
        calculate_total()

root = tk.Tk()
root.title("Amusement Park Booking System")
root.geometry("500x450")
root.configure(bg="lightblue")

# Variables
name_var = tk.StringVar()
contact_var = tk.StringVar()
ride_var = tk.StringVar()
date_var = tk.StringVar()
tickets_var = tk.StringVar(value="1")
ticket_price = 30  # Fixed price per ticket

rides = ["Roller Coaster", "Ferris Wheel", "Water Slide", "Bumper Cars"]

# Page 1 - Name Entry
page1 = tk.Frame(root, bg="lightblue")
tk.Label(page1, text="Enter Your Name:", bg="lightblue").pack()
tk.Entry(page1, textvariable=name_var).pack()
tk.Button(page1, text="Next", command=lambda: next_page(page1, page2)).pack()

# Page 2 - Contact Entry
page2 = tk.Frame(root, bg="lightblue")
tk.Label(page2, text="Enter Contact Number:", bg="lightblue").pack()
tk.Entry(page2, textvariable=contact_var).pack()
tk.Button(page2, text="Next", command=lambda: next_page(page2, page3)).pack()
tk.Button(page2, text="Back", command=lambda: prev_page(page2, page1)).pack()

# Page 3 - Ride Selection & Ticketing
page3 = tk.Frame(root, bg="lightblue")
tk.Label(page3, text="Select Ride:", bg="lightblue").pack()
ttk.Combobox(page3, textvariable=ride_var, values=rides).pack()
tk.Label(page3, text="Enter Visit Date:", bg="lightblue").pack()
tk.Entry(page3, textvariable=date_var).pack()

tk.Label(page3, text="Number of Tickets:", bg="lightblue").pack()
ticket_frame = tk.Frame(page3, bg="lightblue")
tk.Button(ticket_frame, text="-", command=decrement).pack(side=tk.LEFT)
tk.Entry(ticket_frame, textvariable=tickets_var, width=5, justify='center').pack(side=tk.LEFT)
tk.Button(ticket_frame, text="+", command=increment).pack(side=tk.LEFT)
ticket_frame.pack()

# Display Total Cost
total_label = tk.Label(page3, text="Total Cost: $0.00", bg="lightblue")
total_label.pack()

tk.Button(page3, text="Next", command=lambda: next_page(page3, page4)).pack()
tk.Button(page3, text="Back", command=lambda: prev_page(page3, page2)).pack()

# Page 4 - Summary Table
page4 = tk.Frame(root, bg="lightblue")
tk.Label(page4, text="Booking Details", bg="lightblue").pack()
details_table = ttk.Treeview(page4, columns=("Name", "Contact", "Ride", "Date", "Tickets", "Total Cost"), show="headings")
details_table.heading("Name", text="Name")
details_table.heading("Contact", text="Contact")
details_table.heading("Ride", text="Ride")
details_table.heading("Date", text="Date")
details_table.heading("Tickets", text="Tickets")
details_table.heading("Total Cost", text="Total Cost")
details_table.pack()
tk.Button(page4, text="Submit", command=submit_details).pack()
tk.Button(page4, text="Back", command=lambda: prev_page(page4, page3)).pack()

# Start with Page 1
page1.pack(pady=20)
root.mainloop()
