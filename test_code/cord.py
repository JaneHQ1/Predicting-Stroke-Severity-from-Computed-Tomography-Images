"""
add button press event in matplotlib
"""

import matplotlib.pyplot as plt
import nibabel as nib


class mat_plot:
    def __init__(self, struct_arr):
        self.struct_transverse = struct_arr.T
        self.struct_frontal = struct_arr.transpose(1, 2, 0)
        self.struct_sagittal = struct_arr.transpose(0, 2, 1)

        self.fig = plt.figure()
        self.ax_transverse = self.fig.add_subplot(221)
        self.ax_transverse.index = self.struct_transverse.shape[0] // 2
        self.ax_transverse.imshow(self.struct_transverse[self.ax_transverse.index], cmap="gray")

        self.ax_frontal = self.fig.add_subplot(223)
        self.ax_frontal.index = self.struct_frontal.shape[0] // 2
        self.ax_frontal.imshow(self.struct_frontal[self.ax_frontal.index], cmap="gray")

        self.ax_sagittal = self.fig.add_subplot(224)
        self.ax_sagittal.index = self.struct_sagittal.shape[0] // 2
        self.ax_sagittal.imshow(self.struct_sagittal[self.ax_sagittal.index], cmap="gray")
        
    def start(self):
        plt.show()
