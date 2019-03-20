# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 10:16:20 2019

@author: Ngawang Tenzin
"""

# Testing the code to display image using Matplotlib imshow
# Importing required PyQt5 classess and Matplotlib
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QSizePolicy, QGridLayout, QFileDialog
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import nibabel as nib
import matplotlib.pyplot as plt

# Main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menuWindow()
        
    def menuWindow(self):
        # Set main window dimension and title
        self.setWindowIcon(QIcon('menuIcon/uomLog.png'))
        self.setWindowTitle('MP4 Medical Image Processor')
        self.setGeometry(300, 45, 800, 600)
        
        # Create main menu
        mainMenu = self.menuBar()
        basicMenu = mainMenu.addMenu('Basic')
        analyMenu = mainMenu.addMenu('Image Analysis')
        evaluMenu = mainMenu.addMenu('Evaluation')
        
        # Create submenu action and add to main menu
        # Basic submenu
        dicomAct = QAction(QIcon('menuIcon/fileOpen.png'), 'Load Dicom', self)
        dicomAct.setShortcut('Ctrl+D')
        #loadAct.triggered.connect(self.load_dicom)
        basicMenu.addAction(dicomAct)
        
        niftiAct = QAction(QIcon('menuIcon/fileOpen.png'), 'Load Nifti', self)
        niftiAct.setShortcut('Ctrl+N')
        #niftiAct.triggered.connect(self.loadNifti)
        basicMenu.addAction(niftiAct)
        
        closeAct = QAction(QIcon('menuIcon/fileClose.png'), 'Close', self)
        closeAct.setShortcut('Ctrl+Q')
        closeAct.triggered.connect(self.close)
        basicMenu.addAction(closeAct)
        
        # Display the images in grid
        self.main_widget = QWidget(self)
        layout = QGridLayout(self.main_widget)
        
        axis_trans = PlotImages(self.main_widget, width=5, height=4, dpi=100, axis_type="Transverse")
        axis_front = PlotImages(self.main_widget, width=5, height=4, dpi=100, axis_type="Frontal")
        axis_sagit = PlotImages(self.main_widget, width=5, height=4, dpi=100, axis_type="Sagittal")
        layout.addWidget(axis_trans, 0,0)
        layout.addWidget(axis_front, 1,0)
        layout.addWidget(axis_sagit, 1,1)
        
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("Well done for printing me!", 5000)
        
# Class to plot medical images
class PlotImages(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, axis_type="Transverse"):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axis_type = axis_type
        
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self.plotImages()
        
    # Function to plot the images
    def plotImages(self):
        file_path = r"D:\CapstoneProject\nifti_2\ARTERIELLE.nii.gz"
        nifti_file = nib.load(file_path)
        pixel_dataset = nifti_file.get_fdata()
                
        if self.axis_type == "Frontal":
            dataset_subset = pixel_dataset.transpose(1, 2, 0)
        elif self.axis_type == "Sagittal":
            dataset_subset = pixel_dataset.transpose(0, 2, 1)
        else:
            dataset_subset = pixel_dataset.T
            
        axis_plot = self.figure.add_subplot(111)
        axis_plot.index = dataset_subset.shape[0] // 2
        axis_plot.imshow(dataset_subset[axis_plot.index], cmap="gray")
        
        self.draw()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    