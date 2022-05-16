import tkinter as tk
from tkinter import ttk

def paned_window():
    root = tk.Tk()
    root.title('PanedWindow Demo')
    root.geometry('300x200')

    # change style to classic (Windows only) 
    # to show the sash and handle
    style = ttk.Style()
    style.theme_use('classic')

    # paned window
    pw = ttk.PanedWindow(orient=tk.HORIZONTAL)

    # Left listbox
    left_list = tk.Listbox(root)
    left_list.pack(side=tk.LEFT)
    pw.add(left_list)

    # Right listbox
    right_list = tk.Listbox(root)
    right_list.pack(side=tk.LEFT)
    pw.add(right_list)

    # place the panedwindow on the root window
    pw.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

def create_input_frame(container):

    frame = ttk.Frame(container)

    # grid layout for the input frame
    frame.columnconfigure(0, weight=1)

    # Find what
    # ttk.Label(frame, text='Find what:').grid(column=0, row=0, sticky=tk.W)
    keyword = ttk.Entry(frame, width=30)
    keyword.focus()
    keyword.grid(column=0, row=0, sticky=tk.S)

    # Replace with:
    # ttk.Label(frame, text='Replace with:').grid(column=0, row=1, sticky=tk.W)
    # replacement = ttk.Entry(frame, width=30)
    # replacement.grid(column=1, row=1, sticky=tk.W)

    # Match Case checkbox
    # match_case = tk.StringVar()
    # match_case_check = ttk.Checkbutton(
        # frame,
        # text='Match case',
        # variable=match_case,
        # command=lambda: print(match_case.get()))
    # match_case_check.grid(column=0, row=2, sticky=tk.W)

    # Wrap Around checkbox
    # wrap_around = tk.StringVar()
    # wrap_around_check = ttk.Checkbutton(
        # frame,
        # variable=wrap_around,
        # text='Wrap around',
        # command=lambda: print(wrap_around.get()))
    # wrap_around_check.grid(column=0, row=3, sticky=tk.W)

    # for widget in frame.winfo_children():
        # widget.grid(padx=0, pady=5)

    return frame


def create_button_frame(container):
    frame = ttk.Frame(container)

    frame.columnconfigure(0, weight=1)

    ttk.Button(frame, text='Find Friends').grid(column=0, row=0)
    ttk.Button(frame, text='Random Sonnet').grid(column=1, row=0)
    # ttk.Button(frame, text='Replace All').grid(column=2, row=0)
    ttk.Button(frame, text='Leave').grid(column=2, row=0)

    # for widget in frame.winfo_children():
        # widget.grid(ipadx==0, ipady==3)

    return frame

def send_button(container):
    frame = ttk.Frame(container)
    frame.columnconfigure(0, weight=1)

    ttk.Button(frame, text='Send').grid(column=3, row=0)
    for widget in frame.winfo_children():
        widget.grid(ipadx=0, ipady=0)
    return frame

def create_main_window():

    # root window
    root = tk.Tk()
    root.title('Replace')
    root.geometry('600x800')
    root.resizable(True, True)
    # windows only (remove the minimize/maximize button)
    # root.attributes('-toolwindow', True)

    # layout on the root window
    root.columnconfigure(0, weight=4)
    root.columnconfigure(1, weight=4)
    root.columnconfigure(2, weight=4)
    root.columnconfigure(3, weight=4)
    root.columnconfigure(4, weight=4)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(3, weight=1)
    root.rowconfigure(4, weight=1)
    root.rowconfigure(5, weight=1)
    root.rowconfigure(6, weight=1)
    root.rowconfigure(7, weight=1)
    root.rowconfigure(8, weight=1)
    root.rowconfigure(9, weight=1)

    button_frame = create_button_frame(root)
    button_frame.grid(padx=0,pady=0,column=2, row=6)

    input_frame = create_input_frame(root)
    # input_frame.grid(column=0, row=0)
    input_frame.grid(padx=0,pady=0,column=2, row=7)


    button_frame = send_button(root)
    button_frame.grid(padx=0,pady=0,column=2, row=8)

    root.mainloop()

def test():
    import tkinter

    master=tkinter.Tk()
    master.title("pack() method")
    master.geometry("450x350")

    button1=tkinter.Button(master, text="LEFT")
    button1.pack(side=tkinter.LEFT)

    button2=tkinter.Button(master, text="RIGHT")
    button2.pack(side=tkinter.RIGHT)

    button3=tkinter.Button(master, text="TOP")
    button3.pack(side=tkinter.TOP)

    button4=tkinter.Button(master, text="BOTTOM")
    button4.pack(side=tkinter.BOTTOM)

    master.mainloop()



if __name__ == "__main__":
    create_main_window()
    # paned_window()
