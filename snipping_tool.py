import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab
import os
import datetime

class SnippingTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snipping Tool")
        self.geometry("300x100")
        self.configure(bg="white")

        self.snip_button = tk.Button(self, text="Snip", command=self.start_snip)
        self.snip_button.pack(pady=20)

    def start_snip(self):
        self.withdraw()
        self.snip_window = SnipWindow(self)

class SnipWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.attributes("-fullscreen", True)
        self.attributes("-alpha", 0.3)
        self.configure(bg="black")

        self.canvas = tk.Canvas(self, cursor="cross", bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.start_x = None
        self.start_y = None
        self.rect = None

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_mouse_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        x1 = int(self.start_x)
        y1 = int(self.start_y)
        x2 = int(self.canvas.canvasx(event.x))
        y2 = int(self.canvas.canvasy(event.y))

        self.destroy()
        self.parent.deiconify()

        self.capture_screen(x1, y1, x2, y2)

    def capture_screen(self, x1, y1, x2, y2):
        bbox = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        img = ImageGrab.grab(bbox)
        
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if filename:
            img.save(filename)

if __name__ == "__main__":
    app = SnippingTool()
    app.mainloop()
