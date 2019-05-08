

import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import os.path

# source_folder = r'E:\Training_Batch'
# file_name = 'segmentation-100.nii'

source_folder = r'E:\segmentation_liver\data\train'
file_name = 'segmentation-100_500.npy'

# Load .nii
# pixel_arr = nib.load(os.path.join(source_folder, file_name))
# pixel_arr = pixel_arr.get_fdata()
# pixel_arr = pixel_arr[200]

# Load .npy
pixel_arr = np.load(os.path.join(source_folder, file_name)).T

pixel_arr = (pixel_arr == 1)
print(type(pixel_arr))

plt.figure()
plt.imshow(pixel_arr, cmap="gray")

plt.show()