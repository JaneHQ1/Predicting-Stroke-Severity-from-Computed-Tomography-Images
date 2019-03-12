# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 16:18:06 2019

@author: Ngawang Tenzin
"""

# Importing required PyQt5 classess and Matplotlib
from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QFileDialog, QApplication
from PyQt5.QtGui import QIcon, QPixmap
import sys
import pydicom as dicom
import nibabel as nib
import matplotlib.pyplot as plt


# Main window
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()
        
    def initWindow(self):
        # Set window dimension and title
        self.setWindowIcon(QIcon('menuIcon/uomLog.png'))
        self.setWindowTitle('MP4 Medical Image Processor')
        self.setGeometry(100, 100, 800, 600)
        
        # Create main menu
        mainMenu = self.menuBar()
        basicMenu = mainMenu.addMenu('Basic')
        analyMenu = mainMenu.addMenu('Image Analysis')
        evaluMenu = mainMenu.addMenu('Evaluation')
        
        # Create submenu action and add to main menu
        # Basic submenu
        loadAct = QAction(QIcon('menuIcon/fileOpen.png'), 'Load Dicom', self)
        loadAct.setShortcut('Ctrl+D')
        loadAct.triggered.connect(self.load_dicom)
        basicMenu.addAction(loadAct)
        
        loadAct = QAction(QIcon('menuIcon/fileOpen.png'), 'Load Nifti', self)
        loadAct.setShortcut('Ctrl+N')
        loadAct.triggered.connect(self.load_nifti)
        basicMenu.addAction(loadAct)
        
        roiAct = QAction(QIcon('menuIcon/fileSave.png'), 'Region of Interest', self)
        roiAct.setShortcut('Ctrl+R')
        basicMenu.addAction(roiAct)
        
        measAct = QAction(QIcon('menuIcon/fileFile.png'), 'Measure', self)
        measAct.setShortcut('Ctrl+M')
        basicMenu.addAction(measAct)
        
        closeAct = QAction(QIcon('menuIcon/fileClose.png'), 'Close', self)
        closeAct.setShortcut('Ctrl+Q')
        closeAct.triggered.connect(self.close)
        basicMenu.addAction(closeAct)
        
        # Image Analysis submenu
        dectAct = QAction('Detection', self)
        analyMenu.addAction(dectAct)
        
        segmAct = QAction('Segmentation', self)
        analyMenu.addAction(segmAct)
        
        # Evalution submenu
        runAct = QAction('Run Evaluation', self)
        evaluMenu.addAction(runAct)
        
        gtruthAct = QAction('Ground Truth', self)
        evaluMenu.addAction(gtruthAct)
        
        
    # Function to create png image format from dicom file
    def load_dicom(self):
        #   Source: https://pydicom.github.io/pydicom/stable/auto_examples/input_output/plot_read_dicom.html
        filePath, _= QFileDialog.getOpenFileName(self, "Select Medical image", "", "Image Files (*.dcm)")
        dataset = dicom.dcmread(filePath)
        plt.imsave('z_image.png', dataset.pixel_array, cmap=plt.cm.bone)
        
        self.label = QLabel()
        self.setCentralWidget(self.label)
        pixmap = QPixmap("z_image.png")
        self.label.setPixmap(pixmap)
        
    def load_nifti(self):
        #   Source: https://pydicom.github.io/pydicom/stable/auto_examples/input_output/plot_read_dicom.html
        filePath, _= QFileDialog.getOpenFileName(self, "Select Medical image", "", "Image Files (*.nii)")
        niiFile = nib.load(filePath)
        nii_data = niiFile.get_fdata()
        slice_0 = nii_data[:, :, 16]
        plt.imsave('y_image.png', slice_0.T, cmap=plt.cm.bone)
        
        self.label = QLabel()
        self.setCentralWidget(self.label)
        pixmap = QPixmap("y_image.png")
        self.label.setPixmap(pixmap)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())
    