import tkinter as tk
from tkinter import Label, Button
import mysql.connector

# Function to reset vote counts to 0 in the database
def reset_vote_counts():
    try:
        # Establish MySQL connection
        mysql_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="voter_register"
        )

        cursor = mysql_connection.cursor()

        # Reset vote counts in the database
        cursor.execute("UPDATE party SET vote_count = 0")
        mysql_connection.commit()

        # Retrieve updated data from the party table
        cursor.execute("SELECT party_name, vote_count FROM party")
        party_data = cursor.fetchall()

        # Update the GUI with the new data
        update_gui(party_data)

    except mysql.connector.Error as err:
        # Handle any potential MySQL errors here
        print(f"Error: {err}")

    finally:
        cursor.close()
        mysql_connection.close()

# Function to update the GUI with vote counts
def update_gui(party_data):
    for widget in frame.winfo_children():
        widget.destroy()

    # Increase font size and make column names bold
    column_font = ("Helvetica", 14, "bold")
    Label(frame, text="Party", font=column_font).grid(row=0, column=0, padx=0.04 * window_width, pady=0.02 * window_height, sticky="nsew")
    Label(frame, text="Vote Count", font=column_font).grid(row=0, column=1, padx=0.04 * window_width, pady=0.02 * window_height, sticky="nsew")

    # Increase font size for data
    data_font = ("Helvetica", 15)

    for i, (party_name, count) in enumerate(party_data, start=1):
        Label(frame, text=party_name.capitalize(), font=data_font).grid(row=i, column=0, padx=0.04 * window_width, pady=0.01 * window_height, sticky="nsew")
        Label(frame, text=str(count), font=data_font).grid(row=i, column=1, padx=0.04 * window_width, pady=0.01 * window_height, sticky="nsew")

    # Add a button to reset votes
    reset_button = Button(frame, text="Reset Votes", command=reset_vote_counts)
    reset_button.grid(row=i + 1, column=0, columnspan=2, pady=20)

    # Configure row and column weights to make them expand proportionally
    for r in range(i + 2):
        frame.grid_rowconfigure(r, weight=1)
    for c in range(2):
        frame.grid_columnconfigure(c, weight=1)

# Function to retrieve and display vote counts from the database
def display_vote_counts():
    global frame, window_width, window_height

    root = tk.Tk()
    root.title("Vote Counts")

    # Increase window size
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    frame = tk.Frame(root)
    frame.pack(expand=True, fill='both')

    # Retrieve data from the party table
    mysql_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="voter_register"
    )
    cursor = mysql_connection.cursor()

    try:
        cursor.execute("SELECT party_name, vote_count FROM party")
        party_data = cursor.fetchall()

        # Update the GUI with the initial data
        update_gui(party_data)

    except mysql.connector.Error as err:
        # Handle any potential MySQL errors here
        print(f"Error: {err}")

    finally:
        cursor.close()
        mysql_connection.close()

    root.mainloop()

if __name__ == "__main__":
    display_vote_counts()
