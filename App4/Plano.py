import tkinter as tk
from Pixel import Pixel  # Importa la clase Pixel desde el archivo Pixel.py

class Plano(tk.Canvas):
    def __init__(self, parent, lx, ly, grid_scale):
        super().__init__(parent, width=lx*grid_scale, height=ly*grid_scale, bg='white')
        self.lx = lx
        self.ly = ly
        self.grid_scale = grid_scale
        self.pixeles_origen = []
        self.paint_grilla()

    def paint_pixel(self, x, y, color='green'):
        x1 = x * self.grid_scale
        y1 = y * self.grid_scale
        x2 = x1 + self.grid_scale
        y2 = y1 + self.grid_scale
        self.create_rectangle(x1, y1, x2, y2, outline='black', fill=color)

    def push_pixel_origen(self, x, y, color='red'):
        self.pixeles_origen.append(Pixel(x, y, self.grid_scale, color))  # Instancia un nuevo objeto Pixel
        self.repaint_pixeles_origen()

    def pop_pixel_origen(self):
        if self.pixeles_origen:
            self.pixeles_origen.pop()
            self.repaint_pixeles_origen()

    def peek_pixel_origen(self):
        if self.pixeles_origen:
            return self.pixeles_origen[-1]
        return None

    def clear_pixeles_origen(self):
        self.pixeles_origen = []
        self.repaint_pixeles_origen()

    def repaint_pixeles_origen(self):
        self.delete("all")
        self.paint_grilla()  # Vuelve a pintar la grilla antes de los píxeles
        for pixel in self.pixeles_origen:
            pixel.paintFill(self)

    def paint_grilla(self):
        for i in range(self.lx):
            for j in range(self.ly):
                x1 = i * self.grid_scale
                y1 = j * self.grid_scale
                x2 = x1 + self.grid_scale
                y2 = y1 + self.grid_scale
                self.create_rectangle(x1, y1, x2, y2, outline="gray", fill="white")
