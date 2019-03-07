"""
    Use matplotlib to plot x and y plane
"""

import pydicom
import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.ndimage
from skimage import morphology
from skimage import measure
from skimage.transform import resize
# from sklearn.cluster import KMeans
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.tools import FigureFactory as FF
from plotly.graph_objs import *


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


def voxel_3d_pixel(dcms,j):
    voxel_list = []
    row_vector = dcms[j].ImageOrientationPatient[0:3]
    column_vector = dcms[j].ImageOrientationPatient[3:6]
    pixel_size = list(map(float, list(dcms[j].PixelSpacing)))


    pixel_size_x = pixel_size[0]
    pixel_size_y = pixel_size[1]
    image_position_patient = [float(i) for i in list(dcms[j].ImagePositionPatient)]

    for m in range(dcms[j].Rows):
        pixel_location_x = m
        row_change_x = [i * pixel_size_x * float(pixel_location_x) for i in row_vector]
        # print(row_change_x)

        for n in range(dcms[j].Columns):
            pixel_location_y = n
            row_change_y = [i * pixel_size_y * float(pixel_location_y) for i in column_vector]
            # print(row_change_y)
            voxel = list(map(lambda x: x[0] + x[1] + x[2], list(zip(image_position_patient, row_change_x, row_change_y))))
            voxel_list.append(voxel)

    return voxel_list


id = 0
data_path = r"C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\test_images10"
patient = load_scan(data_path)
voxel_list = voxel_3d_pixel(patient, 0)
print(voxel_list)
# t = np.array(voxel_list).shape
# print(t)

