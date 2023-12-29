import tkinter as tk
from tkinter import Radiobutton, StringVar, Label, messagebox, Button
from PIL import ImageTk, Image
import mysql.connector

# Initialize vote counts and total voters
votes_count = {party.lower(): 0 for party, _ in [
    ("Aam Aadmi Party", r"C:\Users\shash\Desktop\5th sem\face-attendance-system-master3\img\aap.png"),
    ("BJP", r"C:\Users\shash\Desktop\5th sem\face-attendance-system-master3\img\bjp.png"),
    ("Congress",
     r"C:\Users\shash\Desktop\5th sem\face-attendance-system-master3\img\cong.png"),
    ("NOTA", r"C:\Users\shash\Desktop\5th sem\face-attendance-system-master3\img\nota.png"),
    ("Shiv Sena", r"C:\Users\shash\Desktop\5th sem\face-attendance-system-master3\img\ss.png")
]}

total_voters = 0
vote = None

# Initialize MySQL connection
mysql_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="voter_register"
)

def load_votes_count():
    # Load the initial vote counts from the database
    global votes_count
    cursor = mysql_connection.cursor()
    cursor.execute("SELECT party_name, vote_count FROM party")
    result = cursor.fetchall()
    for party_name, count in result:
        votes_count[party_name.lower()] = count

def save_votes():
    # Save the updated votes to the MySQL database
    cursor = mysql_connection.cursor()

    for party_name, count in votes_count.items():
        update_query = f"UPDATE party SET vote_count = {count} WHERE party_name = '{party_name}'"
        cursor.execute(update_query)

    # Commit the changes to the database
    mysql_connection.commit()

def vote_cast(frame1, party_name):
    global total_voters
    for widget in frame1.winfo_children():
        widget.destroy()

    # Simulating server interaction (replace with actual logic)
    # Since there is no actual server, we'll just simulate success
    message = "Successful"

    if message == "Successful":
        Label(frame1, text="Vote Casted Successfully", font=('Helvetica', 18, 'bold')).grid(row=1, column=1)
        ok_button = Button(frame1, text="OK", command=lambda: root.destroy(), bg="blue", fg="white", width=12, height=1,
                           font=("Helvetica", 12, "bold"))
        ok_button.grid(row=2, column=0, columnspan=2, pady=(40, 20))

        # Convert party_name to lowercase before updating the count
        party_name_lower = party_name.lower()

        # Update the vote count for the selected party
        votes_count[party_name_lower] += 1

        # Save the updated votes to the party table
        save_votes()
    else:
        Label(frame1, text="Vote Cast Failed... \nTry again", font=('Helvetica', 18, 'bold')).grid(row=1, column=1)

def confirm_vote(frame1, vote):
    party_name = vote.get()
    confirmation = messagebox.askyesno("Confirm Vote", f"Are you sure you want to vote for {party_name.capitalize()}?")
    if confirmation:
        vote_cast(frame1, vote.get())

def voting_page(frame1):
    global votes_count, vote, root
    root.title("Cast Vote")
    for widget in frame1.winfo_children():
        widget.destroy()

    Label(frame1, text="Cast Vote", font=('Helvetica', 18, 'bold')).grid(row=0, column=1, rowspan=1)
    Label(frame1, text="").grid(row=1, column=0)

    vote = StringVar(frame1, "-1")  # Initialize vote here

    # List to store PhotoImage objects
    image_list = []

    def create_button(row_num, party_name, image_path):
        Radiobutton(frame1, text=party_name, variable=vote, value=party_name.lower(),
                    indicator=0, height=4, width=15).grid(row=row_num, column=1)

        # Create PhotoImage object and store it in the list
        logo = ImageTk.PhotoImage((Image.open(image_path)).resize((45, 45), Image.LANCZOS))
        image_list.append(logo)

        Label(frame1, image=logo).grid(row=row_num, column=0)

    # Load initial vote counts from the database
    load_votes_count()

    party_info = [
    ("Aam Aadmi Party", r"C:\Users\shash\Desktop\5th sem\face-attendance-system-master3\img\aap.png"),
    ("BJP", r"C:\Users\shash\Desktop\5th sem\face-attendance-system-master3\img\bjp.png"),
    ("Congress",
     r"C:\Users\shash\Desktop\5th sem\face-attendance-system-master3\img\cong.png"),
    ("NOTA", r"C:\Users\shash\Desktop\5th sem\face-attendance-system-master3\img\nota.png"),
    ("Shiv Sena", r"C:\Users\shash\Desktop\5th sem\face-attendance-system-master3\img\ss.png")
    ]

    for i, (party_name, image_path) in enumerate(party_info, start=2):
        create_button(i, party_name, image_path)

    confirm_button = tk.Button(frame1, text="Confirm Vote", command=lambda: confirm_vote(frame1, vote), bg="green")
    confirm_button.grid(row=len(party_info) + 2, column=1, pady=10)

    frame1.pack()
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Voting System")

    # Calculate the window position for centering
    window_width = 500
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    frame1 = tk.Frame(root)
    voting_page(frame1)
    root.mainloop()

