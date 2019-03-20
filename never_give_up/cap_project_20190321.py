# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 15:28:19 2019

@author: Ngawang Tenzin
"""

# Importing required PyQt5 classess and Matplotlib
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QWidget, QGroupBox, QLabel, QVBoxLayout, 
                             QGridLayout, QFileDialog)
from PyQt5.QtGui import QIcon, QPixmap, QCursor, QPainter, QPen
from PyQt5.QtCore import Qt

import nibabel as nib
import matplotlib.pyplot as plt


# Main window class
class MainWindow(QMainWindow):
    # Medical image pixel data
    pixel_dataset = []
    slice_position = [26, 20, 16]
    
    def __init__(self):
        super().__init__()
        self.menuWindow()
        
    def menuWindow(self):
        # Set main window dimension and title
        self.setWindowIcon(QIcon('menuIcon/uomLog.png'))
        self.setWindowTitle('MP4 Medical Image Processor')
        self.setGeometry(300, 50, 800, 600)
        
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
        niftiAct.triggered.connect(self.loadNifti)
        basicMenu.addAction(niftiAct)
        
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
        dectAct = QAction('Run Detection', self)
        analyMenu.addAction(dectAct)
        
        segmAct = QAction('Run Segmentation', self)
#        segmAct.triggered.connect(self.runSegmentation)
        analyMenu.addAction(segmAct)
        
        # Evalution submenu
        gtruthAct = QAction('Run Ground Truth', self)
        evaluMenu.addAction(gtruthAct)
        
    # Extract pixel data from medical image file
    def loadNifti(self):
        #   Source: https://pydicom.github.io/pydicom/stable/auto_examples/input_output/plot_read_dicom.html
        try:
            filePath, _= QFileDialog.getOpenFileName(self, "Select Medical image", "", "Image Files (*.nii *.nii.gz)")
            niftiFile = nib.load(filePath)
            self.pixel_dataset = niftiFile.get_fdata()
            self.convertData()
        except:
            self.statusBar().showMessage("File type not supported or empty !!!", 2500)
            
    # Convert pixel data into png and load the image
    def convertData(self):
        #Convert the pixel data into png image
        # Slice-X
        slice_x = self.pixel_dataset[self.slice_position[0], :, :]
        plt.imsave('x_image.png', slice_x.T, cmap=plt.cm.bone)
        
        # Slice-Y
        slice_y = self.pixel_dataset[:, self.slice_position[1], :]
        plt.imsave('y_image.png', slice_y.T, cmap=plt.cm.bone)
        
        # Slice-Z
        slice_z = self.pixel_dataset[:, :, self.slice_position[2]]
        plt.imsave('z_image.png', slice_z.T, cmap=plt.cm.bone)
        
        # Use DisplayWindow class to display images
        self.setCentralWidget(DisplayWindow())

    # Position of mouse pressed on image 
    def mousePressEvent(self, event):
        if (event.x()>17 and event.x()<275) and (event.y()>51 and event.y()<309):
            self.slice_position[0] = event.x() - 17
            self.slice_position[1] = event.y() - 51
        elif(event.x()>17 and event.x()<380) and (event.y()>347 and event.y()<605):
            self.slice_position[2] = event.x() - 17
            self.slice_position[0] = event.y() - 347
        elif (event.x()>411 and event.x()<773) and (event.y()>347 and event.y()<605):
            self.slice_position[2] = event.x() - 411
            self.slice_position[1] = event.y() - 347
        else:
            self.statusBar().showMessage("You clicked outside the image!!!", 1000)
            
        # Use convertData method to save image as per mouse pressed position
        self.convertData()
        
#    # Run Segmentation algorithm 
#    def runSegmentation(self):
#        # Use DisplayWindow class to display images
#        self.setCentralWidget(DisplayWindow())
        
# Class to display central widgets 
class DisplayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.centralWindow()
#        self.displaySegmentation()
        
    def centralWindow(self):
        # Read image, resize to fit into window then add to GroupBox
        # Frontal plane image
        groupBox1 = QGroupBox("Sagittal Plane:")
        x_image = QLabel(self)
        x_pixmap = QPixmap("x_image.png")
        x_pixmap_resize = x_pixmap.scaledToHeight(256)
        x_image.setPixmap(x_pixmap_resize)
        x_image.setCursor(QCursor(Qt.CrossCursor))  # To change shape of cursor
        vbox1 = QVBoxLayout()
        vbox1.addWidget(x_image)
        groupBox1.setLayout(vbox1)
        
        # Sagittal plane image
        groupBox2 = QGroupBox("Frontal Plane:")
        y_image = QLabel(self)
        y_pixmap = QPixmap("y_image.png")
        y_pixmap_resize = y_pixmap.scaledToHeight(256)
        y_image.setPixmap(y_pixmap_resize)
        y_image.setCursor(QCursor(Qt.CrossCursor))
        vbox2 = QVBoxLayout()
        vbox2.addWidget(y_image)
        groupBox2.setLayout(vbox2)
        
        # Transverse plane image
        groupBox3 = QGroupBox("Transverse Plane:")
        z_image = QLabel(self)
        z_pixmap = QPixmap("z_image.png")
        z_pixmap_resize = z_pixmap.scaledToHeight(256)
        z_image.setPixmap(z_pixmap_resize)
        z_image.setCursor(QCursor(Qt.CrossCursor))
        vbox3 = QVBoxLayout()
        vbox3.addWidget(z_image)
        groupBox3.setLayout(vbox3)
        
        # Extract patient details from medical image dataset
        groupBox4 = QGroupBox("Patient Details:")
        patient_name = QLabel("Patient's Name...: ")
        patient_id = QLabel("Patient's ID.......: ")
        data_size = QLabel("Pixel Data Size....: ")

        vbox4 = QVBoxLayout()
        vbox4.addWidget(patient_name)
        vbox4.addWidget(patient_id)
        vbox4.addWidget(data_size)
        vbox4.addStretch(2)
        groupBox4.setLayout(vbox4)
        
        # Display all GroupBox in grid
        grid = QGridLayout()
        grid.addWidget(groupBox1, 1,1)
        grid.addWidget(groupBox2, 1,0)
        grid.addWidget(groupBox3, 0,0)
        grid.addWidget(groupBox4, 0,1)
        
        self.setLayout(grid)
        
#    #   Display Segmentation
#    def displaySegmentation(self, event):
#        # Read image, resize to fit into window then add to GroupBox
#        seg_display = QPainter()
#        seg_display.begin(self)
#        seg_display.setPen(QPen(Qt.red, 2))
#        seg_display.drawRect(25,75,35,30)
#        seg_display.end()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Applying StylSheet to Groupbox and label
    app.setStyleSheet("QGroupBox{font-weight: bold;} QLabel{color: blue;}")  
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    