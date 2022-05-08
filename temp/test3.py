import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

class modern_GUI:
    def __init__(self) -> None:
        pass

    def gui_loop(self):

        # root window
        self.root = tk.Tk()
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        self.root.title('Sign In')

        # Login Frame
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # Congifure Styles
        # self.style = ttk.Style()
        # self.style.configure("Label", font=("Arial", 15))
        # self.style = ttk.Style()
        # self.style.configure("TButton", font=("Arial", 15))

        # Sign in frame
        self.signin = ttk.Frame(self.root)
        self.signin.pack(
            padx=10,
            pady=10,
            fill='x',
            expand=True
        )

        # Username
        self.user_label = ttk.Label(
            self.signin,
            text="Username:")
        self.user_label.pack(
            fill='x',
            expand=True)

        self.user_box = ttk.Entry(
            self.signin,
            textvariable=self.username)
        self.user_box.pack(
            fill='x',
             expand=True)

        self.user_box.focus()

        # self.password
        self.pass_label = ttk.Label(
            self.signin,
            text="Password:")
        self.pass_label.pack(fill='x', expand=True)

        self.pass_box = ttk.Entry(self.signin, textvariable=self.password, show="*")
        self.pass_box.pack(fill='x', expand=True)

        # login button
        self.button = ttk.Button(
            self.signin,
            text="Login",
            command=self.login_clicked)
        self.button.pack(fill='x', expand=True, pady=10)

        # try:
            # from ctypes import windll

            # windll.shcore.SetProcessDpiAwareness(1)

        # finally:
            # self.root.mainloop()
        self.root.mainloop()

    def login_clicked(self):
        msg = f'You entered username: {self.username.get()} and self.password: {self.password.get()}'
        showinfo(
            title='Information',
            message=msg
        )

if __name__ == "__main__":
    # gui = classic_GUI()
    # gui.gui_loop()
    gui = modern_GUI()
    gui.gui_loop()
    print("GUI closed")
    pass

