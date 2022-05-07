#!/usr/bin/python

import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

class GUI:
    def __init__(self):
        self.gui_done = False
        # Returns a string
        self.nickname = simpledialog.askstring("Nickname", "Enter a nickname:")

    def gui_loop(self):
        self.running = True
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.win, text="Chat", bg="lightgray")
        self.chat_label.configure(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message", bg="lightgray")
        self.msg_label.configure(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3, width=30)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', tkinter.END)}"
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

if __name__ == "__main__":
    gui = GUI()
    gui.gui_loop()
    print("GUI closed")