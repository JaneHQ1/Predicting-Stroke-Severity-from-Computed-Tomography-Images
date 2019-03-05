"""
Use Matplotlib display dicom
"""
import pydicom
from pydicom.data import get_testdata_files
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import os

class Matplot():


    def __init__(self):
        pass


    # load DCM file folder
    def DCM_loader(path):
        dcms=[]
        for file in os.listdir(path):

            # pydicom.dataset.FileDataset' object cannot be append to list
            # The append() method adds a single item to the existing list.
            # It doesn't return a new list; rather it modifies the original list.

            # pydicom.filereader.dcmread(fp, defer_size=None, stop_before_pixels=False, force=False, specific_tags=None)
            # fp:str or file-like: Either a file-like object, or a string containing the file name.
            # If a file-like object, the caller is responsible for closing it.
            # return: An instance of FileDataset that represents a parsed DICOM file.
            dcms.append(pydicom.dcmread(os.path.join(path, file)))
        return dcms


    # update canvas
    def update(val):
        index = int(s_index.val)

        # set_data(x, y, A)
        # Set the grid for the pixel centers, and the pixel values.
        # x and y are monotonic 1-D ndarrays of lengths N and M, respectively, specifying pixel centers
        canvas.set_data(dcms[index].pixel_array)
        plt.draw()


# Remember to add the r before the path
path = r"C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\Series 002 [CT - Crane SPC]"
dcms = Matplot.DCM_loader(path)
a = 1
# print(dcms)

# matplotlib.pyplot.imshow(X, cmap=None, norm=None, aspect=None, interpolation=None, alpha=None, vmin=None, vmax=None,
# origin=None, extent=None, shape=None, filternorm=1, filterrad=4.0, imlim=None, resample=None, url=None, *, data=None, **kwargs)[source]
# X : array-like or PIL image
# The image data. Supported array shapes are:
#(M, N): an image with scalar data. The data is visualized using a colormap.

# cmap : str or Colormap, optional
# A Colormap instance or registered colormap name. The colormap maps scalar data to colors.

# pixel_array one of the information in dcms.
# Matplotlib has a number of built-in colormaps accessible via matplotlib.cm.get_cmap.
# bone: sequential increasing black-white color map with a tinge of blue, to emulate X-ray film
canvas = plt.imshow(dcms[0].pixel_array, cmap=plt.cm.bone)

# plt.axes(rect, projection=None, polar=False, **kwargs)
# 4-tuple of floats rect = [left, bottom, width, height]. Basically it is the size of the index.
# Returns: Axes (or a subclass of Axes)
ax_index = plt.axes([0.226, 0.005, 0.572, 0.02], facecolor='lightgoldenrodyellow')

# class matplotlib.widgets.Slider(ax, label, valmin, valmax, valinit=0.5, valfmt='%1.2f', closedmin=True, closedmax=True,
# slidermin=None, slidermax=None, dragging=True, valstep=None, **kwargs)[source]
# A slider representing a floating point range.
# val : float - Slider value.
# ax : Axes - The Axes to put the slider in.
# label : str - Slider label.
# valmin : float - The minimum value of the slider.
# valmax : float - The maximum value of the slider.
# valinit : float, optional, default: 0.5 - The slider initial position.
# valstep : float, optional, default: None - If given, the slider will snap to multiples of valstep.
s_index = Slider(ax_index, 'Index', 0, len(dcms)-1, valinit=0, valstep=1)

# on_changed(func)
# Function to call when slider is changed.
# Returns: cid : int - Connection id (which can be used to disconnect func)
s_index.on_changed(Matplot.update)
plot = plt.show()



# Matplot.plotz(path)

# def toggle_images(event):
	# plt.imshow(ds2.pixel_array,cmap=plt.cm.bone)
	# plt.draw()
#plt.connect('button_press_event', toggle_images)

# print(plt.get_backend())
