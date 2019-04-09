# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 12:47:30 2019
Title: MP4-Medical Image Processing
@author: MP4 Team

"""
from matplotlib.widgets import RectangleSelector

# ROI class to draw rectangle
class ROI():
    def __init__(self, fig, ax):
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.fig = fig
        self.ax = ax

        self.RS = RectangleSelector(self.ax, self.line_select_callback,
                                    drawtype='box', useblit=True,
                                    button=[1, 3],  # don't use middle button
                                    minspanx=5, minspany=5,
                                    spancoords='pixels',
                                    interactive=True)
        self.fig.canvas.mpl_connect('key_press_event', self.toggle_selector)

    def line_select_callback(self, eclick, erelease):
        'eclick and erelease are the press and release events'
        self.x1, self.y1 = eclick.xdata, eclick.ydata
        self.x2, self.y2 = erelease.xdata, erelease.ydata
        # print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (self.x1, self.y1, self.x2, self.y2))

    def toggle_selector(self, event):
        print(' Key pressed.')
        # if event.key == 'enter':
        #     print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (self.x1, self.y1, self.x2, self.y2))
        if event.key in ['enter'] and self.RS.active:
            print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (self.x1, self.y1, self.x2, self.y2))
            # self.RS.set_active(False)

