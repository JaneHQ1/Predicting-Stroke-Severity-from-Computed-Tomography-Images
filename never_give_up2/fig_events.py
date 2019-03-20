'''
update image
'''
import numpy as np
import matplotlib.pyplot as plt

'''
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


'''
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

        self.txt_tran = ax_tran.text(0.7, 0.9, '', color='b')
        self.txt_fron = ax_fron.text(0.7, 0.9, '', color='b')

    def control_events(self, event):
        fig = event.canvas.figure
        ax_tran = fig.axes[0]
        ax_fron = fig.axes[1]
        ax_sagi = fig.axes[2]
        x_index = np.int_(event.xdata)
        y_index = np.int_(event.ydata)

        if ax_tran.contains(event)[0]:
            plt.connect('button_press_event', self.mouse_cursor(event))
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


    def mouse_cursor(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        z = self.ax_tran.index
        # update the line positions
        self.lx_tran.set_ydata(y)
        self.ly_tran.set_xdata(x)

        self.txt_tran.set_text('x=%1d y=%1d z=%1d' % (x, y, z))
        plt.draw()




'''
class Cursor(object):
    def __init__(self, ax_tran, ax_fron, ax_sagi, vol_tran, vol_fron, vol_sagi):
        self.ax_tran = ax_tran
        self.ax_fron = ax_fron
        self.ax_sagi = ax_sagi

        self.tran = vol_tran
        self.tran = vol_fron
        self.tran = vol_sagi

        self.ax_tran.index = vol_tran.shape[0] // 2
        self.ax_fron.index = vol_fron.shape[0] // 2
        self.ax_sagi.index = vol_sagi.shape[0] // 2

        self.lx_tran = ax_tran.axhline(color='b', linewidth=0.8)
        self.ly_tran = ax_tran.axvline(color='b', linewidth=0.8)
        self.lx_fron = ax_fron.axhline(color='b')
        self.ly_fron = ax_fron.axvline(color='b')

        self.txt = self.ax_tran.text(0.7, 0.9, '', transform=self.ax_tran.transAxes, color='b')
        self.txt = self.ax_fron.text(0.7, 0.9, '', transform=self.ax_fron.transAxes, color='b')

    def check(self, event):

        if self.ax_tran.contains(event)[0]:
            x, y = event.xdata, event.ydata
            z = self.ax_tran.index
            plt.connect('button_press_event', self.mouse_cursor(event, x, y, z))

        elif self.ax_fron.contains(event)[0]:
            pass

        elif self.ax_sagi.contains(event)[0]:
            pass

    def mouse_cursor(self, event, x, y, z):
        if not event.inaxes:
            return

        # x, y = event.xdata, event.ydata
        # z = self.ax.index
        # update the line positions
        self.lx_tran.set_ydata(y)
        self.ly_tran.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f, z=%1.2f' (x, y, z))
        plt.draw()
'''








