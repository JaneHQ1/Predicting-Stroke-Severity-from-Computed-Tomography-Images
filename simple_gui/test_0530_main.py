# -*- coding: utf-8 -*-
"""
Created on Thu May 30 10:53:25 2019

@author: Ngawang Tenzin
"""

#   Main Program to Start
#   Importing required PyQt5 class
import sys
import os
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QWidget, QTableWidget, QTableWidgetItem, 
                             QVBoxLayout, QFileDialog)
#   Importing required Matplotlib and Numpy class
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#from matplotlib.pyplot import plt
import numpy as np
import re
import h5py

#   Importing nibabel for Nifti files
import nibabel as nib

#   Importing backend class for Image display and Image event
from test_0530_seg import ValidateWindowCtr

#   Main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.index_trans, self.index_gtruth, self.index_segmen = [0], [0], [0]
        self.menu_window()
        
    # Menubar function
    def menu_window(self):
         # Set main window dimension and title
        self.setWindowIcon(QIcon('menu_icon/uomLog.png'))
        self.setWindowTitle('MP4 Medical Image Processor')
        self.setGeometry(75, 50, 700, 650)
        
        self.load_segmentation_file()
    
    # Extract pixel data from h5 and ground truth file
    def load_segmentation_file(self):
        # Get file path
        vol_file_path = r"D:\CapstoneProject\current_test_code\training_data\Training Batch 1\volume-99.nii"
        gtruth_file_path = r"D:\CapstoneProject\current_test_code\training_data\Training Batch 1\segmentation-99.nii" 
        segmen_file_path = r"D:\CapstoneProject\current_test_code\training_data\Training Batch 1\prediction-99.h5"
        
        # Extract pixel data and set initial index or slice number
#        voxel_trans = nib.load(vol_file_path).get_fdata()*255
        voxel_trans = nib.load(vol_file_path).get_fdata()
#        voxel_gtruth = nib.load(gtruth_file_path).get_fdata()*255
        voxel_gtruth = nib.load(gtruth_file_path).get_fdata()
        voxel_segmen = h5py.File(segmen_file_path,"r")["predictions"].value
        
        self.vol_trans = np.flip(voxel_trans.transpose(2, 1, 0))
        self.vol_gtruth = np.flip(voxel_gtruth.transpose(2, 1, 0))
        self.vol_segmen = np.flip(voxel_segmen.transpose(2, 1, 0))
        
        self.index_trans[0] = self.vol_trans.shape[0] // 2
        #self.index_gtruth[0] = self.vol_gtruth.shape[0] // 3
        self.index_gtruth[0] = 135
        self.index_segmen[0] = self.vol_segmen.shape[0] // 2
        
        # Plot the image using above pixel data
        self.plot_validate_image()
        
        
    # Plot two image side by side on the window
    def plot_validate_image(self):
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        ax_trans = fig.add_subplot(223, adjustable='box', aspect='auto')
        im_trans = ax_trans.imshow(self.vol_trans[self.index_trans[-1]], cmap="gray")
        #im_trans = ax_trans.imshow(self.vol_trans[self.index_trans[-1]])
        ax_trans.set_title('Transverse Voxel Image', color = 'b')
        
        ax_gtruth = fig.add_subplot(221, adjustable='box', aspect='auto')
        #im_gtruth = ax_gtruth.imshow(self.vol_gtruth[self.index_gtruth[-1]], cmap="gray")
        im_gtruth = ax_gtruth.imshow(self.vol_gtruth[self.index_gtruth[-1]])
        ax_gtruth.set_title('Ground Truth Image', color = 'b')
        
        ax_segmen = fig.add_subplot(222, adjustable='box', aspect='auto')
        #im_segmen = ax_segmen.imshow(self.vol_segmen[self.index_segmen[-1]], cmap="gray")
        im_segmen = ax_segmen.imshow(self.vol_segmen[self.index_segmen[-1]])
        ax_segmen.set_title('Segmented Image', color = 'b')
        
#        self.segmen_ctrl = ValidateWindowCtr(fig, im_trans, im_gtruth, im_segmen, self.vol_trans, self.vol_gtruth, 
#                                             self.vol_segmen, ax_trans, ax_gtruth, ax_segmen, self.index_trans, 
#                                             self.index_gtruth, self.index_segmen)
        
        # Display canvas of Matplotlib as central Widget
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QVBoxLayout())
        self.widget.layout().addWidget(self.canvas)
        
        
#   Start of main program to run
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())