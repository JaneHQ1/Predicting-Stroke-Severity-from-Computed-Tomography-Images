# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 21:39:19 2019

@author: janej
"""

import nibabel as nib
import os
#print(os.stat(r'C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\TestSample\nifti_1').st_size == 0)
epi_img = nib.load(r'C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\TestSample\nifti_1\ARTERIELLE.nii')
epi_img_data = epi_img.get_fdata()
epi_img_data.shape

import matplotlib.pyplot as plt
def show_slices(slices):
    """ Function to display row of image slices """
    fig, axes = plt.subplots(1, len(slices))
    for i, slice in enumerate(slices):
        axes[i].imshow(slice.T, cmap="gray", origin="lower")

slice_0 = epi_img_data[26, :, :]
slice_1 = epi_img_data[:, 20, :]
slice_2 = epi_img_data[:, :, 16]
show_slices([slice_0, slice_1, slice_2])
plt.suptitle("Center slices for EPI image")  