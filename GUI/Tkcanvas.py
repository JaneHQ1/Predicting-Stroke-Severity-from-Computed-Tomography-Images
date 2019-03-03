"""
Tkinter Canvas
"""
from GUI.Navbar import *
from tkinter import *
# from GUI.Matplot import *

import matplotlib as mpl
import matplotlib.pyplot as plt
# import mat
import numpy as np
import tkinter as tk
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

'''
def main():
    root = Tk()
    root.geometry("800x600")
    app = Navbar(root)
    root.mainloop()

if __name__ == '__main__':
    main()
'''



# Create a canvas
w, h = 800, 600
window = tk.Tk()
# window.title("A figure in a canvas")
app = Navbar(window)
canvas = tk.Canvas(window, width=w, height=h)
canvas.pack()




# Let Tk take over
tk.mainloop()