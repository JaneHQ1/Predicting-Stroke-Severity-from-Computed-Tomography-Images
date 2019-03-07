"""
Use Matplotlib display dicom
"""
"""
Use Matplotlib display dicom
"""
import pydicom
import numpy as np
from pydicom.data import get_testdata_files
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import os

class Matplot():


    def __init__(self):
        pass


    # load DCM file folder
    # def DCM_loader(path):
    #     dcms=[]
    #     for file in os.listdir(path):
    #     # pydicom.dataset.FileDataset' object cannot be append to list
    #         dcms.append(pydicom.dcmread(os.path.join(path, file)))
    #     return dcms

    def load_scan(path):
        slices = [pydicom.read_file(path + '\\' + s) for s in os.listdir(path)]
        slices.sort(key=lambda x: int(x.InstanceNumber))
        try:
            slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
        except:
            slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

        for s in slices:
            s.SliceThickness = slice_thickness
        return slices


    # update canvas
    def update(val):
        index = int(s_index.val)
        canvas.set_data(dcms[index].pixel_array)
        plt.draw()




path = r"C:\Users\Jin\Downloads\Predicting-Stroke-Severity-from-Computed-Tomography-Images-master\Series 002 [CT - Crane SPC]"
# dcms = Matplot.DCM_loader(path)
dcms = Matplot.load_scan(path)

# print(dcms)
canvas = plt.imshow(dcms[0].pixel_array, cmap=plt.cm.bone)
ax_index = plt.axes([0.15, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
s_index = Slider(ax_index, 'Index', 0, len(dcms)-1, valinit=0, valstep=1)

s_index.on_changed(Matplot.update)
plot = plt.show()



# Matplot.plotz(path)

# def toggle_images(event):
	# plt.imshow(ds2.pixel_array,cmap=plt.cm.bone)
	# plt.draw()
#plt.connect('button_press_event', toggle_images)

# print(plt.get_backend())