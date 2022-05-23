from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import filedialog as fd


class WrapAll:
    def __init__(self) -> None:

        self.window = Tk()
        self.window.title("Add watermark to images")
        self.window.config(padx=10, pady=10)

        self.my_var = StringVar()
        self.x = IntVar(self.window, 0)
        self.y = IntVar(self.window, 0)
        self.text_xcor = IntVar(self.window, 0)
        self.text_ycor = IntVar(self.window, 0)
        self.aspect = IntVar(self.window, 1)
        self.text_size = IntVar(self.window, 60)
        self.logo_opacity = DoubleVar(self.window, 0.0)
        self.colour_var = StringVar(self.window, "#f0a00c66")

        self.canvas = Canvas(self.window, width=840, height=640)
        self.canvas.grid(row=0, column=0, rowspan=7)

        self.upload_img = Button(
            width=50,
            text="Upload image ",
            font=("", 12),
            command=self.select_files,
        )
        self.upload_img.grid(column=1, row=0, columnspan=4, padx=10, pady=10)

        self.font_size_label = Label(text="Choose font size: ", font=("", 13))
        self.font_size_label.grid(column=1, row=1)

        self.choose_text_size = Scale(
            from_=20,
            to=60,
            tickinterval=10,
            orient=HORIZONTAL,
            width=23,
            length=300,
            resolution=10,
            command=self.size_text,
        )

        self.choose_text_size.grid(row=1, column=2, columnspan=3)

        self.choose_color = Button(
            text="Select text colour",
            width=18,
            font=("", 12),
            command=self.change_color,
        )

        self.choose_color.grid(column=0, row=7)

        self.text_opacity = Label(text="Text opacity ", font=("", 13))
        self.text_opacity.grid(column=1, row=3)

        self.opacity_text = Scale(
            from_=20,
            to=100,
            tickinterval=20,
            orient=HORIZONTAL,
            width=23,
            length=300,
            resolution=20,
            command=self.opacity,
        )

        self.opacity_text.grid(row=3, column=2, columnspan=3)

        self.add_text = Label(text="Add watermark text: ", font=("", 13))
        self.add_text.grid(column=1, row=2)

        self.e_text = Entry(width=25, font=("Helvetica", 18), textvariable=self.my_var)
        self.e_text.grid(column=2, row=2, columnspan=3)

        self.my_var.trace("w", lambda *args: self.character_limit(self.my_var))

        self.logo_opacity_label = Label(text="Logo opacity: ", font=("", 13))
        self.logo_opacity_label.grid(column=1, row=5)

        self.opacity_logo = Scale(
            from_=20,
            to=100,
            tickinterval=20,
            orient=HORIZONTAL,
            width=23,
            length=300,
            resolution=20,
            command=self.change_logo_opacity,
        )

        self.opacity_logo.grid(row=5, column=2, columnspan=3)

        self.upload_image = Button(
            text="Add logo image",
            font=("Helvetica", 12),
            width=20,
            command=self.add_logo,
        )
        self.upload_image.grid(column=1, row=4)

        self.adjust = Label(
            text="Adjust logo position with arrows", font=("Ariel.ttf", 13)
        )
        self.adjust.grid(column=2, row=4, columnspan=3)

        self.save_button = Button(
            width=50,
            text="Save image ",
            font=("Ariel.ttf", 12),
            command=self.save_image,  # lambda: self.save_image(self.original_image),
        )
        self.save_button.grid(column=1, row=6, columnspan=4)

        self.my_var.trace_add("write", self.on_key)

        self.window.bind("<Left>", self.left)
        self.window.bind("<Right>", self.right)
        self.window.bind("<Up>", self.up)
        self.window.bind("<Down>", self.down)
        # self.canvas.bind("<B1-Motion>", self.motion)
        self.canvas.bind("<B1-Motion>", self.motion_text)
        self.window.mainloop()

    def select_files(self):
        self.filetypes = (("image files", "*.jpg"), ("image files", "*.png"))
        self.filenames = fd.askopenfilenames(
            title="Open files", initialdir="./images", filetypes=self.filetypes
        )
        self.original_image = Image.open(self.filenames[0]).convert("RGBA")
        self.make_preview()

    def make_preview(self):
        if self.original_image.width > 840:
            self.aspect.set(round(self.original_image.width / 840))

        if self.original_image.height > 640:
            self.aspect.set(round(self.original_image.height / 640))
            # print(self.aspect.get())

        self.preview_image = self.original_image.copy().reduce(self.aspect.get())

        if self.preview_image.width > 840 or self.preview_image.height > 640:
            self.aspect.set(self.aspect.get() + 1)
            self.preview_image = self.original_image.copy().reduce(self.aspect.get())
            # print(self.aspect.get())

        self.test = ImageTk.PhotoImage(self.preview_image)

        self.image_container = self.canvas.create_image(
            0, 0, image=self.test, anchor=NW
        )

    def on_key(self, var, mode, callback):

        self.img = Image.new("RGBA", self.preview_image.size, (255, 255, 255, 0))

        self.draw = ImageDraw.Draw(self.img)

        self.font = ImageFont.truetype("DejaVuSerif-Bold.ttf", self.text_size.get())

        self.draw.text(
            (self.text_xcor.get(), self.text_ycor.get()),
            text=self.my_var.get(),
            font=self.font,
            fill=self.colour_var.get(),
        )

        self.out = Image.alpha_composite(self.preview_image, self.img)

        try:
            self.out1 = Image.alpha_composite(self.out, self.img1)

        except AttributeError:
            self.test1 = ImageTk.PhotoImage(self.out)
        else:
            self.test1 = ImageTk.PhotoImage(self.out1)
        self.canvas.itemconfigure(self.image_container, image=self.test1)

    def add_logo(self):
        self.filetypes = (("image files", "*.png"),)
        self.filename = fd.askopenfilenames(
            title="Open files", initialdir="./images", filetypes=self.filetypes
        )
        self.logo_image = Image.open(self.filename[0]).convert("RGBA")
        self.logo_preview = self.logo_image.copy()

        self.adjust_logo()

    def adjust_logo(self):
        self.logo_preview.thumbnail((self.text_size.get(), self.text_size.get()))
        self.im2 = Image.new("RGBA", self.logo_preview.size, (0, 0, 0, 0))
        self.blended = Image.blend(
            self.logo_preview, self.im2, alpha=self.logo_opacity.get()
        )

        self.img1 = Image.new("RGBA", self.preview_image.size, (0, 0, 0, 0))
        self.img1.paste(self.blended, (self.x.get(), self.y.get()), self.blended)

        self.out1 = Image.alpha_composite(self.preview_image, self.img1)

        try:
            self.out2 = Image.alpha_composite(self.out, self.img1)
        except AttributeError:
            self.test = ImageTk.PhotoImage(self.out1)
        else:
            self.test = ImageTk.PhotoImage(self.out2)

        self.canvas.itemconfigure(self.image_container, image=self.test, tags="square")

        return True

    def change_color(self):
        self.colors = askcolor(title="Tkinter Color Chooser")
        self.colour_var.set(self.colors[1])
        self.on_key("", "", "")

    def character_limit(self, my_var):
        if len(self.my_var.get()) > 0:
            self.my_var.set(self.my_var.get()[:15])

    def opacity(self, value):
        if value == "20":
            self.colour_var.set((self.colors[1] + "33"))

        elif value == "40":
            self.colour_var.set((self.colors[1] + "66"))

        elif value == "60":
            self.colour_var.set((self.colors[1] + "99"))

        elif value == "80":
            self.colour_var.set((self.colors[1] + "cc"))

        else:
            self.colour_var.set((self.colors[1] + "ff"))

        self.on_key("", "", "")

    def change_logo_opacity(self, value):
        if value == "20":
            self.logo_opacity.set(0.6)
        elif value == "40":
            self.logo_opacity.set(0.4)
        elif value == "60":
            self.logo_opacity.set(0.25)
        elif value == "80":
            self.logo_opacity.set(0.1)
        else:
            self.logo_opacity.set(0.0)

        self.adjust_logo()

    def save_image(self):
        counter = 0
        for items in self.filenames:
            self.original_image = Image.open(items).convert("RGBA")
            counter += 1
            self.process(counter)

    def process(self, counter):
        self.xcor = int(
            self.text_xcor.get() / self.preview_image.width * self.original_image.width
        )

        self.ycor = int(
            self.text_ycor.get() / self.preview_image.width * self.original_image.width
        )

        self.texts = int(
            self.text_size.get() / self.preview_image.width * self.original_image.width
        )

        self.xx = int(
            self.x.get() / self.preview_image.width * self.original_image.width
        )

        self.yy = int(
            self.y.get() / self.preview_image.width * self.original_image.width
        )

        self.img = Image.new("RGBA", self.original_image.size, (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.truetype("DejaVuSerif-Bold.ttf", self.texts)

        self.draw.text(
            (self.xcor, self.ycor),
            text=self.my_var.get(),
            font=self.font,
            fill=self.colour_var.get(),
        )

        self.out = Image.alpha_composite(self.original_image, self.img)

        # self.logo_image.thumbnail((self.texts, self.texts))
        # self.transparent_layer = Image.new("RGBA", self.logo_image.size, (0, 0, 0, 0))

        # self.blended = Image.blend(
        #     self.logo_image, self.transparent_layer, alpha=self.logo_opacity.get()
        # )

        # self.original_image.paste(self.blended, (self.xx, self.yy), self.blended)

        try:
            self.logo_image.thumbnail((self.texts, self.texts))
            self.transparent_layer = Image.new(
                "RGBA", self.logo_image.size, (0, 0, 0, 0)
            )

            self.blended = Image.blend(
                self.logo_image, self.transparent_layer, alpha=self.logo_opacity.get()
            )

            self.original_image.paste(self.blended, (self.xx, self.yy), self.blended)
        except AttributeError as error:
            self.out.save(f"./watermark_images/watermark{counter}111.png")
        else:
            self.final = Image.alpha_composite(self.original_image, self.img)
            self.final.save(f"./watermark_images/watermark{counter}.png")

    def size_text(self, value):
        self.text_size.set(self.choose_text_size.get())
        # self.AdjustLogo()
        self.on_key("", "", "")

    def motion_text(self, event):
        self.text_xcor.set(event.x)
        self.text_ycor.set(event.y)
        self.on_key("", "", "")

    def left(self, e):
        self.x.set(self.x.get() - 15)
        self.y.set(self.y.get())
        self.adjust_logo()

    def right(self, e):
        self.x.set(self.x.get() + 15)
        self.y.set(self.y.get())
        self.adjust_logo()

    def up(self, e):
        self.x.set(self.x.get())
        self.y.set(self.y.get() - 15)
        self.adjust_logo()

    def down(self, e):
        self.x.set(self.x.get())
        self.y.set(self.y.get() + 15)
        self.adjust_logo()


WrapAll()
