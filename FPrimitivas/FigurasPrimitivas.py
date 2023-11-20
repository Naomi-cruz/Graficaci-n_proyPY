from tkinter import *
from tkinter import colorchooser
import math

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Figuras primitivas")
        self.master.geometry("800x600")
        self.master.resizable(False, False)
        self.canvas = Canvas(self.master, width=500, height=600)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.shapes = []  # Lista para almacenar las figuras
        self.color = 'black'
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.finalize_shape)

        # Contenedor para botones y lista de figuras
        self.side_frame = Frame(self.master, width=200, height=600)
        self.side_frame.pack_propagate(False)  # Evitar que el Frame se ajuste automáticamente al contenido
        self.side_frame.pack(side=RIGHT, fill=BOTH)

        # Lista de figuras
        self.listbox_label = Label(self.side_frame, text="Lista de figuras")
        self.listbox_label.pack()

        self.listbox = Listbox(self.side_frame, width=30, selectmode=SINGLE)
        self.listbox.pack(fill=BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_listbox_select)

        # Configuración del contenedor para los botones
        self.button_frame = Frame(self.side_frame)
        self.button_frame.pack(fill=BOTH)

        shape_label = Label(self.button_frame, text="Figura:")
        shape_label.pack()

        self.shape_var = StringVar()
        shape_options = OptionMenu(self.button_frame, self.shape_var, "Linea", "Cuadrado", "Triangulo", "Rectangulo")
        shape_options.pack(fill=BOTH)

        color_button = Button(self.button_frame, text="Seleccionar Color", command=self.choose_color)
        color_button.pack(fill=BOTH)

        scale_label = Label(self.button_frame, text="Aumentar tamaño:")
        scale_label.pack()

        self.scale_factor_entry = Entry(self.button_frame)
        self.scale_factor_entry.pack(fill=BOTH)

        scale_button = Button(self.button_frame, text="Aceptar", command=self.scale_shape)
        scale_button.pack(fill=BOTH)

        translate_label = Label(self.button_frame, text="Trasladar:")
        translate_label.pack()

        self.translate_x_entry = Entry(self.button_frame)
        self.translate_x_entry.pack(fill=BOTH)

        self.translate_y_entry = Entry(self.button_frame)
        self.translate_y_entry.pack(fill=BOTH)

        translate_button = Button(self.button_frame, text="Aceptar", command=self.translate_shape)
        translate_button.pack(fill=BOTH)

        rotate_label = Label(self.button_frame, text="Rotar (grados):")
        rotate_label.pack()

        self.rotate_angle_entry = Entry(self.button_frame)
        self.rotate_angle_entry.pack(fill=BOTH)

        rotate_button = Button(self.button_frame, text="Aceptar", command=self.rotate_shape)
        rotate_button.pack(fill=BOTH)

    def start_drawing(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def finalize_shape(self, event):
        shape_type = self.shape_var.get()

        if shape_type == "Linea":
            shape = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color)
        elif shape_type == "Cuadrado":
            side_length = min(abs(event.x - self.start_x), abs(event.y - self.start_y))
            if event.x < self.start_x:
                self.start_x = event.x
            if event.y < self.start_y:
                self.start_y = event.y
            shape = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x + side_length, self.start_y + side_length, fill=self.color)
        elif shape_type == "Triangulo":
            shape = self.canvas.create_polygon(self.start_x, self.start_y, event.x, event.y, self.start_x, event.y, fill=self.color)
        elif shape_type == "Rectangulo":
            shape = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, fill=self.color)

        shape_info = f"{shape_type}, Color: {self.color}, ID: {shape}"
        self.listbox.insert(END, shape_info)

        self.shapes.append(shape)  # Agregar la figura a la lista

    def scale_shape(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_shape = self.shapes[selected_index[0]]
            scale_factor = float(self.scale_factor_entry.get())
            self.canvas.scale(selected_shape, self.start_x, self.start_y, scale_factor, scale_factor)

    def translate_shape(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_shape = self.shapes[selected_index[0]]
            dx = int(self.translate_x_entry.get())
            dy = int(self.translate_y_entry.get())
            self.canvas.move(selected_shape, dx, dy)

    def rotate_shape(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_shape = self.shapes[selected_index[0]]
            angle = float(self.rotate_angle_entry.get())
            cx, cy = self.get_center(selected_shape)
            self.rotate(selected_shape, cx, cy, angle)

    def choose_color(self):
        _, self.color = colorchooser.askcolor()

    def on_listbox_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_shape = self.shapes[selected_index[0]]
            coords = self.canvas.coords(selected_shape)
            self.start_x, self.start_y = coords[0], coords[1]

    def get_center(self, shape):
        bbox = self.canvas.bbox(shape)
        cx = (bbox[0] + bbox[2]) / 2
        cy = (bbox[1] + bbox[3]) / 2
        return cx, cy

    def rotate(self, shape, cx, cy, angle):
        if self.canvas.type(shape) == "line":
            coords = self.canvas.coords(shape)
            x1, y1, x2, y2 = coords
            x1_rotated, y1_rotated = self.rotate_point(x1, y1, cx, cy, angle)
            x2_rotated, y2_rotated = self.rotate_point(x2, y2, cx, cy, angle)
            self.canvas.coords(shape, x1_rotated, y1_rotated, x2_rotated, y2_rotated)
        elif self.canvas.type(shape) == "rectangle":
            coords = self.canvas.coords(shape)
            x1, y1, x2, y2 = coords
            x1_rotated, y1_rotated = self.rotate_point(x1, y1, cx, cy, angle)
            x2_rotated, y2_rotated = self.rotate_point(x2, y2, cx, cy, angle)
            self.canvas.coords(shape, x1_rotated, y1_rotated, x2_rotated, y2_rotated)
        elif self.canvas.type(shape) == "polygon":
            coords = self.canvas.coords(shape)
            rotated_polygon = self.rotate_polygon(coords, cx, cy, angle)
            self.canvas.coords(shape, *rotated_polygon)

    def rotate_point(self, x, y, cx, cy, angle):
        angle_rad = math.radians(angle)
        x_rotated = cx + (x - cx) * math.cos(angle_rad) - (y - cy) * math.sin(angle_rad)
        y_rotated = cy + (x - cx) * math.sin(angle_rad) + (y - cy) * math.cos(angle_rad)
        return x_rotated, y_rotated

    def rotate_polygon(self, coords, cx, cy, angle):
        rotated_polygon = []
        angle_rad = math.radians(angle)
        for i in range(0, len(coords), 2):
            x = coords[i]
            y = coords[i + 1]
            x_rotated = cx + (x - cx) * math.cos(angle_rad) - (y - cy) * math.sin(angle_rad)
            y_rotated = cy + (x - cx) * math.sin(angle_rad) + (y - cy) * math.cos(angle_rad)
            rotated_polygon.extend([x_rotated, y_rotated])
        return rotated_polygon

root = Tk()
app = DrawingApp(root)
root.mainloop()

