import tkinter as tk

class Pixel:
    def __init__(self, x, y, width, color="red"):
        self.x = x
        self.y = y
        self.width = width
        self.color = color

    def paintFill(self, canvas):
        x1 = self.x * self.width
        y1 = self.y * self.width
        x2 = x1 + self.width
        y2 = y1 + self.width
        canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill=self.color)
