import tkinter as tk
from tkinter import ttk
from Plano import Plano

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Demo de Plano con Puntos y Píxeles")
        self.geometry("600x400")

        self.plano = Plano(self, lx=10, ly=10, grid_scale=30)
        self.plano.pack(pady=20)

        self.btn_paint_pixel = ttk.Button(self, text="Pintar Píxel", command=self.paint_pixel)
        self.btn_paint_pixel.pack()

        self.btn_push_pixel = ttk.Button(self, text="Agregar Píxel de Origen", command=self.push_pixel_origen)
        self.btn_push_pixel.pack()

        self.btn_pop_pixel = ttk.Button(self, text="Eliminar Último Píxel de Origen", command=self.pop_pixel_origen)
        self.btn_pop_pixel.pack()

        self.btn_clear_pixels = ttk.Button(self, text="Limpiar Píxeles de Origen", command=self.clear_pixeles_origen)
        self.btn_clear_pixels.pack()

    def paint_pixel(self):
        x = int(input("Ingrese la coordenada x del píxel: "))
        y = int(input("Ingrese la coordenada y del píxel: "))
        self.plano.paint_pixel(x, y)

    def push_pixel_origen(self):
        x = int(input("Ingrese la coordenada x del píxel de origen: "))
        y = int(input("Ingrese la coordenada y del píxel de origen: "))
        self.plano.push_pixel_origen(x, y)

    def pop_pixel_origen(self):
        self.plano.pop_pixel_origen()

    def clear_pixeles_origen(self):
        self.plano.clear_pixeles_origen()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()