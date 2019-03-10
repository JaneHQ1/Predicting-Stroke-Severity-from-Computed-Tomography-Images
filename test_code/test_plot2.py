"""
https://www.datacamp.com/community/tutorials/matplotlib-3d-volumetric-data
"""

import matplotlib.pyplot as plt
from skimage import data
import pydicom
import nibabel
import os
'''
astronaut = data.astronaut()
ihc = data.immunohistochemistry()
hubble = data.hubble_deep_field()

# Initialize the subplot panels side by side
fig, ax = plt.subplots(nrows=1, ncols=3)

# Show an image in each subplot
ax[0].imshow(astronaut)
ax[0].set_title('Natural image')
ax[1].imshow(ihc)
ax[1].set_title('Microscopy image')
ax[2].imshow(hubble)
ax[2].set_title('Telescope image');
plt.show()
'''

# Read the image
path = r"C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\TestSample\nifti_2"
struct = nibabel.load(os.path.join(path, 'ARTERIELLE.nii.gz'))

# Get a plain NumPy array, without all the metadata
struct_arr = struct.get_fdata()
print(struct_arr.shape)
# (512, 512, 361)
# plot the 75th 512x361 image
plt.imshow(struct_arr[75], aspect = 'equal')
# plt.show()

# Transpose
struct_arr2 = struct_arr.T
# plot the 34th 512x512 image
plt.imshow(struct_arr2[34])
print(struct_arr2.shape)
# (361, 512, 512)
# print(struct_arr2[34])
# plt.show()

"""
In this case, K is a built-in keyboard shortcut to change the x-axis to use a logarithmic scale. 
If we want to use K exclusively, we have to remove it from matplotlib’s default key maps. 
"""
def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)

def multi_slice_viewer(volume):
    remove_keymap_conflicts({'j', 'k'})
    fig, ax = plt.subplots()
    ax.volume = volume
    ax.index = volume.shape[0] // 2
    ax.imshow(volume[ax.index])
    fig.canvas.mpl_connect('key_press_event', process_key)
    plt.show()

def process_key(event):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.key == 'j':
        previous_slice(ax)
    elif event.key == 'k':
        next_slice(ax)
    fig.canvas.draw()

def previous_slice(ax):
    volume = ax.volume
    ax.index = (ax.index - 1) % volume.shape[0]  # wrap around using %
    ax.images[0].set_array(volume[ax.index])

def next_slice(ax):
    volume = ax.volume
    ax.index = (ax.index + 1) % volume.shape[0]
    ax.images[0].set_array(volume[ax.index])


multi_slice_viewer(struct_arr2)





