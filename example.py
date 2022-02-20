# from distutils import command
from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import filedialog as fd


def on_key(var, mode, callback):

    img = Image.new("RGBA", preview_image.size, (255, 255, 255, 0))

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("DejaVuSerif-Bold.ttf", text_size.get())

    draw.text(
        (text_xcor.get(), text_ycor.get()),
        text=my_var.get(),
        font=font,
        fill=colour_var.get(),
    )

    out = Image.alpha_composite(preview_image, img)

    try:
        out1 = Image.alpha_composite(out, img1)

    except AttributeError:
        test1 = ImageTk.PhotoImage(out)
    else:
        test1 = ImageTk.PhotoImage(out1)
    canvas.itemconfigure(image_container, image=test1)


def add_logo():
    filetypes = (("image files", "*.png"),)
    filenames = fd.askopenfilenames(
        title="Open files", initialdir="./images", filetypes=filetypes
    )
    logo_image = Image.open(filenames[0]).convert("RGBA")
    logo_preview = logo_image.copy()

    adjust_logo()


def adjust_logo():
    logo_preview.thumbnail((text_size.get(), text_size.get()))
    im2 = Image.new("RGBA", logo_preview.size, (0, 0, 0, 0))
    blended = Image.blend(logo_preview, im2, alpha=logo_opacity.get())

    img1 = Image.new("RGBA", preview_image.size, (0, 0, 0, 0))
    img1.paste(blended, (x.get(), y.get()), blended)

    out1 = Image.alpha_composite(preview_image, img1)

    try:
        out2 = Image.alpha_composite(out, img1)
    except AttributeError:
        test = ImageTk.PhotoImage(out1)
    else:
        test = ImageTk.PhotoImage(out2)

    canvas.itemconfigure(image_container, image=test, tags="square")


def change_color():
    colors = askcolor(title="Tkinter Color Chooser")
    colour_var.set(colors[1])
    canvas.update()


def character_limit(my_var):
    if len(my_var.get()) > 0:
        my_var.set(my_var.get()[:15])


def opacity(value):
    if value == "20":
        colour_var.set((colors[1] + "33"))
        logo_opacity.set(0.6)
    elif value == "40":
        colour_var.set((colors[1] + "66"))
        logo_opacity.set(0.4)
    elif value == "60":
        colour_var.set((colors[1] + "99"))
        logo_opacity.set(0.25)
    elif value == "80":
        colour_var.set((colors[1] + "cc"))
        logo_opacity.set(0.1)
    else:
        colour_var.set((colors[1] + "ff"))
        logo_opacity.set(0.0)

    adjust_logo()
    on_key("a", "write", "")


def transform(var, preview_size, original_size):
    var.set(var.get() / preview_size * original_size)


