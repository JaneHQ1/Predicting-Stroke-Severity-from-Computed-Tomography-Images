"""
    Use matplotlib to plot x and y plane in pixel
"""

import pydicom
import numpy as np
# from pydicom.data import get_testdata_files
# import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import os


def load_scan(path):
    slices = [pydicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key=lambda x: int(x.InstanceNumber))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices:
        s.SliceThickness = slice_thickness

    return slices


# def create_voxel_array(dcms):
#     image = np.stack([s.pixel_array for s in dcms])
#     return image


def update_frontal(val):
    index = int(s_index.val)
    canvas_frontal.set_data(voxel_frontal[index, :])
    plt.draw()



data_path = r"C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\Series 002 [CT - Crane SPC]"
dcms = load_scan(data_path)
image = np.stack([s.pixel_array for s in dcms])
# print(voxel.shape)
# print(voxel)
# print(voxel[0][0][0])
voxel_frontal = image.transpose(1, 0, 2)
# print(voxel_frontal[95][100][102])
# print(voxel_frontal[0,:])


canvas_frontal = plt.imshow(voxel_frontal[0, :], cmap=plt.cm.bone)
ax_index = plt.axes([0.15, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
s_index = Slider(ax_index, 'Index', 0, 511, valinit=0, valstep=1)
s_index.on_changed(update_frontal)

plot = plt.show()

