import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

# # root window
# root = tk.Tk()
# root.geometry("300x150")
# root.resizable(False, False)
# root.title('Sign In')

# # store email address and password
# email = tk.StringVar()
# password = tk.StringVar()


# def login_clicked():
    # """ callback when the login button clicked
    # """
    # msg = f'You entered email: {email.get()} and password: {password.get()}'
    # showinfo(
        # title='Information',
        # message=msg
    # )


# # Sign in frame
# signin = ttk.Frame(root)
# signin.pack(
    # padx=10,
    # pady=10,
    # fill='x',
    # expand=True
# )

# # email
# email_label = ttk.Label(
    # signin,
    # text="Email Address:"
# )
# email_label.pack(
    # fill='x',
    # expand=True)

# email_entry = ttk.Entry(
    # signin,
    # textvariable=email
# )
# email_entry.pack(fill='x',
                 # expand=True
                 # )
# email_entry.focus()

# # password
# password_label = ttk.Label(signin, text="Password:")
# password_label.pack(fill='x', expand=True)

# password_entry = ttk.Entry(signin, textvariable=password, show="*")
# password_entry.pack(fill='x', expand=True)

# # login button
# login_button = ttk.Button(signin, text="Login", command=login_clicked)
# login_button.pack(fill='x', expand=True, pady=10)


# root.mainloop()

class modern_GUI:
    def __init__(self):
        pass

    def gui_loop(self):

        # Tkinter Window
        self.root = tk.Tk()
        self.root.geometry("600x300")
        self.root.resizable(False, False)
        self.root.title("Modern GUI Demo")

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
        self.msg_label = ttk.Label(
            self.root,
            text="Username:"
        )
        self.msg_label.pack(
            fill='x',
            expand=True)

        self.user_box = ttk.Entry(
            self.root,
            textvariable=self.username
        )
        self.user_box.pack(
            fill='x',
            expand=True
        )

        # Password Input
        self.msg_label = ttk.Label(
            self.root,
            text="Password: "
        )
        self.msg_label.pack(fill='x', expand=True)

        self.pass_box = ttk.Entry(
            self.root,
            textvariable=self.password,
            show="*")
        self.pass_box.pack(fill='x',expand=True)

        # Tkinter Button 
        button_icon = tk.PhotoImage(file='./assets/send_icon_small.png')
        self.button = ttk.Button(
            self.root,
            image=button_icon,
            text="BUTTON",
            # style="TButton",
            compound=tk.RIGHT,
            command=self.login_clicked)

        self.button.pack(fill='x', expand=True, pady=10)

        try:
            from ctypes import windll

            windll.shcore.SetProcessDpiAwareness(1)

        finally:
            self.root.mainloop()

    def login_clicked(self):
        msg = f'You entered email: {self.username.get()} and password: {self.password.get()}'
        showinfo(
            title='Information',
            message=msg
        )
    def write(self):
        pass
        # self.sock.send(message.encode('utf-8'))
        # self.input_area.delete('1.0', 'end')

    # This kills the GUI window when I press the X button
    def stop(self):
        self.running = False
        self.root.destroy()
        exit(0)

if __name__ == "__main__":
    # gui = classic_GUI()
    # gui.gui_loop()
    gui = modern_GUI()
    gui.gui_loop()
    print("GUI closed")

