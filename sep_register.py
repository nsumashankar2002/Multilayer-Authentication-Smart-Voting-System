import tkinter as tk
import mysql.connector
from sep_message import MessageWindow
import random
import subprocess

class RegisterWindow:
    def __init__(self, main_window):
        self.main_window = main_window
        self.voter_id = None
        self.aadhar_no = None
        self.pre_register_window = None
        self.otp_window = None
        self.generated_otp = None
        self.entered_voter_id = None
        self.entered_aadhar_no = None
        self.otp_generated = False

        self.label_font = ("Helvetica", 20, "bold")
        self.entry_font = ("Helvetica", 16)

        self.register_new_user()

    def register_new_user(self):
        self.pre_register_window = tk.Toplevel(self.main_window)
        self.pre_register_window.geometry("800x400")
        self.center_window(self.pre_register_window)

        self.voter_id_label = tk.Label(self.pre_register_window, text='Please input Voter ID', font=self.label_font)
        self.voter_id_label.pack(pady=(20, 0))

        self.entry_voter_id = tk.Entry(self.pre_register_window, font=self.entry_font)
        self.entry_voter_id.pack(pady=10)

        self.aadhar_label = tk.Label(self.pre_register_window, text='Please input Aadhar Number', font=self.label_font)
        self.aadhar_label.pack(pady=10)

        self.entry_aadhar = tk.Entry(self.pre_register_window, font=self.entry_font)
        self.entry_aadhar.pack(pady=10)

        self.next_button_pre_register = self.get_button(
            self.pre_register_window, text='Next', color='green', command=self.validate_and_proceed
        )
        self.next_button_pre_register.pack(pady=(10, 0))

        self.entry_voter_id.bind('<Return>', lambda event: self.entry_aadhar.focus_set())
        self.entry_aadhar.bind('<Return>', lambda event: self.validate_and_proceed())

    def validate_and_proceed(self):
        voter_id = self.entry_voter_id.get().strip()
        aadhar_no = self.entry_aadhar.get().replace(" ", "").strip()

        self.entered_voter_id = voter_id
        self.entered_aadhar_no = aadhar_no

        if self.validate_user_data(voter_id, aadhar_no):
            if self.check_user_exists(voter_id, aadhar_no):
                self.pre_register_window.destroy()
                error_message = 'Already Registered! \nProceed to login'
                MessageWindow(self.main_window, error_message)

            else:
                mobile_number = self.retrieve_mobile_number(voter_id, aadhar_no)

                if mobile_number:
                    if not self.otp_generated:
                        self.generated_otp = self.generate_random_otp()
                        print(f"Generated OTP: {self.generated_otp}")
                        self.otp_generated = True

                    print(f"OTP sent to that mobile number: {mobile_number}")

                    self.pre_register_window.destroy()
                    self.show_otp_window()
                else:
                    error_message = 'Mobile Number retrieval failed. Please try again.'
                    MessageWindow(self.main_window, error_message)
        else:
            error_message = 'Invalid Voter ID or Aadhar Number format. Please provide valid details.'
            MessageWindow(self.main_window, error_message)



    def validate_user_data(self, voter_id, aadhar_no):
        if len(voter_id) != 10 or not (voter_id[:3].isalpha() and voter_id[3:].isdigit()):
            return False

        if len(aadhar_no) != 12 or not aadhar_no.isdigit():
            return False

        return True

    def check_user_exists(self, voter_id, aadhar_no):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="voter_register"
            )

            cursor = connection.cursor()

            select_query = "SELECT * FROM users WHERE voter_id = %s AND aadhar_no = %s"
            data = (voter_id, aadhar_no)
            cursor.execute(select_query, data)

            result = cursor.fetchone()

            cursor.close()
            connection.close()

            return result is not None

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return False

    def show_otp_window(self):
        self.otp_window = tk.Toplevel(self.main_window)
        self.otp_window.geometry("600x300")
        self.center_window(self.otp_window)

        self.prompt_otp_label = tk.Label(self.otp_window,
                                         text='Please enter the OTP sent to your Aadhar linked phone number:',
                                         font=self.label_font, wraplength=500)
        self.prompt_otp_label.pack(pady=(20, 0))

        self.otp_label = tk.Label(self.otp_window, text='OTP:', font=self.label_font)
        self.otp_label.pack(pady=10)

        self.entry_otp = tk.Entry(self.otp_window, font=self.entry_font)
        self.entry_otp.pack(pady=(10, 0))

        self.next_button_otp_window = self.get_button(
            self.otp_window, text='Next', color='green', command=self.validate_otp_and_proceed
        )
        self.next_button_otp_window.pack(pady=20)

    def validate_otp_and_proceed(self):
        entered_otp = self.entry_otp.get().strip()

        if entered_otp == self.generated_otp:
            print("OTP validation successful! Proceeding with registration.")
            voter_id = self.entered_voter_id
            aadhar_no = self.entered_aadhar_no

            self.voter_id = voter_id
            self.aadhar_no = aadhar_no

            self.otp_window.destroy()
            self.call_sep_main()

        else:
            error_message = 'Invalid OTP. Please try again.'
            MessageWindow(self.main_window, error_message)

    def call_sep_main(self):
        try:
            subprocess.run(['python', 'sep_main.py', str(self.voter_id), str(self.aadhar_no)])
        except Exception as e:
            print(f"Error calling sep_main.py: {e}")

    def retrieve_mobile_number(self, voter_id, aadhar_no):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="voter_register"
            )

            cursor = connection.cursor()

            select_query = "SELECT phone_no FROM user_data WHERE voter_id = %s AND aadhar_no = %s"
            data = (voter_id, aadhar_no)
            cursor.execute(select_query, data)

            result = cursor.fetchone()

            cursor.close()
            connection.close()

            if result:
                return result[0]
            else:
                return None

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return None

    def generate_random_otp(self):
        return str(random.randint(100000, 999999))

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()

        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

    def get_button(self, parent, text, color, command):
        button = tk.Button(parent, text=text, command=command, font=self.label_font, bg=color, fg="white",
                           width=15, height=2)
        return button


if __name__ == "__main__":
    root = tk.Tk()
    register_window = RegisterWindow(root)
    root.mainloop()
