import tkinter as tk

# Dimensiones de la ventana y del terreno
ANCHO = 600
ALTO = 400
NUM_PIXELES = 10  # Número de puntos por lado

class TerrenoApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg='white')
        self.canvas.pack()

        # Dibujar el terreno
        self.dibujar_terreno()

    def dibujar_terreno(self):
        # Calcular el tamaño de cada pixel
        ancho_pixel = ANCHO // NUM_PIXELES
        alto_pixel = ALTO // NUM_PIXELES

        # Dibujar cada punto o pixel en el terreno
        for fila in range(NUM_PIXELES):
            for columna in range(NUM_PIXELES):
                x1 = columna * ancho_pixel
                y1 = fila * alto_pixel
                x2 = x1 + ancho_pixel
                y2 = y1 + alto_pixel
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='green')

if __name__ == "__main__":
    root = tk.Tk()
    app = TerrenoApp(root)
    root.mainloop()
