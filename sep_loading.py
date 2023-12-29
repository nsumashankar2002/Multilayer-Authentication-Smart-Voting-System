import tkinter as tk

class LoadingWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Loading")
        self.geometry(root.geometry())

        self.label = tk.Label(self, text="Loading, please wait", font=("Helvetica", 26))
        self.label.pack(expand=True)

        self.num_dots = 3
        self.animate_loading()

    def animate_loading(self):
        dots = "." * self.num_dots
        self.label.config(text=f"Loading, please wait{dots}")

        self.num_dots = (self.num_dots + 1) % 5

        self.after(500, self.animate_loading)
