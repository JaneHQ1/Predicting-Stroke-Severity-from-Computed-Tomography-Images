import numpy as np
import matplotlib.pyplot as plt

class ImageDisplay(object):
    def __init__(self, vol_tran, vol_fron, vol_sagi, ax_tran, ax_fron, ax_sagi):
        self.im_tran = None
        self.im_fron = None
        self.im_sagi = None

        self.vol_tran = vol_tran
        self.vol_fron = vol_fron
        self.vol_sagi = vol_sagi

        self.ax_tran = ax_tran
        self.ax_fron = ax_fron
        self.ax_sagi = ax_sagi

        self.ax_tran.index = self.vol_tran.shape[0] // 2
        self.ax_fron.index = self.vol_fron.shape[0] // 2
        self.ax_sagi.index = self.vol_sagi.shape[0] // 2

    def initialize_transverse_display(self):
        if self.im_tran is not None:
            self.im_tran.remove()
        self.im_tran = self.ax_tran.imshow(self.vol_tran[self.ax_tran.index], cmap="gray")

    def initialize_frontal_display(self):
        if self.im_fron is not None:
            self.im_fron.remove()
        self.im_fron = self.ax_fron.imshow(self.vol_fron[self.ax_fron.index], cmap="gray")

    def initialize_sagittal_display(self):
        if self.im_sagi is not None:
            self.im_sagi.remove()
        self.im_sagi = self.ax_sagi.imshow(self.vol_sagi[self.ax_fron.index], cmap="gray")

    def update_transverse_display(self, index):
        self.im_tran.set_data(self.vol_tran[index])

    def update_frontal_display(self, index):
        self.im_fron.set_data(self.vol_fron[index])

    def update_sagittal_display(self, index):
        self.im_sagi.set_data(self.vol_sagi[index])

