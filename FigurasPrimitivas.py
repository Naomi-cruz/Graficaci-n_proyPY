from tkinter import *
from tkinter import colorchooser

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Figuras primitivas")
        self.canvas = Canvas(self.master, width=800, height=400)
        self.canvas.pack()
        self.shape = None
        self.start_x = 0
        self.start_y = 0
        self.color = 'black'
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)

        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    def start_drawing(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def draw(self, event):
        if self.shape:
            self.canvas.delete(self.shape)

        shape_type = shape_var.get()

        if shape_type == "Linea":
            self.shape = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color)
        elif shape_type == "Cuadrado":
            self.shape = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, fill=self.color)
        elif shape_type == "Triangulo":
            self.shape = self.canvas.create_polygon(self.start_x, self.start_y, event.x, event.y, self.start_x, event.y, fill=self.color)
        elif shape_type == "Rectangulo":
            self.shape = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, fill=self.color)

    def scale_shape(self):
        scale_factor = float(scale_factor_entry.get())
        self.canvas.scale(self.shape, self.start_x, self.start_y, scale_factor, scale_factor)

    def translate_shape(self):
        dx = int(translate_x_entry.get())
        dy = int(translate_y_entry.get())
        self.canvas.move(self.shape, dx, dy)

    def choose_color(self):
        _, self.color = colorchooser.askcolor()

root = Tk()
shape_var = StringVar()
shape_var.set("Linea")

app = DrawingApp(root)

shape_label = Label(root, text="Figura:")
shape_label.pack(side=LEFT)

shape_options = OptionMenu(root, shape_var, "Linea", "Cuadrado", "Triangulo", "Rectangulo")
shape_options.pack(side=LEFT)

color_button = Button(root, text="Seleccionar Color", command=app.choose_color)
color_button.pack(side=LEFT)

scale_label = Label(root, text="Aumentar tamaño:")
scale_label.pack(side=LEFT)

scale_factor_entry = Entry(root)
scale_factor_entry.pack(side=LEFT)

scale_button = Button(root, text="Aceptar", command=app.scale_shape)
scale_button.pack(side=LEFT)

translate_label = Label(root, text="Trasladar:")
translate_label.pack(side=LEFT)

translate_x_entry = Entry(root)
translate_x_entry.pack(side=LEFT)

translate_y_entry = Entry(root)
translate_y_entry.pack(side=LEFT)

translate_button = Button(root, text="Aceptar", command=app.translate_shape)
translate_button.pack(side=LEFT)

root.mainloop()