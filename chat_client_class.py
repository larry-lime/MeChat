import socket
import time
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm
import threading
import time
# GUI Imports
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tks
from tkinter.messagebox import showerror, showwarning, showinfo


class Client:
    def __init__(self, args):
        # This is the user of the system
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args
        # GUI Vars
        self.running = False
        self.trigger = False
        self.login_status = False
        self.chat_start = True

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_trigger(self):
        return self.trigger

    def set_trigger(self, arg):
        self.trigger = arg

    def get_name(self):
        return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        # self.socket.connect(svr)
        self.socket.connect(('0.tcp.jp.ngrok.io', 18632))
        self.sm = csm.ClientSM(self.socket)
        reading_thread = threading.Thread(target=self.gui_loop)
        reading_thread.daemon = True
        reading_thread.start()

    def shutdown_chat(self):
        self.running = False
        return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def get_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = self.console_input.pop(0) if len(
            self.console_input) > 0 else ''
        peer_msg = self.recv() if self.socket in read else []
        return my_msg, peer_msg

    def login(self):
        my_msg, peer_msg = self.get_msgs()
        if len(my_msg) <= 0:
            return(False)
        # print(my_msg)
        login_info = my_msg.split('\n')
        self.name = login_info[0]
        self.pswrd = login_info[1]
        msg = json.dumps(
            {"action": "login", "name": self.name, "password": self.pswrd})
        self.send(msg)
        response = json.loads(self.recv())
        if response["status"] == 'ok':
            return self.logged_in()
        elif response["status"] == 'duplicate':
            return self.login_error('DUPL')
        elif response["status"] == 'wrong':
            return self.login_error('WRONG')

    def logged_in(self):
        self.trigger = True
        self.login_status = True
        self.state = S_LOGGEDIN
        self.sm.set_state(S_LOGGEDIN)
        self.sm.set_myname(self.name)
        return (True)

    def login_error(self, error):
        self.trigger = True
        self.login_status = error
        return False

    def gui_login(self):

        # Error detection
        if self.login_status == 'DUPL':
            self.display_error('Duplicate Username',
                               'Try logging in again with another username')

        elif self.login_status == 'WRONG':
            self.display_error('Incorrect Login', 'Wrong username or password')

        self.login_root = self.new_tk_window("300x150", "User Login")
        # Login String Variables
        username = tk.StringVar()
        password = tk.StringVar()

        # Sign in frame
        self.signin = ttk.Frame(self.login_root)
        self.signin.pack(padx=15, pady=10, fill='x', expand=True)

        # Username
        self.user_label = ttk.Label(self.signin, text="Username:")
        self.user_label.pack(fill='x', expand=True)
        self.user_box = ttk.Entry(self.signin, textvariable=username)
        self.user_box.pack(fill='x', expand=True)
        self.user_box.focus()
        self.user_box.bind('<Return>', self.user_bind)

        # Password
        self.password = ttk.Label(self.signin, text="Password:")
        self.password.pack(fill='x', expand=True)
        self.password_box = ttk.Entry(
            self.signin, textvariable=password, show='*')
        self.password_box.pack(fill='x', expand=True)
        self.password_box.bind('<Return>', self.login_bind)

        # Login Button
        self.button = ttk.Button(
            self.signin, text="Login", command=self.login_action)
        self.button.pack(fill='x', expand=True, pady=10)

        # Execute mainloop
        self.login_root.mainloop()

    def gui_chat(self):

        # Start window and assign string variables
        self.chat_root = self.new_tk_window("450x650", "Chat Windows")
        self.msg = tk.StringVar()

        # Sign in frame
        self.signin = ttk.Frame(self.chat_root)
        self.signin.pack(padx=15, pady=10, fill='x', expand=True)

        # Set profile picture
        profile_pic = tk.PhotoImage(file=self.profile_select())

        self.chat_label = ttk.Label(
            self.signin,
            image=profile_pic,
            compound=tk.LEFT,
            text=f"Chat Window | {self.name.title()}")

        self.chat_label.pack(fill='x', expand=True)

        menu = "Chat commands:\n \
        time: calendar time in the system\n \
        who: to find out who else are there\n \
        c _peer_: to connect to the _peer_ and chat\n \
        ? _term_: to search your chat logs where _term_ appears\n \
        p _#_: to get number <#> sonnet\n \
        q: to leave the chat system\n"

        self.chat_instructions = ttk.Label(self.signin, text=menu)
        self.chat_instructions.pack(fill='x', expand=True)

        # Chat Window
        self.text_area = tks.ScrolledText(self.signin)
        self.text_area.pack(fill='x', pady=5)
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

        # Exit Button
        self.button = ttk.Button(
            self.signin, text="Exit", command=self.exit_chat)
        self.button.pack(side='left', pady=5)

        # Sonnet Button
        self.button = ttk.Button(
            self.signin, text="Get Sonnet", command=self.sonnet_action)
        self.button.pack(side='left', pady=5)

        # Find friends button
        self.button = ttk.Button(
            self.signin, text="Find Friends", command=self.find_friends)
        self.button.pack(side='left', pady=5)

        # Emoji button
        self.button = ttk.Button(
            self.signin, text="Kaomoji", command=self.emoji_action)
        self.button.pack(side='left', pady=5)

        # Send Button
        try:
            button_icon = tk.PhotoImage(file='assets\\send_icon_smaller.png')
        except Exception:
            button_icon = tk.PhotoImage(file='assets/send_icon_smaller.png')

        self.button = ttk.Button(
            self.signin, image=button_icon, text="SEND", compound=tk.RIGHT, command=self.write)
        self.button.pack(fill='x', expand=True, pady=5)
        self.running = True

        # Start the mainloop
        self.chat_root.mainloop()

    def new_tk_window(self, dimensions: str, title: str):
        result = tk.Tk()
        result.geometry(dimensions)
        result.resizable(False, False)
        result.title(title)
        return result

    def profile_select(self):
        import os
        import random
        files = [file for file in os.listdir(
            './assets/') if file.startswith('minion')]
        random_file = random.choice(files)
        return f'./assets/{random_file}'

    def gui_loop(self):
        while self.sm.get_state() != S_LOGGEDIN:
            self.gui_login()
        self.gui_chat()

    def user_bind(self, event):
        self.user_action()
        self.password_box.focus()

    def user_action(self):
        self.username = self.user_box.get()

    def login_bind(self, event):
        self.login_action()

    # TODO Look to improve efficiency of this code
    def login_action(self):
        self.password = self.password_box.get()
        self.console_input.append(self.username + '\n' + self.password)
        while True:
            if self.get_trigger() == True:
                self.login_root.destroy()
                self.set_trigger(False)
                break
            else:
                time.sleep(1)

    def find_friends(self):
        if self.sm.get_state() == S_CHATTING:
            self.display_info('Cannot Find Friends Now',
                              "You're talking to a friend right now! Pay attention")

        elif self.sm.get_state() == S_LOGGEDIN:
            text = 'find_friend'
            # no need for lock, append is thread safe
            self.console_input.append(text)

    def emoji_action(self):
        import random
        if self.sm.get_state() == S_CHATTING:
            self.send_emojis(random)
        elif self.sm.get_state() == S_LOGGEDIN:
            title = 'Cannot Use This Function'
            showinfo(title, "Please try again when you're chatting")

    def send_emojis(self, random):
        emoji_list = ["ಥ_ಥ", "╰(*°▽°*)╯", "(❁´◡`❁)",
                      "(●'◡'●)", ".｡.", "o(≧▽≦)o",
                      "༼ つ ◕_◕ ༽つ", "(╯°□°）╯︵ ┻━┻)",
                      "ψ(._. )>", "ಠ_ಠ", "ಠoಠ", "ಠ‿ಠ"]
        emoji = random.choice(emoji_list)
        self.message = f"[{self.name}]{emoji}\n"
        self.console_input.append(emoji)
        self.show_message()

    def sonnet_action(self):
        import random
        num = str(random.randint(1, 110))
        if self.sm.get_state() == S_CHATTING:
            self.display_info('Cannot Find Sonnet Now',
                              "Please try again when you're not chatting")

        elif self.sm.get_state() == S_LOGGEDIN:
            text = f'p{num}'
            self.console_input.append(text)

    def display_error(self, title, message):
        showerror(f"{title} Error", message)

    def display_info(self, title, message):
        showinfo(title, message)

    def write_bind(self, event):
        self.write()

    def exit_chat(self):
        if self.sm.get_state() == S_CHATTING:
            text = 'bye'
            self.console_input.append(text)
        elif self.sm.get_state() == S_LOGGEDIN:
            text = 'q'
            self.console_input.append(text)

    def write(self):
        text = self.user_box.get()
        # no need for lock, append is thread safe
        self.console_input.append(text)
        if self.sm.get_state() == S_CHATTING:
            self.message = f"[{self.name}]{self.msg.get()}\n"
            self.chat_start = False
        else:
            self.chat_start = True
            self.message = f"{self.msg.get()}\n"
        self.show_message()
        self.user_box.delete(0, 'end')

    def show_message(self):
        self.text_area.config(state='normal')
        self.text_area.insert('end', self.message)
        self.text_area.yview('end')
        self.text_area.config(state='disabled')

    def output(self):
        if len(self.system_msg) > 0:
            print(self.system_msg)
            if self.running:
                self.text_area.config(state='normal')
                self.text_area.insert('end', self.system_msg + '\n')
                self.text_area.yview('end')
                self.text_area.config(state='disabled')
            self.system_msg = ''

    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self):
        self.init_chat()
        self.system_msg += 'Welcome to ICS chat\n'
        self.system_msg += 'Please enter your name: '
        self.output()
        while self.login() != True:
            self.output()
        self.system_msg += f'Welcome, {self.get_name()}!'
        self.output()
        while self.sm.get_state() != S_OFFLINE:
            self.proc()
            self.output()
            time.sleep(CHAT_WAIT)
        self.quit()

# ==============================================================================
# main processing loop
# ==============================================================================
    def proc(self):
        my_msg, peer_msg = self.get_msgs()
        self.system_msg += self.sm.proc(my_msg, peer_msg)
