# Import the required libraries
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os

# Create an instance of tkinter frame or window
win = Tk()

# Set the size of the window
win.geometry("700x350")


def create_subfolder():
    source_path = filedialog.askdirectory(title="Select the Parent Directory")
    path = os.path.join(source_path, "Images")
    os.makedirs(path)


button1 = ttk.Button(win, text="Select a Folder", command=create_subfolder)

button1.pack(pady=5)

win.mainloop()
