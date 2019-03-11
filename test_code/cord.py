'''
connect x,y,z planes
'''

import matplotlib.pyplot as plt
from skimage import data
import pydicom
import nibabel as nib
import os

# Read the image
path = r"C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\TestSample\nifti_2\ARTERIELLE.nii.gz"
struct = nib.load(path)

# Get a plain NumPy array, without all the metadata
struct_arr = struct.get_fdata()
# print(struct_arr.shape)
# (512, 512, 361)
# plot the 75th 512x361 image
# plt.imshow(struct_arr[75], aspect='equal')
# plt.show()

# Transpose
struct_transverse = struct_arr.T
# plot the 34th 512x512 image
# plt.imshow(struct_transverse[34])
# print(struct_transverse.shape)
# (361, 512, 512)
# print(struct_arr2[34])
# plt.show()
struct_frontal = struct_arr.transpose(1, 2, 0)
# plt.imshow(struct_frontal[250])
# print(struct_frontal.shape)
# plt.show()

struct_sagittal = struct_arr.transpose(0, 2, 1)
# plt.imshow(struct_sagittal[250])
# print(struct_sagittal.shape)
# plt.show()


fig = plt.figure()
ax_transverse = fig.add_subplot(221)
ax_transverse.index = struct_transverse.shape[0] // 2
ax_transverse.imshow(struct_transverse[ax_transverse.index])

ax_frontal = fig.add_subplot(223)
ax_frontal.index = struct_frontal.shape[0] // 2
ax_frontal.imshow(struct_frontal[ax_frontal.index])

ax_sagittal = fig.add_subplot(224)
ax_sagittal.index = struct_frontal.shape[0] // 2
ax_sagittal.imshow(struct_sagittal[ax_sagittal.index])

plt.show()