def save_imagez(original):
    transform(text_xcor, preview_image.width, original.width)
    transform(text_ycor, preview_image.width, original.width)
    transform(text_size, preview_image.width, original.width)
    transform(x, preview_image.width, original.width)
    transform(y, preview_image.width, original.width)

    img = Image.new("RGBA", original.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("DejaVuSerif-Bold.ttf", text_size.get())

    draw.text(
        (text_xcor.get(), text_ycor.get()),
        text=my_var.get(),
        font=font,
        fill=colour_var.get(),
    )
    out = Image.alpha_composite(original, img)

    logo_image.thumbnail((text_size.get(), text_size.get()))
    transparent_layer = Image.new("RGBA", logo_image.size, (0, 0, 0, 0))

    blended = Image.blend(logo_image, transparent_layer, alpha=logo_opacity.get())

    original.paste(blended, (x.get(), y.get()), blended)

    try:
        original.save("opp.png")
    except AttributeError:
        out.save("opp.png")
    else:
        final = Image.alpha_composite(original, img)
        final.save("./watermark_images/oop3.png")

    # def save_original_images():
    #     for items in filenames:
    #         original_img = Image.open(items).convert("RGBA")
    #         save_imagez(original_img)


# def motion(event):
#     x.set(event.x)
#     print(x.get())
#     y.set(event.y)
#     adjust_logo()


def motion_text(event):
    text_xcor.set(event.x)
    text_ycor.set(event.y)
    on_key("", "", "")


def left(e):
    x.set(x.get() - 15)
    y.set(y.get())
    adjust_logo()


def right(e):
    x.set(x.get() + 15)
    y.set(y.get())
    adjust_logo()


def up(e):
    x.set(x.get())
    y.set(y.get() - 15)
    adjust_logo()


def down(e):
    x.set(x.get())
    y.set(y.get() + 15)
    adjust_logo()


window = Tk()
window.title("Add watermark to images")
window.config(padx=10, pady=10)

my_var = StringVar()
x = IntVar(window, 0)
y = IntVar(window, 0)
text_xcor = IntVar(window, 0)
text_ycor = IntVar(window, 0)
aspect = IntVar(window, 1)
text_size = IntVar(window, 60)
logo_opacity = DoubleVar(window, 0.0)
colour_var = StringVar(window, "#f0a00c20")

canvas = Canvas(window, width=840, height=640)
canvas.grid(row=0, column=0, rowspan=7)


class WatermarkCreator:
    def __init__(self) -> None:
        self.original_image = None
        self.preview_image = None
        self.image_container = None


watermark_creator = WatermarkCreator()


def select_files(watermark_creator: WatermarkCreator):
    filetypes = (("image files", "*.jpg"), ("image files", "*.png"))
    filenames = fd.askopenfilenames(
        title="Open files", initialdir="./images", filetypes=filetypes
    )
    original_image = Image.open(filenames[0]).convert("RGBA")
    watermark_creator.original_image = original_image
    make_preview(watermark_creator=watermark_creator)


canvas_preview_image = None


def make_preview(watermark_creator: WatermarkCreator):
    if watermark_creator.original_image.width > 840:
        aspect.set(round(watermark_creator.original_image.width / 840))
        print(aspect.get())
    if watermark_creator.original_image.height > 640:
        aspect.set(round(watermark_creator.original_image.height / 640))
        print(aspect.get())

    preview_image = watermark_creator.original_image.copy().reduce(aspect.get())

    if preview_image.width > 840 or preview_image.height > 640:
        aspect.set(aspect.get() + 1)
        preview_image = watermark_creator.original_image.copy().reduce(aspect.get())
        print(aspect.get())

    # NOTE: canvas doesn't work with a local variable being passed in, that's why we need the global definition
    global test
    canvas_preview_image = ImageTk.PhotoImage(preview_image)
    watermark_creator.image_container = canvas.create_image(
        0, 0, image=canvas_preview_image, anchor=NW
    )
    watermark_creator.preview_image = preview_image


upload_img = Button(
    width=50,
    text="Upload image ",
    font=("", 12),
    # command=select_files,
    command=lambda: select_files(watermark_creator=watermark_creator),
)
upload_img.grid(column=1, row=0, columnspan=4, padx=10, pady=10)

font_size = Label(text="Choose font size: ", font=("", 13))
font_size.grid(column=1, row=1)

choose_text_size = Scale(
    from_=20,
    to=60,
    tickinterval=10,
    orient=HORIZONTAL,
    width=23,
    length=300,
    resolution=10,
    command=lambda: text_size.set(choose_text_size.get()),
)
choose_text_size.grid(row=1, column=2, columnspan=3)

choose_color = Button(
    text="Select text colour",
    width=18,
    font=("", 12),
    # command=change_color,
)
choose_color.grid(column=1, row=2)

opacity = Scale(
    from_=20,
    to=100,
    tickinterval=20,
    orient=HORIZONTAL,
    width=23,
    length=300,
    resolution=20,
    # command=opacity,
)
opacity.grid(row=2, column=2, columnspan=3)

add_text = Label(text="Add watermark text: ", font=("", 13))
add_text.grid(column=1, row=3)

e_text = Entry(width=25, font=("Helvetica", 18), textvariable=my_var)
e_text.grid(column=2, row=3, columnspan=3)

my_var.trace("w", lambda *args: character_limit(my_var))

upload_image = Button(
    text="Add logo image",
    font=("Helvetica", 12),
    width=20,
    command=add_logo,
)
upload_image.grid(column=1, row=4)

adjust = Label(text="Adjust logo position with arrows", font=("Ariel.ttf", 13))
adjust.grid(column=2, row=4, columnspan=3)

save_image = Button(
    width=50,
    text="Save image ",
    font=("Ariel.ttf", 12),
    # command=lambda: save_imagez(original_image),
)
save_image.grid(column=1, row=5, columnspan=4)

save_all = Button(
    width=50,
    text="Set automatically watermark to all images",
    font=("Ariel.ttf", 12),
    # command=save_original_images,
)
save_all.grid(column=1, row=6, columnspan=4)

my_var.trace_add("write", on_key)

# window.bind("<Left>", left)
# window.bind("<Right>", right)
# window.bind("<Up>", up)
# window.bind("<Down>", down)
# # canvas.bind("<B1-Motion>", motion)
# canvas.bind("<B1-Motion>", motion_text)
window.mainloop()
