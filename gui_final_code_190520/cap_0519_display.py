# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:49:57 2019
Title: MP4-Medical Image Processing
@author: MP4 Team

"""
#   Class to display the images
class ImageDisplay(object):
    # Initialize the class
    def __init__(self, vol_tran, vol_fron, vol_sagi, ax_tran, ax_fron, ax_sagi, tran_index, fron_index, sagi_index):
        self.vol_tran = vol_tran
        self.vol_fron = vol_fron
        self.vol_sagi = vol_sagi

        self.ax_tran = ax_tran
        self.ax_fron = ax_fron
        self.ax_sagi = ax_sagi
        
        self.tran_index = tran_index
        self.fron_index = fron_index
        self.sagi_index = sagi_index
        
        # Display initial images
        self.im_tran = self.ax_tran.imshow(self.vol_tran[self.tran_index[-1]], cmap="gray")
        self.im_fron = self.ax_fron.imshow(self.vol_fron[self.fron_index[-1]], cmap="gray")
        self.im_sagi = self.ax_sagi.imshow(self.vol_sagi[self.sagi_index[-1]], cmap="gray")
        
    # Update Image based on slice index
    def update_transverse_display(self, index):
        self.im_tran.set_data(self.vol_tran[index])
   
    def update_frontal_display(self, index):
        self.im_fron.set_data(self.vol_fron[index])
        
    def update_sagittal_display(self, index):
        self.im_sagi.set_data(self.vol_sagi[index])
        