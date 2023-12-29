import tkinter as tk
import mysql.connector
from sep_message import MessageWindow  # Assuming MessageWindow is available in your code
from util import msg_box, get_button

class RegisterWindow:
    def __init__(self, main_window):
        self.main_window = main_window
        self.registration_successful = False  # Flag to track successful registration

        # Define fonts
        self.label_font = ("Helvetica", 20, "bold")
        self.entry_font = ("Helvetica", 16)

        # Create the 'user_data' table in MySQL database
        self.create_table()

        self.create_register_window()

    def create_table(self):
        # Connect to MySQL database
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="voter_register"
            )

            cursor = connection.cursor()

            # Create user_data table
            create_table_query = """
                CREATE TABLE IF NOT EXISTS user_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    voter_id VARCHAR(10) UNIQUE NOT NULL,
                    aadhar_no VARCHAR(12) UNIQUE NOT NULL,
                    phone_no VARCHAR(15) UNIQUE NOT NULL
                )
            """
            cursor.execute(create_table_query)

            # Commit changes and close connection
            connection.commit()
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def create_register_window(self):
        # Label and Entry for Voter ID
        self.voter_id_label = tk.Label(self.main_window, text='Please input Voter ID', font=self.label_font)
        self.voter_id_label.pack(pady=(20, 0))

        self.entry_voter_id = tk.Entry(self.main_window, font=self.entry_font)
        self.entry_voter_id.pack(pady=10)

        # Label and Entry for Aadhar Number
        self.aadhar_label = tk.Label(self.main_window, text='Please input Aadhar Number', font=self.label_font)
        self.aadhar_label.pack(pady=10)

        self.entry_aadhar = tk.Entry(self.main_window, font=self.entry_font)
        self.entry_aadhar.pack(pady=10)

        # Label and Entry for Phone Number
        self.phone_label = tk.Label(self.main_window, text='Please input Phone Number', font=self.label_font)
        self.phone_label.pack(pady=10)

        self.entry_phone = tk.Entry(self.main_window, font=self.entry_font)
        self.entry_phone.pack(pady=10)

        self.next_button_register = get_button(
            self.main_window, text='Register', color='green', command=self.register_user
        )
        self.next_button_register.pack(pady=(10, 0))

    def register_user(self):
        voter_id = self.entry_voter_id.get().strip()
        aadhar_no = self.entry_aadhar.get().strip()
        phone_no = self.entry_phone.get().strip()

        # Validate all inputs
        validation_result, error_message = self.validate_inputs(voter_id, aadhar_no, phone_no)

        if not validation_result:
            msg_box('Error!', error_message)
            return

        # Add your validation logic here
        if voter_id and aadhar_no and phone_no:
            success = self.save_user_data(voter_id, aadhar_no, phone_no)
            if success:
                self.registration_successful = True
                self.clear_input_fields()  # Set the flag to True

                # Display the success message only if registration was successful
                if self.registration_successful:
                    message = "Registration successful!"
                    MessageWindow(self.main_window, message)
            else:
                error_message = 'Duplicate entry: Voter ID already registered.'
                MessageWindow(self.main_window, error_message)
        else:
            msg_box('Error!', 'Please provide all the details.')

    def clear_input_fields(self):
        # Clear input fields
        self.entry_voter_id.delete(0, tk.END)
        self.entry_aadhar.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)

    def validate_inputs(self, voter_id, aadhar_no, phone_no):
        # Validate Voter ID format
        if not self.validate_voter_id(voter_id):
            return False, 'Invalid Voter ID format. Please provide a valid Voter ID.'

        # Validate Aadhar number length
        if len(aadhar_no) != 12:
            return False, 'Invalid Aadhar number length. Please provide a valid 12-digit Aadhar number.'

        # Validate Phone number length
        if len(phone_no) != 10:
            return False, 'Invalid Phone number length. Please provide a valid 10-digit phone number.'

        # Additional validation logic can be added here

        return True, ''

    def validate_voter_id(self, voter_id):
        # Validate that the Voter ID contains 10 alphanumeric values
        if len(voter_id) != 10:
            return False

        # Validate the format of the first 3 characters (alphabets) and the next 7 characters (numbers)
        if not (voter_id[:3].isalpha() and voter_id[3:].isdigit()):
            return False

        return True

    def save_user_data(self, voter_id, aadhar_no, phone_no):
        # Connect to MySQL database
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="voter_register"
            )

            cursor = connection.cursor()

            # Insert user data into the database
            insert_query = "INSERT INTO user_data (voter_id, aadhar_no, phone_no) VALUES (%s, %s, %s)"
            data = (voter_id, aadhar_no, phone_no)
            cursor.execute(insert_query, data)

            # Commit changes and close connection
            connection.commit()
            cursor.close()
            connection.close()

            return True

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return False

    def center_window(self):
        self.main_window.update_idletasks()
        width = self.main_window.winfo_width()
        height = self.main_window.winfo_height()

        x = (self.main_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.main_window.winfo_screenheight() // 2) - (height // 2)

        self.main_window.geometry(f"{width}x{height}+{x}+{y}")
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")
    register_window = RegisterWindow(root)
    register_window.center_window()
    root.mainloop()
