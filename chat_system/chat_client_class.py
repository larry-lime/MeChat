import socket
import time
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm
import threading
# GUI
# import tkinter
# import tkinter.scrolledtext
# from tkinter import simpledialog

class Client:
    def __init__(self, args):
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args
        # self.nickname = simpledialog.askstring("Nickname", "Enter a nickname:")
        # GUI Flag Var
        self.gui_done = False
        self.running = True

        # GUI Programming
        # msg = tkinter.Tk()
        # msg.withdraw()

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_name(self):
        return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)
        reading_thread = threading.Thread(target=self.read_input)
        reading_thread.daemon = True
        reading_thread.start()

        # GUI Thread
        # gui_thread = threading.Thread(target=self.gui_loop)
        # gui_thread.start()

    def shutdown_chat(self):
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

    def output(self):
        if len(self.system_msg) > 0:
            # I think that this is where I should implement the GUI
            print(self.system_msg)
            self.system_msg = ''

    def login(self):
        my_msg, peer_msg = self.get_msgs()
        if len(my_msg) > 0:
            self.name = my_msg
            msg = json.dumps({"action":"login", "name":self.name})
            # print('bug?',type(msg))
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.state = S_LOGGEDIN
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)
                self.print_instructions()
                return (True)
            elif response["status"] == 'duplicate':
                self.system_msg += 'Duplicate username, try again'
                return False
        else:               # fix: dup is only one of the reasons
           return(False)


    def read_input(self):
        while True:
            # I think that I may need to add the input GUI element here. I'm not sure
            text = sys.stdin.readline()[:-1]
            self.console_input.append(text) # no need for lock, append is thread safe

    # def gui_loop(self):
        # self.win = tkinter.Tk()
        # self.win.configure(bg="lightgray")

        # self.chat_label = tkinter.Label(self.win, text="Chat", bg="lightgray")
        # self.chat_label.configure(font=("Arial", 12))
        # self.chat_label.pack(padx=20, pady=5)

        # self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        # self.text_area.pack(padx=20, pady=5)
        # self.text_area.config(state='disabled')

        # self.msg_label = tkinter.Label(self.win, text="Message", bg="lightgray")
        # self.msg_label.configure(font=("Arial", 12))
        # self.msg_label.pack(padx=20, pady=5)

        # self.input_area = tkinter.Text(self.win, height=3, width=30)
        # self.input_area.pack(padx=20, pady=5)

        # self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        # self.send_button.config(font=("Arial", 12))
        # self.send_button.pack(padx=20, pady=5)

        # self.gui_done = True
        # self.win.protocol("WM_DELETE_WINDOW", self.stop)
        # self.win.mainloop()


    # def write(self):
        # message = f"{self.nickname}: {self.input_area.get('1.0', tkinter.END)}"
        # print(message)
        # # Right here is when I need to send the message to the server
        # # self.sock.send(message.encode('utf-8'))
        # self.input_area.delete('1.0', 'end')

    # # This kills the GUI window when I press the X button
    # def stop(self):
        # self.running = False
        # self.win.destroy()
        # exit(0)

    # def recieve(self):
        # while self.running:
            # try: 
                # # message = self.sock.recv(1024)
                # message = "test"
                # if message == "NICK":
                    # # self.sock.send(self.nickname.encode('utf-8'))
                    # pass
                # else:
                    # if self.gui_done:
                        # self.text_area.config(state='normal')
                        # self.text_area.insert('end', message)
                        # self.text_area.yview('end')
                        # self.text_area.config(state='disabled')
            # except:
                # break

    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self):
        self.init_chat()
        # Start GUI with terminal chat
        # self.gui_loop()
        self.system_msg += 'Welcome to ICS chat\n'
        self.system_msg += 'Please enter your name: '
        self.output()
        while self.login() != True:
            self.output()
        self.system_msg += 'Welcome, ' + self.get_name() + '!'
        self.output()
        # This is how the actual chat room operates
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
        # print('my_msg:',my_msg)
        # print('peer_msg:',peer_msg)
        self.system_msg += self.sm.proc(my_msg, peer_msg)
