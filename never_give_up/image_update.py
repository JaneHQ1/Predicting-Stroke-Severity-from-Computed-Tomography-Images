'''
update image
'''
import numpy as np

class ImUpdate(object):
    def __init__(self, vol_tran, vol_fron, vol_sagi):
        self.vol_tran = vol_tran
        self.vol_fron = vol_fron
        self.vol_sagi = vol_sagi

    def check_axes(self, event):
        fig = event.canvas.figure
        ax_tran = fig.axes[0]
        ax_fron = fig.axes[1]
        ax_sagi = fig.axes[2]
        x_index = np.int_(event.xdata)
        y_index = np.int_(event.ydata)

        if ax_tran.contains(event)[0]:
            fig.canvas.mpl_connect('button_press_event', self.frontal_view(event, x_index))
            fig.canvas.mpl_connect('button_press_event', self.sagittal_view(event, y_index))

        elif ax_fron.contains(event)[0]:
            fig.canvas.mpl_connect('button_press_event', self.transverse_view(event, y_index))
            fig.canvas.mpl_connect('button_press_event', self.sagittal_view(event, x_index))

        elif ax_sagi.contains(event)[0]:
            fig.canvas.mpl_connect('button_press_event', self.transverse_view(event, y_index))
            fig.canvas.mpl_connect('button_press_event', self.frontal_view(event, x_index))

    def transverse_view(self, event, index):
        fig = event.canvas.figure
        ax_tran = fig.axes[0]
        ax_tran.index = index
        ax_tran.images[0].set_array(self.vol_tran[ax_tran.index])
        fig.canvas.draw()

    def frontal_view(self, event, index):
        fig = event.canvas.figure
        ax_fron = fig.axes[1]
        ax_fron.index = index
        ax_fron.images[0].set_array(self.vol_fron[ax_fron.index])
        fig.canvas.draw()

    def sagittal_view(self, event, index):
        fig = event.canvas.figure
        ax_sagi = fig.axes[2]
        ax_sagi.index = index
        ax_sagi.images[0].set_array(self.vol_sagi[ax_sagi.index])
        fig.canvas.draw()

class Cursor(object):
    def __init__(self, ax_tran, ax_fron, ax_sagi):
        self.ax_tran = ax_tran
        self.ax_fron = ax_fron
        self.ax_sagi = ax_sagi
        





