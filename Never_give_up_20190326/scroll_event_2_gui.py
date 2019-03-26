"""
Use Matplotlib display dicom
"""
import sys
from PyQt5 import QtWidgets
from matplotlib import widgets

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class TranDisplay(object):
    def __init__(self, ax, vol_tran):
        self.im = None
        self.ax = ax
        self.vol_tran = vol_tran
        # self.initialize_display(ax, vol_tran, index)

    def initialize_display(self, ax, vol_tran):
        if self.im is not None:
            self.im.remove()
        self.im = ax.imshow(vol_tran[0], cmap="gray")

    def update_display(self, data):
        self.im.set_data(self.vol_tran[data])


# class EventControl:
#     pass


class ButtonControl:
    def __init__(self, fig):
        self.fig = fig

    def build_slider_bar(self, fig):
        barax = fig.add_axes([0.226, 0.005, 0.572, 0.02], facecolor='lightgoldenrodyellow')
        bar = widgets.Slider(barax, 'Index', 0, 300, valinit=0, valstep=1)
        return bar

class ControlSys(ButtonControl):
    def __init__(self, fig, vol_tran, tran_view):
        self.fig = fig
        self.vol_tran = vol_tran
        self.tran_view = tran_view
        self.index = vol_tran.shape[0] // 2

        ButtonControl.__init__(self, fig)
        # self.slider_bar = self.build_slider_bar(fig)
        # self.slider_bar.on_changed(self.update_im)

        self.fig.canvas.mpl_connect('scroll_event', self.mouse_scroll)

    def mouse_scroll(self, event):
        # if event.inaxes is not self.tran_view.im.get_axes():
        #     return

        if event.button == 'down':
            self.index -= 1
        if event.button == 'up':
            self.index += 1
        self.update_im(self.index)


    def update_im(self, index):
        # self.slider_bar.set_val(index)
        self.tran_view.update_display(int(index))
        self.fig.canvas.draw_idle()


if __name__ == '__main__':
    path = r"C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\TestSample\nifti_2\ARTERIELLE.nii.gz"
    struct = nib.load(path)
    struct_arr = struct.get_fdata()
    tran_arr = struct_arr.transpose(2, 1, 0)
    vol_tran = np.flip(tran_arr)

    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()

    fig = Figure()
    canvas = FigureCanvasQTAgg(fig)
    ax = fig.add_subplot(1, 1, 1)

    # index = vol_tran.shape[0] // 2
    tran_view = TranDisplay(ax, vol_tran)
    tran_view.initialize_display(ax, vol_tran)
    # tran_view.update_display(0)
    ctrl_sys = ControlSys(fig, vol_tran, tran_view)

    # Needed for keyboard events
    # canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
    # canvas.setFocus()
    win.setCentralWidget(canvas)
    win.show()
    sys.exit(app.exec_())

