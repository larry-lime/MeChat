#!/usr/bin/python
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tks
from tkinter.messagebox import showinfo

class classic_GUI:
    def __init__(self):
        # Sets the date variable
        self.gui_done = False
        # Returns a string
        self.nickname = simpledialog.askstring("Nickname", "Enter a nickname:")

    def gui_loop(self):

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
