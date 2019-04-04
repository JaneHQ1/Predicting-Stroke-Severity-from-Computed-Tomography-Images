import sys
from PyQt5 import QtWidgets, QtCore
from matplotlib import widgets
import nibabel as nib
import numpy as np
# from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from imdisplay import *
from roi_controller import *
from cursor_controller import *

if __name__ == '__main__':
    path = r"D:\nifti_2\ARTERIELLE.nii"
    struct = nib.load(path)
    struct_arr = struct.get_fdata()

    tran_arr = struct_arr.transpose(2, 1, 0)
    fron_arr = struct_arr.transpose(1, 2, 0)
    sagi_arr = struct_arr.transpose(0, 2, 1)

    vol_tran = np.flip(tran_arr)
    vol_fron = np.flip(fron_arr)
    vol_sagi = np.flip(sagi_arr)

    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()

    fig = Figure()
    canvas = FigureCanvasQTAgg(fig)
    # for key event
    canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
    canvas.setFocus()

    ax_tran = fig.add_subplot(221, adjustable='box', aspect='auto')
    ax_fron = fig.add_subplot(325, adjustable='box', aspect='auto')
    ax_sagi = fig.add_subplot(326, adjustable='box', aspect='auto')

    # index = vol_tran.shape[0] // 2
    imdis = ImageDisplay(vol_tran, vol_fron, vol_sagi, ax_tran, ax_fron, ax_sagi)
    imdis.initialize_transverse_display()
    imdis.initialize_frontal_display()
    imdis.initialize_sagittal_display()

    # roi = ROI(fig, ax_sagi)
    ctrl_roi = ControlROI(fig, imdis,  vol_tran, vol_fron, vol_sagi, ax_tran, ax_fron, ax_sagi)
    # ctrl_cursor = ControlSys(fig, imdis,  vol_tran, vol_fron, vol_sagi, ax_tran, ax_fron, ax_sagi)

    # Needed for keyboard events
    # canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
    # canvas.setFocus()
    win.setCentralWidget(canvas)
    win.show()
    sys.exit(app.exec_())

