# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 12:48:21 2019
Title: MP4-Medical Image Processing
@author: MP4 Team

"""
# Scroll Controller for scrolling image
class ScrollController():
    def __init__(self, fig, im_dis, vol_tran, vol_fron, vol_sagi, ax_tran, ax_fron, ax_sagi, tran_index, fron_index, sagi_index):
        self.fig = fig
        self.im_dis = im_dis

        self.vol_tran = vol_tran
        self.vol_fron = vol_fron
        self.vol_sagi = vol_sagi

        self.ax_tran = ax_tran
        self.ax_fron = ax_fron
        self.ax_sagi = ax_sagi
        
        self.tran_index = tran_index
        self.fron_index = fron_index
        self.sagi_index = sagi_index
        
        self.scroll_tran = None
        self.scroll_fron = None
        self.scroll_sagi = None
        self.fig.canvas.mpl_connect('axes_leave_event', self.fig_leave_event)
        
    # Enable scroll when mouse pointer inside figure
    def fig_enter_event(self, event):
        if self.ax_tran.in_axes(event):
            self.scroll_tran = self.fig.canvas.mpl_connect('scroll_event', self.transverse_scroll)

        elif self.ax_fron.in_axes(event):
            self.scroll_fron = self.fig.canvas.mpl_connect('scroll_event', self.frontal_scroll)

        elif self.ax_sagi.in_axes(event):
            self.scroll_sagi = self.fig.canvas.mpl_connect('scroll_event', self.sagittal_scroll)
            
    # Disable scroll when mouse pointer inside figure
    def fig_leave_event(self, event):
        self.fig.canvas.mpl_disconnect(self.scroll_tran)
        self.fig.canvas.mpl_disconnect(self.scroll_fron)
        self.fig.canvas.mpl_disconnect(self.scroll_sagi)
        
    # Scroll function for three planes
    def transverse_scroll(self, event):
        if event.button == 'down' and (self.tran_index[-1] > -1*self.vol_tran.shape[0]):
            self.tran_index[-1] -= 1
        if event.button == 'up' and (self.tran_index[-1] < self.vol_tran.shape[0]-1):
            self.tran_index[-1] += 1
        self.im_dis.update_transverse_display(self.tran_index[-1])
        self.fig.canvas.draw_idle()
        
    def frontal_scroll(self, event):
        if event.button == 'down' and (self.fron_index[-1] > -1*self.vol_fron.shape[0]):
            self.fron_index[-1] -= 1
        if event.button == 'up' and (self.fron_index[-1] < self.vol_fron.shape[0]-1):
            self.fron_index[-1] += 1
        self.im_dis.update_frontal_display(self.fron_index[-1])
        self.fig.canvas.draw_idle()
        
    def sagittal_scroll(self, event):
        if event.button == 'down' and (self.sagi_index[-1] > -1*self.vol_sagi.shape[0]):
            self.sagi_index[-1] -= 1
        if event.button == 'up' and (self.sagi_index[-1] < self.vol_sagi.shape[0]-1):
            self.sagi_index[-1] += 1
        self.im_dis.update_sagittal_display(self.sagi_index[-1])
        self.fig.canvas.draw_idle()