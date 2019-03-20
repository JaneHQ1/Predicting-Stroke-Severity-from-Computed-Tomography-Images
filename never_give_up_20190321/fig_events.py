'''
Events:
update images
add cursor
show coordinates
'''
import numpy as np
import matplotlib.pyplot as plt

class ImUpdate(object):
    def __init__(self, vol_tran, vol_fron, vol_sagi, ax_tran, ax_fron, ax_sagi):
        self.vol_tran = vol_tran
        self.vol_fron = vol_fron
        self.vol_sagi = vol_sagi

        self.ax_tran = ax_tran
        self.ax_fron = ax_fron
        self.ax_sagi = ax_sagi

        self.ax_tran.index = vol_tran.shape[0] // 2
        self.ax_fron.index = vol_fron.shape[0] // 2
        self.ax_sagi.index = vol_sagi.shape[0] // 2

        self.lx_tran = ax_tran.axhline(color='b', linewidth=0.8)
        self.ly_tran = ax_tran.axvline(color='b', linewidth=0.8)
        self.lx_fron = ax_fron.axhline(color='b', linewidth=0.8)
        self.ly_fron = ax_fron.axvline(color='b', linewidth=0.8)
        self.lx_sagi = ax_sagi.axhline(color='b', linewidth=0.8)
        self.ly_sagi = ax_sagi.axvline(color='b', linewidth=0.8)

        self.txt_tran = ax_tran.text(1, 1, '', color='b')
        self.txt_fron = ax_fron.text(1, 1, '', color='b')
        self.txt_sagi = ax_sagi.text(1, 1, '', color='b')

    def control_events(self, event):
        fig = event.canvas.figure
        ax_tran = fig.axes[0]
        ax_fron = fig.axes[1]
        ax_sagi = fig.axes[2]
        x_index = np.int_(event.xdata)
        y_index = np.int_(event.ydata)

        if ax_tran.contains(event)[0]:
            plt.connect('button_press_event', self.add_cursor(event, self.ax_tran))
            fig.canvas.mpl_connect('button_press_event', self.frontal_view(event, y_index))
            fig.canvas.mpl_connect('button_press_event', self.sagittal_view(event, x_index))

        elif ax_fron.contains(event)[0]:
            plt.connect('button_press_event', self.add_cursor(event, self.ax_fron))
            fig.canvas.mpl_connect('button_press_event', self.transverse_view(event, y_index))
            fig.canvas.mpl_connect('button_press_event', self.sagittal_view(event, x_index))

        elif ax_sagi.contains(event)[0]:
            plt.connect('button_press_event', self.add_cursor(event, self.ax_sagi))
            fig.canvas.mpl_connect('button_press_event', self.transverse_view(event, y_index))
            fig.canvas.mpl_connect('button_press_event', self.frontal_view(event, x_index))

    def transverse_view(self, event, index):
        fig = event.canvas.figure
        ax_tran = fig.axes[0]
        ax_tran.index = index
        vol_tran = self.vol_tran
        # ax_tran.images[0].set_array(self.vol_tran[ax_tran.index])
        ax_tran.images[0].set_data(self.vol_tran[ax_tran.index])
        fig.canvas.draw()

    def frontal_view(self, event, index):
        fig = event.canvas.figure
        ax_fron = fig.axes[1]
        ax_fron.index = index
        # ax_fron.images[0].set_array(self.vol_fron[ax_fron.index])
        ax_fron.images[0].set_data(self.vol_fron[ax_fron.index])
        fig.canvas.draw()

    def sagittal_view(self, event, index):
        fig = event.canvas.figure
        ax_sagi = fig.axes[2]
        ax_sagi.index = index
        ax_sagi.images[0].set_array(self.vol_sagi[ax_sagi.index])
        fig.canvas.draw()

    def add_cursor(self, event, ax):
        if ax is self.ax_tran:
            # self.ax_fron.index = event.ydata
            # self.ax_sagi.index = event.xdata
            x, y, z = event.xdata, event.ydata, self.ax_tran.index
            coord_tran = [x, y, z]
            coord_fron = [x, z, y]
            coord_sagi = [y, z, x]
            self.plot_cursor(coord_tran, self.lx_tran, self.ly_tran, self.txt_tran)
            self.plot_cursor(coord_fron, self.lx_fron, self.ly_fron, self.txt_fron)
            self.plot_cursor(coord_sagi, self.lx_sagi, self.ly_sagi, self.txt_sagi)

        if ax is self.ax_fron:
            x, y, z = event.xdata, event.ydata, self.ax_fron.index
            coord_fron = [x, y, z]
            coord_tran = [x, z, y]
            coord_sagi = [z, y, x]
            self.plot_cursor(coord_tran, self.lx_tran, self.ly_tran, self.txt_tran)
            self.plot_cursor(coord_fron, self.lx_fron, self.ly_fron, self.txt_fron)
            self.plot_cursor(coord_sagi, self.lx_sagi, self.ly_sagi, self.txt_sagi)

        if ax is self.ax_sagi:
            x, y, z = event.xdata, event.ydata, self.ax_sagi.index
            coord_sagi = [x, y, z]
            coord_tran = [z, x, y]
            coord_fron = [z, y, x]
            self.plot_cursor(coord_tran, self.lx_tran, self.ly_tran, self.txt_tran)
            self.plot_cursor(coord_fron, self.lx_fron, self.ly_fron, self.txt_fron)
            self.plot_cursor(coord_sagi, self.lx_sagi, self.ly_sagi, self.txt_sagi)


    def plot_cursor(self, coord, lx, ly, txt):
        x, y, z = coord[0], coord[1], coord[2]
        lx.set_ydata(y)
        ly.set_xdata(x)

        txt.set_text('x=%1d y=%1d z=%1d' % (x, y, z))
        plt.draw()












