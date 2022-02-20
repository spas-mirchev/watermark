import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# create the root window
root = tk.Tk()
root.title("Tkinter File Dialog")

root.geometry("300x150")
from PIL import Image, ImageTk


def select_files():
    filetypes = (("image files", "*.jpg"), ("image files", "*.png"))

    filenames = fd.askopenfilenames(
        title="Open files", initialdir=".", filetypes=filetypes
    )

    showinfo(title="Selected Files", message=filenames)
    print(filenames)


# open button
open_button = ttk.Button(root, text="Open Files", command=select_files)

open_button.pack(expand=True)

root.mainloop()
