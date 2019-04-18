# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 12:47:30 2019
Title: MP4-Medical Image Processing
@author: MP4 Team

"""
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from matplotlib.widgets import RectangleSelector

# Draw rectangle around Region of Interest
class RectSelector():
    def __init__(self, fig, axes, patient_id):
        self.fig = fig
        self.ax = axes
        self.patient_id = patient_id
        
        self.roi = RectangleSelector(self.ax, self.start_end_select, drawtype='box', useblit=True,
                                    button=[1, 3],  # don't use middle button
                                    minspanx=5, minspany=5, spancoords='pixels', interactive=True)
        
    # Select start and end Coordinate of the rectangle
    def start_end_select(self, eclick, erelease):
        #eclick and erelease are the press and release events
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        
        text_file = open('roi_ax_data.txt', 'a')
        text_file.write(self.patient_id[0] + '     ')
        text_file.write(str(self.ax) + '     ')
        text_file.write('(%5.4f, %5.4f)   (%5.4f, %5.4f)' % (x1, y1, x2, y2))
        text_file.write('\n')
        text_file.close()

        