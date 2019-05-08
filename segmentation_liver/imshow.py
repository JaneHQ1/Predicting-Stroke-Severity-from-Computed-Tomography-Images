

import numpy as np
import matplotlib.pyplot as plt


path = r"E:\segmentation_tumour\data\train\segmentation-100_200.npy"

pixel_arr = np.load(path)

plt.figure()
plt.imshow(pixel_arr, cmap="gray")

plt.show()