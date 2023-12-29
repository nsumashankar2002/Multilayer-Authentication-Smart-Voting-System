import tkinter as tk
import threading
from sep_loading import LoadingWindow
from sep_login import create_login_window
from sep_register import RegisterWindow
from util import get_button, get_text_label


class HomePage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1200x520+350+100")
        self.root.title("Home Page")

        self.home_label = get_text_label(self.root, "Welcome to Online Voting System App")
        self.home_label.pack(side=tk.TOP, pady=20)

        self.login_button = get_button(self.root, "Login", "green", self.login)
        self.login_button.pack(side=tk.TOP, pady=20)

        self.register_button = get_button(self.root, "Register", "gray", self.register)
        self.register_button.pack(side=tk.TOP, pady=20)

        # Center the buttons horizontally and vertically
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # def run_main_script(self):
    #     # Show loading window
    #     loading_window = LoadingWindow(self.root)
    #     loading_window.update_idletasks()
    #
    #     # Run the main script in a separate thread
    #     threading.Thread(target=self.run_main_script_thread, args=(loading_window, self)).start()
    #
    # def run_main_script_thread(self, loading_window, main_instance):
    #     # Run the main script
    #     subprocess.run(["python", "main.py"])
    #
    #     # Wait for the main GUI window to close
    #     self.root.wait_window(main_instance.root)
    #
    #     # Destroy the loading window after the main GUI window is closed
    #     loading_window.destroy()

    def login(self):
        login_window = create_login_window(self.root)

    def register(self):
        register_window = RegisterWindow(self.root)

    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    home_page = HomePage()
    home_page.start()
