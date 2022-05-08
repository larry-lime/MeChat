import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tks
from tkinter import simpledialog

class GUI:
    def __init__(self) -> None:
        self.user = simpledialog.askstring("User","Enter your name:")
    
    def gui_main(self):
        self.runnning = True
        self.win = tk.Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = tk.Label(self.win, text="Chat", bg="lightgray")
        self.chat_label.configure(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tks.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.win.mainloop()

class Test:
    def __init__(self) -> None:
        pass

    # Widget syntax:
    # widget = WidgetName(container, **options)
    def gui_main(self):
        self.window = tk.Tk()
        # Give the current window a title
        self.window.title('Tkinter Window Demo')
        # Set the size of the window
        win_x = 600
        win_y = 400
        self.window.geometry(f"{win_x}x{win_y}+1000+200")

        # Create a label widget
        self.message = tk.Label(self.window, text="Hello, World!")
        self.message.pack()

        # keep the window displaying
        self.window.mainloop()


if __name__ == "__main__":
    # gui = GUI()
    gui = Test()
    gui.gui_main()
