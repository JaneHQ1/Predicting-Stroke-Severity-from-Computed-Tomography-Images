"""
    Use matplotlib to plot x and y plane
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

data_path = r"C:\Users\Jin\Downloads\Predicting-Stroke-Severity-from-Computed-Tomography-Images-master\Series 002 [CT - Crane SPC]"
dcms = load_scan(data_path)
image = np.stack([s.pixel_array for s in dcms])
print(image.shape)

plane_xz=np.zeros((512,142,512))


def voxel_xz(image):
    for y in range(512):
        for z in range(142):
            for x in range(512):
                plane_xz.itemset((y,z,x), image[z][x][y])
                # voxel=np.stack(plane)
    return plane_xz

xz_image=voxel_xz(image)
print(xz_image)
print(xz_image.shape)
a=1
