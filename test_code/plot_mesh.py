'''
pcolormesh
https://pyscience.wordpress.com/2014/09/08/dicom-in-python-importing-medical-image-data-into-numpy-with-pydicom-and-vtk/
'''

import pydicom
import os
import numpy
from matplotlib import pyplot as plt

PathDicom = r"C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\MyHead"
lstFilesDCM = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName,filename))


# Get ref file
RefDs = pydicom.read_file(lstFilesDCM[0])

# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))

# Load spacing values (in mm)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))

"""
py.arange([start, ]stop, [step, ]dtype=None)
Return evenly spaced values within a given interval.
Values are generated within the half-open interval [start, stop) (in other words, the interval including start but excluding stop). 
For integer arguments the function is equivalent to the Python built-in range function, but returns an ndarray rather than a list.

"""
# where we simply use numpy.arange, ConstPixelDims, and ConstPixelSpacing to calculate axes for this array
x = numpy.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
y = numpy.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
z = numpy.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])


"""
numpy.zeros(shape, dtype=float, order='C')
Return a new array of given shape and type, filled with zeros.
shape : int or tuple of ints
Shape of the new array, e.g., (2, 3) or 2.
dtype : data-type, optional
The desired data-type for the array, e.g., numpy.int8. Default is numpy.float64.
"""
# The array is sized based on 'ConstPixelDims'
ArrayDicom = numpy.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)

# loop through all the DICOM files
for filenameDCM in lstFilesDCM:
    # read the file
    ds = pydicom.read_file(filenameDCM)
    # store the raw image data
    ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array

"""
dpi: dots per inch
"""
plt.figure(dpi=300)
"""
Axes.set_aspect(aspect, adjustable=None, anchor=None, share=False)
aspect : {'auto', 'equal'} or num
'equal'	same scaling from data to plot units for x and y
adjustable : {'box', 'datalim'}
If 'box', change the physical dimensions of the Axes. If 'datalim', change the x or y data limits.
"""
plt.axes().set_aspect('equal', 'datalim')
plt.set_cmap(plt.gray())
# image1 = plt.pcolormesh(x, y, numpy.flipud(ArrayDicom[:, :, 80]))
"""
z is row an y is column.
Flip ArrayDicom to be (x,y,z)
"""
plt.pcolormesh(z, y, numpy.flipud(ArrayDicom[150, :, :]))

# fig, axs = plt.subplots(1, 2)
# axs[0, 0].plt.show(image1)
plt.show()