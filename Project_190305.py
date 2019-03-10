# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 15:39:10 2019

@author: Ngawang Tenzin
"""
# Importing required PyQt5 classess
from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QFileDialog, QApplication
from PyQt5.QtGui import QIcon, QPixmap
import sys
import pydicom as dicom
import matplotlib.pyplot as plt
import time

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
        fileMenu = mainMenu.addMenu('File')
        measMenu = mainMenu.addMenu('Measure')
        viewMenu = mainMenu.addMenu('View')
        rotateMenu = mainMenu.addMenu('Rotate')
        layoutMenu = mainMenu.addMenu('Layout')
        
        # Create submenu action and add to main menu
        # File submenu
        newAct = QAction(QIcon('menuIcon/fileFile.png'), 'New', self)
        newAct.setShortcut('Ctrl+N')
        newAct.triggered.connect(self.create_image)
        fileMenu.addAction(newAct)
        
        openAct = QAction(QIcon('menuIcon/fileOpen.png'), 'Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.triggered.connect(self.open_image)
        fileMenu.addAction(openAct)
        
        saveAct = QAction(QIcon('menuIcon/fileSave.png'), 'Save', self)
        saveAct.setShortcut('Ctrl+S')
        fileMenu.addAction(saveAct)
        
        closeAct = QAction(QIcon('menuIcon/fileClose.png'), 'Close', self)
        closeAct.setShortcut('Ctrl+Q')
        closeAct.triggered.connect(self.close)
        fileMenu.addAction(closeAct)
        
        # Measure submenu
        lineAct = QAction('Line', self)
        measMenu.addAction(lineAct)
        
        angleAct = QAction('Angle', self)
        measMenu.addAction(angleAct)
        
        areaAct = QAction('Area', self)
        measMenu.addAction(areaAct)
        
        # View submenu
        fitscreenAct = QAction('Fit to Screen', self)
        viewMenu.addAction(fitscreenAct)
        
        orginalAct = QAction('Original Resolution', self)
        viewMenu.addAction(orginalAct)
        
        magnifyAct = QAction('Magnify Spot', self)
        viewMenu.addAction(magnifyAct)
        
        # Rotate submenu
        rrightAct = QAction('Rotate Right', self)
        rotateMenu.addAction(rrightAct)
        
        rleftAct = QAction('Rotate Left', self)
        rotateMenu.addAction(rleftAct)
        
        rclearAct = QAction('Clear Transform', self)
        rotateMenu.addAction(rclearAct)
        
        # Layout submenu
        oneoneAct = QAction(QIcon('menuIcon/layout1_1.png'), '1x1 Screen Layout', self)
        layoutMenu.addAction(oneoneAct)
        
        onetwoAct = QAction(QIcon('menuIcon/layout1_2.png'), '1x2 Screen Layout', self)
        layoutMenu.addAction(onetwoAct)
        
        twooneAct = QAction(QIcon('menuIcon/layout2_1.png'), '2x1 Screen Layout', self)
        layoutMenu.addAction(twooneAct)
        
        twotwoAct = QAction(QIcon('menuIcon/layout2_2.png'), '2x2 Screen Layout', self)
        layoutMenu.addAction(twotwoAct)
        
    # Function to open image files of .jpg, .png and .bmp extension only
    def open_image(self):
        self.label = QLabel()
        self.setCentralWidget(self.label)
        imagePath, _= QFileDialog.getOpenFileName(self, "Select Medical image", "", "Image Files (*.jpg *.png *.bmp)")
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(pixmap)
        #self.resize(pixmap.width(), pixmap.height())
        
    # Function to create new image from dicom file
    def create_image(self):
        #   Source: https://pydicom.github.io/pydicom/stable/auto_examples/input_output/plot_read_dicom.html
        filePath, _= QFileDialog.getOpenFileName(self, "Select Medical image", "", "Image Files (*.dcm)")
        dataset = dicom.dcmread(filePath)
        pat_name = dataset.PatientName
        display_name = pat_name.family_name + ", " + pat_name.given_name
        print("Patient's name...:", display_name)
        print("Patient id.......:", dataset.PatientID)
        print("Modality.........:", dataset.Modality)
        if 'PixelData' in dataset:
            rows = int(dataset.Rows)
            cols = int(dataset.Columns)
            print("Image size.......: {rows:d} x {cols:d}, {size:d} bytes".format(
                rows=rows, cols=cols, size=len(dataset.PixelData)))
            if 'PixelSpacing' in dataset:
                print("Pixel spacing....:", dataset.PixelSpacing)
        
        # Use .get() if not sure the item exists, and want a default value if missing
        print("Slice location...:", dataset.get('SliceLocation', "(missing)"))
        
        # Plot the image using matplotlib and save the figure
        plt.imshow(dataset.pixel_array, cmap=plt.cm.bone)
        plt.savefig("medImages\dicomImage_" + time.strftime("%Y%m%d_%H%M%S"))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())
    