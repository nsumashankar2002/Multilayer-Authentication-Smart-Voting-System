import tkinter as tk
import mysql.connector
from sep_message import MessageWindow
import subprocess

def create_login_window(root):
    login_window = tk.Toplevel(root)
    login_window.geometry("500x400")
    login_window.title("Login")

    # Font configuration for the labels and input fields
    label_font = ("Helvetica", 20, "bold")
    entry_font = ("Helvetica", 16)

    username_label = tk.Label(login_window, text="Username:", font=label_font)
    username_label.pack(pady=(20, 0))
    username_entry = tk.Entry(login_window, font=entry_font)
    username_entry.pack(pady=5)

    password_label = tk.Label(login_window, text="Password:", font=label_font)
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_window, show="*", font=entry_font)
    password_entry.pack(pady=10)

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="voter_register"
        )

        cursor = connection.cursor()

        # Create voted_users table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS voted_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            voted INT NOT NULL DEFAULT 0
        )
        """
        cursor.execute(create_table_query)
        connection.commit()

        def login():
            entered_username = username_entry.get()
            entered_password = password_entry.get()

            try:
                cursor = connection.cursor()

                # Authenticate user
                login_query = "SELECT * FROM users WHERE name = %s AND password = %s"
                cursor.execute(login_query, (entered_username, entered_password))
                result = cursor.fetchone()

                if result:
                    # Check if the user has already voted
                    check_vote_query = "SELECT voted FROM voted_users WHERE name = %s"
                    cursor.execute(check_vote_query, (entered_username,))
                    voted_status = cursor.fetchone()

                    if voted_status and voted_status[0] == 1:
                        message = "You have already casted your vote.\n Multiple voting is not allowed."
                    else:
                        # Update the voted status for the user in voted_users table
                        insert_vote_query = "INSERT INTO voted_users (name, voted) VALUES (%s, %s)"
                        cursor.execute(insert_vote_query, (entered_username, 1))
                        connection.commit()

                        login_window.destroy()
                        message = "Login successful! You can now cast your vote."
                        MessageWindow(root, message)
                        subprocess.Popen(["python", "main.py"])

                        # Use after_idle to bring focus to the main window without delay
                        root.after_idle(lambda: root.focus_force())
                else:
                    message = "Invalid username or password. Please try again."

                cursor.close()

            except Exception as e:
                message = f"Error connecting to the database: {e}"

            if login_window.winfo_exists():
                MessageWindow(login_window, message)

        login_button = tk.Button(login_window, text="Login", command=login, bg="green", fg="white", width=12, height=1,
                                font=("Helvetica", 12, "bold"))
        login_button.pack(pady=(5, 0))

        # Center the login window
        login_window.update_idletasks()
        width = login_window.winfo_width()
        height = login_window.winfo_height()

        x = (login_window.winfo_screenwidth() // 2) - (width // 2)
        y = (login_window.winfo_screenheight() // 2) - (height // 2)

        login_window.geometry(f"{width}x{height}+{x}+{y}")

    except Exception as e:
        message = f"Error connecting to the database: {e}"
        MessageWindow(login_window, message)

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    create_login_window(root)
    root.mainloop()
