"""
Use Matplotlib display dicom
"""
import sys
from PyQt5 import QtWidgets, QtCore
from matplotlib import widgets
from matplotlib.widgets import RectangleSelector

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


class ROI():
    def __init__(self, fig):
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.fig = fig

    def rec_select(self, ax):
        self.RS = RectangleSelector(ax, self.line_select_callback,
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
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (self.x1, self.y1, self.x2, self.y2))

    def toggle_selector(self, event):
        print(' Key pressed.')
        # if event.key == 'enter':
        #     print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (self.x1, self.y1, self.x2, self.y2))
        if event.key in ['enter'] and self.RS.active:
            print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (self.x1, self.y1, self.x2, self.y2))
            # self.RS.set_active(False)

class ControlSys(ROI):
    def __init__(self, fig, ax, vol_tran, tran_view):
        self.fig = fig
        self.vol_tran = vol_tran
        self.tran_view = tran_view
        self.index = vol_tran.shape[0] // 2
        self.ax = ax

        ROI.__init__(self, self.fig)

        self.fig.canvas.mpl_connect('scroll_event', self.mouse_scroll)
        self.rec_select(self.ax)

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
    path = r"D:\nifti_2\ARTERIELLE.nii"
    struct = nib.load(path)
    struct_arr = struct.get_fdata()
    tran_arr = struct_arr.transpose(2, 1, 0)
    vol_tran = np.flip(tran_arr)

    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()

    fig = Figure()
    canvas = FigureCanvasQTAgg(fig)
    canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
    canvas.setFocus()
    ax = fig.add_subplot(1, 1, 1)

    # index = vol_tran.shape[0] // 2
    tran_view = TranDisplay(ax, vol_tran)
    tran_view.initialize_display(ax, vol_tran)
    # tran_view.update_display(0)
    ctrl_sys = ControlSys(fig, ax, vol_tran, tran_view)
    # x1, x2, y1, y2 = RectangleSelector(ax, ROI.line_select_callback,
    #                        drawtype='box', useblit=True,
    #                        button=[1, 3],  # don't use middle button
    #                        minspanx=5, minspany=5,
    #                        spancoords='pixels',
    #                        interactive=True)


    # Needed for keyboard events
    # canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
    # canvas.setFocus()
    win.setCentralWidget(canvas)
    win.show()
    sys.exit(app.exec_())

