# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:49:57 2019
Title: MP4-Medical Image Processing
@author: MP4 Team

"""
#   Main Program to Start
#   Importing required PyQt5 class
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QIcon

#   Importing required Matplotlib and Numpy class
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
import re

#   Importing nibabel for Nifti files
import nibabel as nib

#   Importing backend class for Image display and Image event
from display_0404 import ImageDisplay
from click_controller_0404 import ClickController
from scroll_controller_0404 import ScrollController
from roi_0404 import *
from patient_0404 import *

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
        main_menu = self.menuBar()
        basic_menu = main_menu.addMenu('Basic')
        analysis_menu = main_menu.addMenu('Image Analysis')
        evalution_menu = main_menu.addMenu('Evaluation')
        
        # Create submenu action and add to main menu
        # Basic submenu
        nifti_action = QAction(QIcon('menu_icon/fileOpen.png'), 'Load Nifti', self)
        nifti_action.setShortcut('Ctrl+N')
        nifti_action.triggered.connect(self.load_nifti_file)
        basic_menu.addAction(nifti_action)
        
        measure_action = QAction(QIcon('menu_icon/fileFile.png'), 'Measure', self)
        measure_action.setShortcut('Ctrl+M')
        basic_menu.addAction(measure_action)
        
        close_action = QAction(QIcon('menu_icon/fileClose.png'), 'Close', self)
        close_action.setShortcut('Ctrl+Q')
        close_action.triggered.connect(self.close)
        basic_menu.addAction(close_action)
        
        # Image Analysis submenu
        detaction_action = QAction('Run Detection', self)
        analysis_menu.addAction(detaction_action)
        
        segmen_action = QAction('Run Segmentation', self)
        analysis_menu.addAction(segmen_action)
        
        # Evalution submenu
        gtruth_action = QAction('Run Ground Truth', self)
        evalution_menu.addAction(gtruth_action)
        
        # Create toolbar
        toolbar_1 = self.addToolBar('Change View')
        toolbar_2 = self.addToolBar('Select Axes')
        
        # Create clickable action and scrolling action and add to toolbar_1
        cursor_action = QAction(QIcon('menu_icon/cursor.png'), 'Image click', self)
        cursor_action.triggered.connect(self.set_click_enabled)
        toolbar_1.addAction(cursor_action)
        
        scroll_action = QAction(QIcon('menu_icon/scroll.png'), 'Image scroll', self)
        scroll_action.triggered.connect(self.set_scroll_enabled)
        toolbar_1.addAction(scroll_action)
        
        # Create clickable action and scrolling action and add to toolbar_2
        tran_action = QAction(QIcon('menu_icon/tran.png'), 'Enable Transverse Plane', self)
        tran_action.triggered.connect(self.ax_tran_enabled)
        toolbar_2.addAction(tran_action)
        
        fron_action = QAction(QIcon('menu_icon/fron.png'), 'Enable Frontal Plane', self)
        fron_action.triggered.connect(self.ax_fron_enabled)
        toolbar_2.addAction(fron_action)
        
        sagi_action = QAction(QIcon('menu_icon/sagi.png'), 'Enable Sagittal Plane', self)
        sagi_action.triggered.connect(self.ax_sagi_enabled)
        toolbar_2.addAction(sagi_action)
        
        # Direct User to use Menu to display images
        self.statusBar().showMessage('Use Basic Menu to display Medical Images', 5000)
        
        
    # Extract pixel data from medical image file of NIFTI format
    def load_nifti_file(self):
        try:
            # To extract pixel data
            file_path, _= QFileDialog.getOpenFileName(self, 'Select Medical image', '', 'Image Files (*.nii *.nii.gz)')
            nifti_file = nib.load(file_path)
            pixel_arr = nifti_file.get_fdata()*255
            
            tran_arr = pixel_arr.transpose(2, 1, 0)
            fron_arr = pixel_arr.transpose(1, 2, 0)
            sagi_arr = pixel_arr.transpose(0, 2, 1)
            
            self.vol_tran = np.flip(tran_arr)
            self.vol_fron = np.flip(fron_arr)
            self.vol_sagi = np.flip(sagi_arr)
            
            # To extract header data
            folder_path = os.path.dirname(file_path)
            self.new_matdata_path = None
            for file in os.listdir(folder_path):
                if file.endswith('.mat'):                   
                    matdata_path = os.path.join(folder_path, file)
                    self.new_matdata_path = matdata_path.replace(os.sep, '/')
                    
            # Plot the image using pixel data
            self.plot_images()

        except:
            self.statusBar().showMessage('File type not supported or empty !', 2500)
            
    # Make image clicking enabled
    def set_click_enabled(self):
        try:
            self.click_image = self.canvas.mpl_connect('button_press_event', self.event_ctrl.button_press_events)
            if self.scroll_image: self.canvas.mpl_disconnect(self.scroll_image)
            self.statusBar().showMessage('View mode change to clickable mode enabled!', 1500)
        except:
            self.statusBar().showMessage('Try loading image first or try again!', 2500)
            
    # Make image scrolling enabled
    def set_scroll_enabled(self):
        try:
            self.scroll_image = self.canvas.mpl_connect('axes_enter_event', self.roi_ctrl.fig_enter_event)
            if self.click_image: self.canvas.mpl_disconnect(self.click_image)
            self.statusBar().showMessage('View mode change to scroll mode enabled!', 1500)
        except:
            self.statusBar().showMessage('Try loading image first or try again!', 2500)
            
    # Select axes for drawing rectangle
    # Select Transverse Plane axes
    def ax_tran_enabled(self):
        try:
            self.plot_images('ax_tran')
            self.statusBar().showMessage('Transverse Plane Enabled for drawing', 1500)
        except:
            self.statusBar().showMessage('Try loading image first or try again!', 2500)
            
    # Select Frontal Plane axes
    def ax_fron_enabled(self):
        try:
            self.plot_images('ax_fron')
            self.statusBar().showMessage('Frontal Plane Enabled for drawing', 1500)
        except:
            self.statusBar().showMessage('Try loading image first or try again!', 2500)
            
    def ax_sagi_enabled(self):
        try:
            self.plot_images('ax_sagi')
            self.statusBar().showMessage('Sagittal Plane Enabled for drawing', 1500)
        except:
            self.statusBar().showMessage('Try loading image first or try again!', 2500)
            
            
    # Plot the image using pixel data
    def plot_images(self, ax_select = False):
        # Define fig, canvas and subplots
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        ax_tran = fig.add_subplot(221, adjustable='box', aspect='auto')
        ax_fron = fig.add_subplot(325, adjustable='box', aspect='auto')
        ax_sagi = fig.add_subplot(326, adjustable='box', aspect='auto')
        
        # To display Patient information
        ax_info = fig.add_subplot(222, adjustable='box', aspect='auto')
        if self.new_matdata_path:
            id = Patient(self.new_matdata_path, 'PatientID')
            name = Patient(self.new_matdata_path, 'PatientName')
            age = Patient(self.new_matdata_path, 'PatientAge')
            
            id_str = id.patient_dict()
            name_str = name.patient_dict()
            age_str = age.patient_dict()
            
            patient_id = re.findall('\d+', id_str)
            patient_name = re.findall('\w+', name_str)
            patient_age = re.findall('\w+', age_str)
            
            txt_id = ax_info.text(0.1, 0.8, 'patient ID: ' + patient_id[0], color='k')
            txt_name = ax_info.text(0.1, 0.6, 'patient name: ' + patient_name[0], color='k')
            tex_age = ax_info.text(0.1, 0.4, 'patient age: ' + patient_age[0], color='k')
        else:
            txt_id = ax_info.text(0.1, 0.8, 'patient ID: ' + 'No Header file', color='k')
            patient_id = ['No_Header_file']
            
        # To display image
        im_dis = ImageDisplay(self.vol_tran, self.vol_fron, self.vol_sagi, ax_tran, ax_fron, ax_sagi)
        im_dis.initialize_transverse_display()
        im_dis.initialize_frontal_display()
        im_dis.initialize_sagittal_display()
        
        # To draw rectangle on axes
        if ax_select == 'ax_tran':
            self.ax_enabled = ax_tran
        elif ax_select == 'ax_fron':
            self.ax_enabled = ax_fron
        elif ax_select == 'ax_sagi':
            self.ax_enabled = ax_sagi
        else:
            self.ax_enabled = False
            
        if self.ax_enabled: self.roi = RectSelector(fig, self.ax_enabled, patient_id)
       
        # Initialize click controller and scroll controller
        self.event_ctrl = ClickController(fig, im_dis, self.vol_tran, self.vol_fron, self.vol_sagi, \
                                          ax_tran, ax_fron, ax_sagi)
        self.roi_ctrl = ScrollController(fig, im_dis, self.vol_tran, self.vol_fron, self.vol_sagi, \
                                      ax_tran, ax_fron, ax_sagi)
        
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
    