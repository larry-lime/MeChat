#!/usr/bin/python
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tks
# from tkinter.messagebox import showinfo
from tkinter import simpledialog

class classic_GUI:
    def __init__(self):
        # Sets the date variable
        self.gui_done = False
        # Returns a string
        self.nickname = simpledialog.askstring("Nickname", "Enter a nickname:")

    def gui_login(self):

        # sets the state variable
        self.running = True
        # Starts the tkinter window
        self.win = tk.Tk()
        # Sets the background to be light gray
        self.win.configure(bg="lightgray")

        self.chat_label = tk.Label(self.win, text="Chat", bg="lightgray")
        self.chat_label.configure(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tks.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tk.Label(self.win, text="Message", bg="lightgray")
        self.msg_label.configure(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tk.Text(self.win, height=3, width=30)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tk.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', tk.END)}"
        print(message)
        # Right here is when I need to send the message to the server
        # self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    # This kills the GUI window when I press the X button
    def stop(self):
        self.running = False
        self.win.destroy()
        exit(0)

    def recieve(self):
        while self.running:
            try: 
                # message = self.sock.recv(1024)
                message = "test"
                if message == "NICK":
                    # self.sock.send(self.nickname.encode('utf-8'))
                    pass
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except:
                break

class modern_GUI:
    def __init__(self):
        self.username = ""
        self.running = True
        self.gui_done = False

    def gui_login(self):

        # Tkinter Window
        self.root = tk.Tk()
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        self.root.title("Chat Login")

        # Login String Variables
        self.username = tk.StringVar()

        # Sign in frame
        self.signin = ttk.Frame(self.root)
        self.signin.pack(
            padx=15,
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

        self.user_box.bind('<Return>', self.login_bind)

        self.user_box.focus()

        # Login Button
        self.button = ttk.Button(
            self.signin,
            text="Login",
            command=self.login_action
        )

        self.button.pack(fill='x', expand=True, pady=10)

        self.root.mainloop()

    def gui_chat(self):

        # Tkinter Window
        self.root = tk.Tk()
        self.root.geometry("300x600")
        self.root.resizable(False, False)
        self.root.title("Chat Windows")

        # Chat String Variables
        self.msg = tk.StringVar()

        # Sign in frame
        self.signin = ttk.Frame(self.root)
        self.signin.pack(
            padx=15,
            pady=10,
            fill='x',
            expand=True
        )

        self.user_label = ttk.Label(
            self.signin,
            text="Chat Window")

        self.user_label.pack(
            fill='x',
            # ipadx=20,
            # ipady=20,
            expand=True)

        # Chat Window
        self.text_area = tks.ScrolledText(self.signin)
        self.text_area.pack(
            fill='x',
            # padx=20,
            pady=5
        )
        self.text_area.config(state='disabled')

        # Message Box
        self.user_box = ttk.Entry(
            self.signin,
            textvariable=self.msg)
        self.user_box.pack(
            fill='x',
            expand=True)

        self.user_box.bind('<Return>', self.write_bind)

        self.user_box.focus()

        # Tkinter Button 
        button_icon = tk.PhotoImage(file='./assets/send_icon_smaller.png')
        self.button = ttk.Button(
            self.signin,
            image=button_icon,
            text="SEND",
            compound=tk.RIGHT,
            command=self.write)

        self.button.pack(fill='x', expand=True, pady=10)

        self.root.mainloop()

    def login_bind(self, event):
        self.login_action()

    def login_action(self):
        self.username = self.user_box.get()
        self.root.destroy()
    
    def write_bind(self, event):
        self.write()

    def write(self):
        """
        This is where I need to send the message to the server
        Comment out the insert code when I implement it
        """
        self.message = f"{self.username}: {self.msg.get()}\n"
        # self.text_area.insert('end', self.message)
        # self.text_area.yview('end')
        self.user_box.delete(0, 'end')

    def recieve(self):
        self.text_area.config(state='normal')
        self.text_area.insert('end', self.message)
        self.text_area.yview('end')
        self.text_area.config(state='disabled')

if __name__ == "__main__":
    # gui = classic_GUI()
    # gui.gui_login()
    gui = modern_GUI()
    gui.gui_login()
    gui.gui_chat()
    print("GUI closed")
