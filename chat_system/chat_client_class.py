import socket
import time
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm
import threading
# GUI
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
        self.gui_done = False
        self.login_ok = False

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_name(self):
        return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        # self.socket.connect(('0.tcp.jp.ngrok.io', 15664))
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
        my_msg = ''
        peer_msg = []
        #peer_code = M_UNDEF    for json data, peer_code is redundant
        if len(self.console_input) > 0:
            my_msg = self.console_input.pop(0)
        if self.socket in read:
            peer_msg = self.recv()
        return my_msg, peer_msg

    # Integrate this with GUI
    def login(self):
        my_msg, peer_msg = self.get_msgs()
        if len(my_msg) > 0:
            # print(my_msg)
            login_info = my_msg.split('\n')
            self.name = login_info[0]
            self.pswrd = login_info[1]
            # print('PASSWORD',self.pswrd)
            msg = json.dumps({"action":"login", "name":self.name, "password":self.pswrd})
            self.send(msg)
            response = json.loads(self.recv())
            # This checks whether the user is authenticated
            if response["status"] == 'ok':
                self.state = S_LOGGEDIN
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)
                self.login_ok = True
                return (True)
            elif response["status"] == 'duplicate':
                self.login_ok = False
                # self.system_msg += 'Duplicate username, try again'
                return False
        else:               # fix: dup is only one of the reasons
           return(False)

    def gui_login(self):
        # Tkinter Window
        self.login_root = tk.Tk()
        self.login_root.geometry("300x150")
        self.login_root.resizable(False, False)
        self.login_root.title("User Login")

        # Login String Variables
        username = tk.StringVar()
        password = tk.StringVar()

        # Sign in frame
        self.signin = ttk.Frame(self.login_root)
        self.signin.pack( padx=15, pady=10, fill='x', expand=True)

        # Username 
        self.user_label = ttk.Label( self.signin, text="Username:")
        self.user_label.pack( fill='x', expand=True)
        self.user_box = ttk.Entry(self.signin, textvariable=username)
        self.user_box.pack( fill='x', expand=True)
        self.user_box.focus()
        self.user_box.bind('<Return>', self.user_bind)

        # Password
        self.password = ttk.Label( self.signin, text="Password:")
        self.password.pack( fill='x', expand=True)
        self.password_box = ttk.Entry( self.signin, textvariable=password, show='*')
        self.password_box.pack( fill='x', expand=True)
        self.password_box.bind('<Return>', self.login_bind)

        # Login Button
        self.button = ttk.Button( self.signin, text="Login", command=self.login_action)
        self.button.pack(fill='x', expand=True, pady=10)

        # Execute mainloop
        self.login_root.mainloop()

    def gui_chat(self):

        # Tkinter Window
        self.chat_root = tk.Tk()
        self.chat_root.geometry("600x800")
        self.chat_root.resizable(True, True)
        self.chat_root.title("Chat Windows")

        # Chat String Variables
        self.msg = tk.StringVar()

        # Sign in frame
        self.signin = ttk.Frame(self.chat_root)
        self.signin.pack(padx=15, pady=10, fill='x', expand=True)

        self.chat_label = ttk.Label(
            self.signin,
            text=f"Chat Window | {self.name.title()}")

        self.chat_label.pack( fill='x', expand=True)

        # Exit Button
        self.button = ttk.Button(
            self.signin,
            text="EXIT",
            command=self.exit_chat)

        self.button.pack(fill='x', expand=True, pady=10)

        menu = "Choose one of the following commands\n \
        time: calendar time in the system\n \
        who: to find out who else are there\n \
        c _peer_: to connect to the _peer_ and chat\n \
        ? _term_: to search your chat logs where _term_ appears\n \
        p _#_: to get number <#> sonnet\n \
        q: to leave the chat system\n\n"

        self.chat_instructions = ttk.Label(
            self.signin,
            text=menu
        )

        self.chat_instructions.pack(
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
        # I don't think I actually need to disable this
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
        try: 
            button_icon = tk.PhotoImage(file='..\\temp\\assets\\send_icon_smaller.png')
        except:
            button_icon = tk.PhotoImage(file='../temp/assets/send_icon_smaller.png')

        self.button = ttk.Button(
            self.signin,
            image=button_icon,
            text="SEND",
            compound=tk.RIGHT,
            command=self.write)

        self.button.pack(fill='x', expand=True, pady=10)

        self.running = True
        self.chat_root.mainloop()

    def gui_loop(self):
        while self.login_ok == False:
            self.gui_login()
            # self.gui_login_error()
        self.gui_chat()

    def gui_login_error(self):
        title = 'Login Error'
        message = 'Duplicate username, try again'
        showerror(title, message)

    def user_bind(self, event):
        self.user_action()
        self.password_box.focus()

    def user_action(self):
        self.username = self.user_box.get()

    def login_bind(self, event):
        self.login_action()

    def login_action(self):
        self.password = self.password_box.get()
        self.console_input.append(self.username + '\n' + self.password) # no need for lock, append is thread safe
        self.login_root.destroy()

    def write_bind(self, event):
        self.write()

    def exit_chat(self):
        if self.sm.get_state() == S_CHATTING:
            text = 'bye'
            self.console_input.append(text) # no need for lock, append is thread safe
        elif self.sm.get_state() == S_LOGGEDIN:
            text = 'q'
            self.console_input.append(text) # no need for lock, append is thread safe

    def write(self):
        text = self.user_box.get()
        self.console_input.append(text) # no need for lock, append is thread safe
        if self.sm.get_state() == S_CHATTING:
            self.message = f"[{self.name}]{self.msg.get()}\n"
        else:
            self.message = f"{self.msg.get()}\n"
        self.text_area.config(state='normal')
        self.text_area.insert('end', self.message)
        self.text_area.yview('end')
        self.text_area.config(state='disabled')
        self.user_box.delete(0, 'end')

    def output(self):
        if len(self.system_msg) > 0:
            # I think that this is where I should implement the GUI
            print(self.system_msg)
            # ---GUI STUFF---
            if self.running:
                self.text_area.config(state='normal')
                self.text_area.insert('end', self.system_msg + '\n')
                self.text_area.yview('end')
                self.text_area.config(state='disabled')
            # ---GUI STUFF---
            self.system_msg = ''

    def read_input(self):
        while True:
            # This is the thing that reads the input from the user
            text = sys.stdin.readline()[:-1]
            print('LOGGED IN STATE', self.state)
            print('TRIGGERED')
            self.console_input.append(text) # no need for lock, append is thread safe

    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self):
        self.init_chat()
        self.system_msg += 'Welcome to ICS chat\n'
        self.system_msg += 'Please enter your name: '
        self.output()
        while self.login() != True:
            self.output()
        # if not self.login_ok:
            # self.gui_login_error()
        self.system_msg += 'Welcome, ' + self.get_name() + '!'
        self.output()
        while self.sm.get_state() != S_OFFLINE:
            self.proc()
            self.output()
            time.sleep(CHAT_WAIT)
        self.quit()

#==============================================================================
# main processing loop
#==============================================================================
    def proc(self):
        my_msg, peer_msg = self.get_msgs()
        self.system_msg += self.sm.proc(my_msg, peer_msg)
