import tkinter as tk

class MessageWindow(tk.Toplevel):
    def __init__(self, root, message):
        super().__init__(root)
        self.title("Message")

        frame = tk.Frame(self)
        frame.pack(expand=True, pady=20)

        label = tk.Label(frame, text=message, font=("Helvetica", 16), wraplength=250, anchor="w")
        label.pack(expand=True, fill='both', padx=10, pady=10)

        ok_button = tk.Button(self, text="OK", command=self.destroy, width=8, height=1)
        ok_button.pack(pady=(10, 20))  # Adjusted pady values

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()

        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    msg = "This is a message. Click OK to close."
    MessageWindow(root, msg)
    root.mainloop()
