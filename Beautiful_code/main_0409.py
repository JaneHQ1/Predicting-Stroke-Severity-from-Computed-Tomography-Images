# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:49:57 2019
Title: MP4-Medical Image Processing
@author: MP4 Team

"""
#   Main Program to Start
#   Importing required PyQt5 class
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QVBoxLayout, QScrollArea, QFileDialog
from PyQt5.QtGui import QIcon

#   Importing required Matplotlib and Numpy class
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np

#   Importing nibabel for Nifti files
import nibabel as nib

#   Importing backend class for Image display and Image event
from display_0409 import *
from event_controller_0409 import *
from roi_controller_0409 import *
from roi_0409 import *
from patient_0409 import *

#   Main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu_window()
        
    # Menubar function
    def menu_window(self):
         # Set main window dimension and title
        self.setWindowIcon(QIcon('menuIcon/uomLog.png'))
        self.setWindowTitle('MP4 Medical Image Processor')
        self.setGeometry(300, 50, 650, 650)
        
        # Create main menu
        mainMenu = self.menuBar()
        basicMenu = mainMenu.addMenu('Basic')
        analyMenu = mainMenu.addMenu('Image Analysis')
        evaluMenu = mainMenu.addMenu('Evaluation')
        roiMenu = mainMenu.addMenu('Region of Interest')
        
        # Create submenu action and add to main menu
        # Basic submenu
        dicomAct = QAction(QIcon('menuIcon/fileOpen.png'), 'Load Dicom', self)
        dicomAct.setShortcut('Ctrl+D')
        #loadAct.triggered.connect(self.load_dicom)
        basicMenu.addAction(dicomAct)
        
        niftiAct = QAction(QIcon('menuIcon/fileOpen.png'), 'Load Nifti', self)
        niftiAct.setShortcut('Ctrl+N')
        niftiAct.triggered.connect(self.load_nifti_file)
        basicMenu.addAction(niftiAct)
        
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
        analyMenu.addAction(segmAct)
        
        # Evalution submenu
        gtruthAct = QAction('Run Ground Truth', self)
        evaluMenu.addAction(gtruthAct)
        
        # Region of Interest submenu
        tranAct = QAction('Transverse Plane', self, checkable=True)
        tranAct.triggered.connect(self.load_nifti_file)
        roiMenu.addAction(tranAct)
        
        fronAct = QAction('Frontal Plane', self, checkable=True)
        fronAct.triggered.connect(self.load_nifti_file)
        roiMenu.addAction(fronAct)
        
        sagitAct = QAction('Frontal Plane', self, checkable=True)
        sagitAct.triggered.connect(self.load_nifti_file)
        roiMenu.addAction(sagitAct)
        
        
#        roiAct = QAction(QIcon('menuIcon/fileSave.png'), 'Region of Interest', self)
#        roiAct.setShortcut('Ctrl+R')
#        basicMenu.addAction(roiAct)
#        
#        
#        enubar = self.menuBar()
#        viewMenu = menubar.addMenu('View')
#        
#        viewStatAct = QAction('View statusbar', self, checkable=True)
#        viewStatAct.setStatusTip('View statusbar')
#        viewStatAct.setChecked(True)
#        viewStatAct.triggered.connect(self.toggleMenu)
#        
#        viewMenu.addAction(viewStatAct)
        
        
        
        # Direct User to use Meny to display images
        self.statusBar().showMessage("Use Basic Menu to display Medical Images", 5000)
        
        
    # Extract pixel data from medical image file of NIFTI format
    def load_nifti_file(self):
        try:
            filePath, _= QFileDialog.getOpenFileName(self, "Select Medical image", "", "Image Files (*.nii *.nii.gz)")
            niftiFile = nib.load(filePath)
            pixel_arr = niftiFile.get_fdata()
            
            tran_arr = pixel_arr.transpose(2, 1, 0)
            fron_arr = pixel_arr.transpose(1, 2, 0)
            sagi_arr = pixel_arr.transpose(0, 2, 1)
            
            self.vol_tran = np.flip(tran_arr)
            self.vol_fron = np.flip(fron_arr)
            self.vol_sagi = np.flip(sagi_arr)
            
            # Plot the image using pixel data
            self.plot_images()

        except:
            self.statusBar().showMessage("File type not supported or empty !!!", 2500)
            
    # Plot the image using pixel data
    def plot_images(self):
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        # for key event
#        canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
#        canvas.setFocus()
    
        ax_tran = fig.add_subplot(221, adjustable='box', aspect='auto')
        ax_fron = fig.add_subplot(325, adjustable='box', aspect='auto')
        ax_sagi = fig.add_subplot(326, adjustable='box', aspect='auto')
        
        # --Start of patient info--
        ax_info = fig.add_subplot(222, adjustable='box', aspect='auto')
        #ax_info.axis('off')
        
        path_matdata = r"D:\CapstoneProject\nifti_2\dcmHeaders.mat"
        id = Patient(path_matdata, 'PatientID')
        name = Patient(path_matdata, 'PatientName')
        age = Patient(path_matdata, 'PatientAge')
        
        id_str = id.patient_dict()
        name_str = name.patient_dict()
        age_str = age.patient_dict()
        
        patient_id = re.findall('\d+', id_str)
        patient_name = re.findall('\w+', name_str)
        patient_age = re.findall('\w+', age_str)
        
        txt_id = ax_info.text(0.1, 0.8, 'patient ID: ' + patient_id[0], color='k')
        txt_name = ax_info.text(0.1, 0.6, 'patient name: ' + patient_name[0], color='k')
        tex_age = ax_info.text(0.1, 0.4, 'patient age: ' + patient_age[0], color='k')
        #--End of pateint info
        
        im_dis = ImageDisplay(self.vol_tran, self.vol_fron, self.vol_sagi, ax_tran, ax_fron, ax_sagi)
        im_dis.initialize_transverse_display()
        im_dis.initialize_frontal_display()
        im_dis.initialize_sagittal_display()
        
        self.ev_ctrl = EventController(fig, im_dis, self.vol_tran, self.vol_fron, self.vol_sagi, ax_tran, ax_fron, ax_sagi)
        self.roi_ctrl = RoiController(fig, im_dis,  self.vol_tran, self.vol_fron, self.vol_sagi, ax_tran, ax_fron, ax_sagi)
        roi = ROI(fig, ax_sagi)
        
        # Display canvas of Matplotlib as central Widget
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QVBoxLayout())

        self.toolbar = NavigationToolbar(self.canvas, self.widget)
        self.widget.layout().addWidget(self.toolbar)
        self.widget.layout().addWidget(self.canvas)
        
        # Connect Mouse Event to Event Controller class
        self.canvas.mpl_connect('button_press_event', self.ev_ctrl.button_press_events)
        
        
#   Start of main program to run
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
