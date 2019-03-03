# -*- coding: utf-8 -*-
"""
Navigation bar
"""
from tkinter import *
from PIL import ImageTk, Image

class Navbar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.init_navbar()
        
    def init_navbar(self):
        self.master.title("3D Medical Image Analyzer")
        self.pack(fill=BOTH, expand=1)
        
        navbar = Menu(self.master)
        self.master.config(menu = navbar)
        
        file = Menu(navbar)
        file.add_command(label="Open")
        file.add_command(label="Exit", command=self.close_win)
        navbar.add_cascade(label="File", menu=file)
        
        edit = Menu(navbar)
        # edit.add_command(label="Load Image", command=self.show_img)
        edit.add_command(label="Show Text", command=self.show_txt)
        navbar.add_cascade(label="Edit", menu=edit)
        
    def close_win(self):
        self.master.destroy()
    '''
    def show_img(self):
        load_img =Image.open("medical_images/tp.jpg")
        resize_img = load_img.resize((400, 300), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(resize_img)
        img = Label(self, image=render)
        img.image = render
        img.place(x=10, y=10)
        
        load_img =Image.open("medical_images/sp.jpg")
        resize_img = load_img.resize((400, 300), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(resize_img)
        img = Label(self, image=render)
        img.image = render
        img.place(x=10, y=310)
        
        load_img =Image.open("medical_images/cp.jpg")
        resize_img = load_img.resize((400, 300), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(resize_img)
        img = Label(self, image=render)
        img.image = render
        img.place(x=410, y=310)
        
        #img.pack(side = LEFT)
    '''
    def show_txt(self):
        text = Label(self, text="Transverse Plane")
        text.pack(side = LEFT)
        
# def main():
#     root = Tk()
#     root.geometry("800x600")
#     app = Navbar(root)
#     root.mainloop()
#
# if __name__ == '__main__':
#     main()
    