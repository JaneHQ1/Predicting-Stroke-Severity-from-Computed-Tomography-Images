# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 12:47:30 2019
Title: MP4-Medical Image Processing
@author: MP4 Team

"""
# Region of interest class
from matplotlib.patches import Rectangle

class ROI(object):
    def __init__(self, ax, roi_data, pat_id, ax_name, ax_index):
        self.ax = ax
        self.roi_data = roi_data
        self.pat_id = pat_id
        self.ax_name = ax_name
        self.ax_index = ax_index
        
        self.rect = Rectangle((0, 0), 1, 1, facecolor='None', edgecolor='red')
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.is_pressed = False
        self.ax.add_patch(self.rect)
        
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
    def on_press(self, event):
        self.is_pressed = True
        self.x1 = event.xdata
        self.y1 = event.ydata

    def on_motion(self, event):
        if self.is_pressed == True:
            self.x2 = event.xdata
            self.y2 = event.ydata
            self.rect.set_width(self.x2 - self.x1)
            self.rect.set_height(self.y2 - self.y1)
            self.rect.set_xy((self.x1, self.y1))
            self.rect.set_linestyle('dashed')
            self.ax.figure.canvas.draw()
            
    def on_release(self, event):
        self.is_pressed = False
        self.x2 = event.xdata
        self.y2 = event.ydata
        self.rect.set_width(self.x2 - self.x1)
        self.rect.set_height(self.y2 - self.y1)
        self.rect.set_xy((self.x1, self.y1))
        self.rect.set_linestyle('solid')
        self.ax.figure.canvas.draw()
        
        # Append axes name and two rectangluar coordinates
        self.roi_data.append([self.pat_id, self.ax_name, self.ax_index[-1], int(self.x1), int(self.y1), int(self.x2), int(self.y2)])
        
# Single window controller
class SingleWindowCtr(ROI):
    # Initialization
    def __init__(self, fig, im_single, vol_data, ax_single, ax_index, roi_data, pat_id, ax_name):
        self.fig = fig
        self.im_single = im_single
        self.vol_data = vol_data
        self.ax_single = ax_single
        self.ax_index = ax_index
        self.roi_data = roi_data
        self.pat_id = pat_id
        self.ax_name = ax_name
        
        self.scroll_single = None
        self.txt_single = self.ax_single.text(0, -10, 'Slice No: '+str(self.ax_index[-1]), color='b')
        self.fig.canvas.mpl_connect('axes_enter_event', self.fig_enter_event)
        self.fig.canvas.mpl_connect('axes_leave_event', self.fig_leave_event)
        
    # Enable scrolling image
    def fig_enter_event(self, event):
        self.scroll_single = self.fig.canvas.mpl_connect('scroll_event', self.single_plane_scroll)
        ROI.__init__(self, self.ax_single, self.roi_data, self.pat_id, self.ax_name, self.ax_index)
        
    # Disable scrolling image
    def fig_leave_event(self, event):
        self.fig.canvas.mpl_disconnect(self.scroll_single)

    # Scroll image
    def single_plane_scroll(self, event):       
        if event.button == 'down' and (self.ax_index[-1] > -1*self.vol_data.shape[0]):
            self.ax_index[-1] -= 1
            
        if event.button == 'up' and (self.ax_index[-1] < self.vol_data.shape[0]-1):
            self.ax_index[-1] += 1
            
        self.im_single.set_data(self.vol_data[self.ax_index[-1]])
        self.txt_single.set_text('Slice No: '+str(self.ax_index[-1])) 
        self.fig.canvas.draw_idle()