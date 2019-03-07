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

data_path = r"C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\Series 002 [CT - Crane SPC]"
dcms = load_scan(data_path)
image = np.stack([s.pixel_array for s in dcms])

