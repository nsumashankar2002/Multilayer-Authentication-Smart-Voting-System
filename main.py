import os.path
import datetime
import subprocess

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import util

import sys
sys.path.insert(0, '/Users/vichursatish/Downloads/Multilayer-Authentication-Smart-Voting-System-main/Silent-Face-Anti-Spoofing')
import test
from test import test


class App:


    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.wm_attributes("-topmost", 1)

        ###
        # Set the window size and position it in the center of the screen
        window_width = 1200
        window_height = 520
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.main_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        ###
        self.login_button_main_window = util.get_button(self.main_window, 'Verify and Cast', 'green', self.login)
        self.login_button_main_window.place(x=750, y=300)





        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

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

    def login(self):

        label = test(
                image=self.most_recent_capture_arr,
                model_dir=r'/Users/vichursatish/Downloads/Multilayer-Authentication-Smart-Voting-System-main/Silent-Face-Anti-Spoofing/resources/anti_spoof_models',
                device_id=0
                )

        if label == 1:

            name = util.recognize(self.most_recent_capture_arr, self.db_dir)

            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
            else:
                util.msg_box('Welcome back !', 'Welcome, {}.'.format(name))
                self.main_window.attributes('-topmost', 0)
                with open(self.log_path, 'a') as f:
                    f.write('{},{},in\n'.format(name, datetime.datetime.now()))
                    f.close()
                subprocess.run(['python', 'VotingPage.py', '--name', name])
                self.main_window.destroy()

        else:
            util.msg_box('Hey, you are a spoofer!', 'You are fake !')

    def cast_vote(self):
        self.recognized_face_window.destroy()
        util.msg_box('Success!', 'You have successfully voted!')

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()



if __name__ == "__main__":
    app = App()
    app.start()

