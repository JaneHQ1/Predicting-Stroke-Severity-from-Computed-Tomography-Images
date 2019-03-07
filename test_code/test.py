''''
def demo():
    c=10
    for i in range(0,9):
       c+=1;
    print(c)
    ''print 的位置很关键'
demo()

'''''


''''
def demo():

    #global c
    'global在不在有区别哦'
    c = 10
demo()
print(c)
'''

# class Student():
#     name = 'Jin'
#     age = 26
#     def print_file(self):
#         print('name:'+self.name)
#         print('age:'+str(self.age))
#student = Student()
#student.print_file()

import pydicom
import numpy as np
import os
import matplotlib.pyplot as plt
#from glob3 import *
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.ndimage
from skimage import morphology
from skimage import measure
from skimage.transform import resize
from sklearn.cluster import KMeans
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


def voxel3d(dcms,j):
    row_vector = dcms[j].ImageOrientationPatient[0:3]
    column_vector = dcms[j].ImageOrientationPatient[3:6]
    pixel_size = list(map(float, list(dcms[j].PixelSpacing)))

    pixel_size_x = pixel_size[0]
    pixel_size_y = pixel_size[1]
    image_position_patient = [float(i) for i in list(dcms[j].ImagePositionPatient)]



    for m in range(dcms[j].Columns):
        pixel_location_x = m
        row_change_x = [i * pixel_size_x * float(pixel_location_x) for i in row_vector ]

        for n in range(dcms[j].Rows):
            pixel_location_y = n
            row_change_y = [i * pixel_size_y * float(pixel_location_y) for i in row_vector ]

            voxel = list(map(lambda x: x[0] + x[1] + x[2], zip(image_position_patient, row_change_x, row_change_y)))
            voxel = np.array(voxel)
            # voxel_list = np.stack(voxel_list, np.array(voxel))

            return voxel




    # np.stack(arrays, axis=0).shape




id = 0
data_path = r"C:\Users\Jin\Downloads\Predicting-Stroke-Severity-from-Computed-Tomography-Images-master\Test_Image"
patient = load_scan(data_path)

voxel = voxel3d(patient,0)
voxel_list = np.array([])
voxel_list = np.stack(voxel_list, voxel)
print(voxel_list)

a=1


