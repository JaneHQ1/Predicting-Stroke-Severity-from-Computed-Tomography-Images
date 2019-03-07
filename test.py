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


def voxel3d(dcms):
    row_vector = [1, 0, 0]
    column_vector = [0, 1, 0]
    pixel_size = list(map(float, list(dcms[0].PixelSpacing)))

    pixel_size_x = pixel_size[0]
    pixel_location_x = 10
    row_change_x = [i * pixel_size_x * float(pixel_location_x) for i in row_vector ]

    pixel_size_y = pixel_size[1]
    pixel_location_y = 100
    row_change_y = [i * pixel_size_y * float(pixel_location_y) for i in row_vector ]

    image_position_patient = list(dcms[0].ImagePositionPatient)
    voxel = image_position_patient + row_change_x +row_change_y

    return voxel


id = 0
data_path = r"C:\Users\Jin\Downloads\Predicting-Stroke-Severity-from-Computed-Tomography-Images-master\Test_Image"
patient = load_scan(data_path)

print(voxel3d(patient))

a=1


