# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 18:07:36 2019

@author: Ngawang Tenzin
"""

# Importing required PyQt5 classess and Matplotlib
from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QFileDialog, QApplication, QWidget, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap
import sys
import pydicom as dicom
import nibabel as nib
import matplotlib.pyplot as plt

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
            
    def initUI(self):
        
        grid = QGridLayout()
        #hbox = QHBoxLayout()
        
        x_image = QLabel(self)
        x_pixmap = QPixmap("x_image.png")
        #x_image.setPixmap(x_pixmap)
        x_pixmap_resize = x_pixmap.scaledToHeight(300)
        x_image.setPixmap(x_pixmap_resize)
        
        y_image = QLabel(self)
        y_pixmap = QPixmap("y_image.png")
        #y_image.setPixmap(y_pixmap)
        y_pixmap_resize = y_pixmap.scaledToHeight(300)
        y_image.setPixmap(y_pixmap_resize)
        
        z_image = QLabel(self)
        z_pixmap = QPixmap("z_image.png")
        #z_image.setPixmap(z_pixmap)
        z_pixmap_resize = z_pixmap.scaledToHeight(300)
        z_image.setPixmap(z_pixmap_resize)
       
        
        #x_image.resize(0.5*x_pixmap.width(), 0.5*x_pixmap.height())
        #x_image.setFrameShape(QFrame.StyledPanel)
        #x_image.setLineWidth(3)
        grid.addWidget(x_image, 0,0)
        grid.addWidget(y_image, 1,0)
        grid.addWidget(z_image, 1,1)
        
 
        self.setLayout(grid)

# Main window
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()
        
    def initWindow(self):
        # Set window dimension and title
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
        
        # To display
        self.window1 = Example()
        self.setCentralWidget(self.window1)
        
    # Function to create png image format from dicom file
    def load_dicom(self):
        #   Source: https://pydicom.github.io/pydicom/stable/auto_examples/input_output/plot_read_dicom.html
        filePath, _= QFileDialog.getOpenFileName(self, "Select Medical image", "", "Image Files (*.dcm)")
        dataset = dicom.dcmread(filePath)
        plt.imsave('z_image.png', dataset.pixel_array, cmap=plt.cm.bone)
        
        """
        self.label = QLabel()
        self.setCentralWidget(self.label)
        pixmap = QPixmap("z_image.png")
        self.label.setPixmap(pixmap)
        """
    def load_nifti(self):
        #   Source: https://pydicom.github.io/pydicom/stable/auto_examples/input_output/plot_read_dicom.html
        filePath, _= QFileDialog.getOpenFileName(self, "Select Medical image", "", "Image Files (*.nii)")
        niiFile = nib.load(filePath)
        nii_data = niiFile.get_fdata()
        # Slice-X
        slice_x = nii_data[26, :, :]
        plt.imsave('x_image.png', slice_x.T, cmap=plt.cm.bone)
        # Slice-Y
        slice_y = nii_data[:, 20, :]
        plt.imsave('y_image.png', slice_y.T, cmap=plt.cm.bone)
        # Slice-Z
        slice_z = nii_data[:, :, 16]
        plt.imsave('z_image.png', slice_z.T, cmap=plt.cm.bone)
        
        """

        self.label = QLabel()
        self.setCentralWidget(self.label)
        pixmap = QPixmap("z_image.png")
        self.label.setPixmap(pixmap)
        """
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())
    