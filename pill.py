from curses import wrapper
from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import filedialog as fd
import os

from click import clear


class WatermarkApp:
    """Builds GUI."""

    def __init__(self, master):
        """Create window."""
        self.master = master
        master.title("Watermark")
        master.config(padx=10, pady=10)
        frame = Frame(master, width=1100, height=600)
        frame.grid(row=0, column=0, rowspan=6)

        self.canvas = Canvas(frame, width=840, height=640)
        self.canvas.pack()
        # self.set_ui()

        # def set_ui(self):
        """Set UI"""
        self.my_var = StringVar()
        self.colour_var = StringVar(self.master, "#f0a00c20")
        self.x = IntVar(self.master, 5)
        self.y = IntVar(self.master, 5)
        self.f = IntVar(self.master, 1)

        upload_img = Button(
            width=50,
            text="Upload image ",
            font=("", 12),
            command=self.select_files,
        )
        upload_img.grid(column=1, row=0, columnspan=4, padx=10, pady=10)

        choose_color = Button(
            text="Select text colour",
            width=18,
            font=("", 12),
            command=self.change_color,
        )
        choose_color.grid(column=1, row=1)

        opacity = Scale(
            from_=20,
            to=100,
            tickinterval=20,
            orient=HORIZONTAL,
            width=23,
            length=300,
            resolution=20,
            # command=self.opacity,
        )
        opacity.grid(row=1, column=2, columnspan=3)

        add_text = Label(text="Add watermark text: ", font=("", 13))
        add_text.grid(column=1, row=2)

        e_text = Entry(width=25, font=("Helvetica", 18), textvariable=self.my_var)
        e_text.grid(column=2, row=2, columnspan=3)
        self.my_var.trace("w", lambda *args: self.character_limit(self.my_var))

        upload_image = Button(
            text="Add logo image",
            font=("Helvetica", 12),
            width=20,
            command=self.AddLogo,
        )
        upload_image.grid(column=1, row=3)

        adjust = Label(text="Adjust logo position with arrows", font=("Ariel.ttf", 13))
        adjust.grid(column=2, row=3, columnspan=3)

        save_image = Button(
            width=50,
            text="Save image ",
            font=("Ariel.ttf", 12),
            command=self.save_image,
        )
        save_image.grid(column=1, row=4, columnspan=4)

        save_all = Button(
            width=50,
            text="Set automatically watermark to all images",
            font=("Ariel.ttf", 12),
            # command=self.save_original_images,
        )
        save_all.grid(column=1, row=5, columnspan=4)

        self.my_var.trace_add("write", self.OnKey)

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

    def open_files(function):
        def wrapper(self):
            self.filetypes = (("image files", "*.jpg"), ("image files", "*.png"))
            self.filenames = fd.askopenfilenames(
                title="Open files", initialdir=".", filetypes=self.filetypes
            )
            function(self)

        return wrapper

    @open_files
    def select_files(self):
        self.clear_image = Image.open(self.filenames[0]).convert("RGBA")
        print(self.clear_image.size[0])
        if self.clear_image.size[0] > 840:
            self.f = self.clear_image.size[0] // 840 + 1
            print(self.f)
            self.preview_image = self.clear_image.copy().reduce(self.f)
        else:
            self.preview_image = self.clear_image.copy()

        self.test = ImageTk.PhotoImage(self.preview_image)

        self.image_container = self.canvas.create_image(
            420, 320, image=self.test, anchor=CENTER
        )

    def OnKey(self, var, mode, callback):

        self.img = Image.new("RGBA", self.preview_image.size, (255, 255, 255, 0))

        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.truetype("DejaVuSerif-Bold.ttf", 50)

        self.draw.text(
            (80, 0),
            text=self.my_var.get(),
            font=self.font,
            fill=self.colour_var.get(),
        )

        self.out = Image.alpha_composite(self.preview_image, self.img)
        self.out1 = Image.alpha_composite(self.out, self.transparent_logo)

        self.test1 = ImageTk.PhotoImage(self.out1)

        self.canvas.itemconfigure(self.image_container, image=self.test1)

    @open_files
    def AddLogo(self):
        self.c_image = Image.open(self.filenames[0]).convert("RGBA")
        self.logo_preview = self.c_image.copy()
        self.logo_preview.thumbnail((70, 70))
        self.transparent_logo = Image.new(
            "RGBA", self.preview_image.size, (255, 255, 255, 0)
        )

        self.transparent_logo.paste(
            self.logo_preview, (self.x.get(), self.y.get()), self.logo_preview
        )

        self.out2 = Image.alpha_composite(
            self.preview_image,
            self.transparent_logo,
        )

        self.test = ImageTk.PhotoImage(self.out2)
        self.canvas.itemconfigure(self.image_container, image=self.test, tags="square")

    def change_color(self):
        self.colors = askcolor(title="Tkinter Color Chooser")
        self.colour_var.set(self.colors[1])
        self.canvas.update()

    def character_limit(self, my_var):
        if len(self.my_var.get()) > 0:
            self.my_var.set(self.my_var.get()[:15])

    def save_image(self):
        self.out1.save("opp.png")

    def left(self, e):
        self.x.set(self.x.get() - 15)
        self.y.set(self.y.get())
        self.transparent_logo.paste(
            self.logo_preview, (self.x.get(), self.y.get()), self.logo_preview
        )

    def right(self, e):
        self.x.set(self.x.get() + 15)
        self.y.set(self.y.get())
        self.transparent_logo.paste(
            self.logo_preview, (self.x.get(), self.y.get()), self.logo_preview
        )

    def up(self, e):
        self.x.set(self.x.get())
        self.y.set(self.y.get() - 15)
        self.transparent_logo.paste(
            self.logo_preview, (self.x.get(), self.y.get()), self.logo_preview
        )

    def down(self, e):
        self.x.set(self.x.get())
        self.y.set(self.y.get() + 15)
        self.transparent_logo.paste(
            self.logo_preview, (self.x.get(), self.y.get()), self.logo_preview
        )

    @open_files
    def save_original_images(self):
        pass


window = Tk()
my_gui = WatermarkApp(window)
window.mainloop()

# def speed_calc_decorator(function):
#     def wrapper(self):
#         self.filenames = function()
#         self.clear_image = Image.open(self.filenames[0]).convert("RGBA")
#         self.preview_image = self.clear_image.copy()
#         self.preview_image.thumbnail(
#             (self.clear_image.size[0] / 2, self.clear_image.size[1] / 2)
#         )
#         print(self.preview_image)

#         self.test = ImageTk.PhotoImage(self.preview_image)
#         self.image_container = self.canvas.create_image(
#             400, 300, image=self.test, anchor=CENTER
#         )

#     return wrapper

# @speed_calc_decorator
# def select_files():
#     filetypes = (("image files", "*.jpg"), ("image files", "*.png"))
#     filenames = fd.askopenfilenames(
#         title="Open files", initialdir=".", filetypes=filetypes
#     )
#     return filenames
