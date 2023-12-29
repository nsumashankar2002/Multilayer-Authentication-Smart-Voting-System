import os.path
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
import pickle
import mysql.connector
from mysql.connector import Error
import util
from util import get_button

import sys

class App:
    def get_entry_text(self, master):
        entry = tk.Entry(master, font=self.entry_font)
        return entry

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='voter_register',
                user='root',
                password='root'
            )
            if connection.is_connected():
                print("Connected to MySQL database")
                return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def open_register_new_user_window(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")
        screen_width = self.register_new_user_window.winfo_screenwidth()
        screen_height = self.register_new_user_window.winfo_screenheight()

        # Calculate the x and y coordinates for the Tk root window
        x = (screen_width - 1200) // 2
        y = (screen_height - 520) // 2

        # Set the geometry of the main window to center it on the screen
        self.register_new_user_window.geometry(f"1200x520+{x}+{y}")

        self.capture_label = tk.Label(self.register_new_user_window)
        self.capture_label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        label_frame = tk.Frame(self.register_new_user_window)
        label_frame.pack(side=tk.RIGHT, anchor=tk.W, padx=10, pady=10)

        self.text_label_register_new_user = tk.Label(
            label_frame, text='Please input username:', font=self.label_font
        )
        self.text_label_register_new_user.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=(10, 0))

        self.entry_text_username = self.get_entry_text(label_frame)
        self.entry_text_username.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=(0, 10))

        self.text_label_password = tk.Label(
            label_frame, text='Please input password', font=self.label_font
        )
        self.text_label_password.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=(10, 0))

        self.entry_text_password = self.get_entry_text(label_frame)
        self.entry_text_password.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=(0, 10))

        self.accept_button_register_new_user_window = get_button(
            label_frame, text='Accept', color='blue', command=self.accept_register_new_user
        )
        self.accept_button_register_new_user_window.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=(30, 5))

        self.try_again_button_register_new_user_window = get_button(
            label_frame, text='Try again', color='red', command=self.try_again_register_new_user
        )
        self.try_again_button_register_new_user_window.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=(5, 30))

        self.add_img_to_label(self.capture_label)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def accept_register_new_user(self):
        name = self.entry_text_username.get().strip()
        password = self.entry_text_password.get()

        if name and password:
            face_encodings = face_recognition.face_encodings(self.register_new_user_capture)

            if face_encodings:
                embeddings = face_encodings[0]

                # Store user data in MySQL
                self.store_user_in_mysql(name, password, embeddings)

                util.msg_box('Success!', 'User was registered successfully!')
                self.register_new_user_window.destroy()
                self.main_window.destroy()
            else:
                util.msg_box('Error!', 'No face found in the captured image. Please try again.')
        else:
            util.msg_box('Error!', 'Please provide both username and password.')

    def store_user_in_mysql(self, name, password, embeddings):
        try:
            cursor = self.db_connection.cursor()

            voter_id = sys.argv[1]
            aadhar_no = sys.argv[2]

            # Create table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    voter_id VARCHAR(10) UNIQUE NOT NULL,
                    aadhar_no VARCHAR(12) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    pickle_path VARCHAR(255) NOT NULL
                )
            ''')

            # Save the embeddings as a pickle file
            pickle_filename = f"{name}.pickle"
            pickle_path = os.path.join(self.db_dir, pickle_filename)
            with open(pickle_path, 'wb') as file:
                pickle.dump(embeddings, file)

            # Insert user data
            cursor.execute('''
                INSERT INTO users (voter_id, aadhar_no, name, password, pickle_path) VALUES (%s, %s, %s, %s, %s)
            ''', (voter_id, aadhar_no, name, password, pickle_path))

            self.db_connection.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def start(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()

        # Calculate the x and y coordinates for the Tk root window
        x = (screen_width - 1200) // 2
        y = (screen_height - 520) // 2

        # Set the geometry of the main window to center it on the screen
        self.main_window.geometry(f"1200x520+{x}+{y}")

        self.label_font = ("Helvetica", 20, "bold")
        self.entry_font = ("Helvetica", 16)

        self.db_dir = r'C:\Users\shash\Desktop\5th sem\face-attendance-system-master3\db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

        self.db_connection = self.connect_to_database()

        self.register_new_user_button_main_window = get_button(
            self.main_window, text='Register New User', color='green', command=self.open_register_new_user_window
        )
        self.register_new_user_button_main_window.pack(side=tk.RIGHT, padx=10, pady=10)

        self.webcam_label = tk.Label(self.main_window, font=self.label_font)
        self.webcam_label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.add_webcam(self.webcam_label)

        self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()
