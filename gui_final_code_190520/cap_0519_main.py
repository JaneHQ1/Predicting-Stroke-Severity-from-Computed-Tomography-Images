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
from cap_0519_display import ImageDisplay
from cap_0519_ccontroller import ClickController
from cap_0519_scontroller import ScrollController
from cap_0519_roi import SingleWindowCtr
from cap_0519_segmen import ValidateWindowCtr
from cap_0519_patient import *


# Window to display image in single axes
class ValidateWindow(QMainWindow):
    def __init__(self, vol_trans, vol_truth, vol_segmen, index_trans, index_truth, index_segmen):
        super().__init__()
        self.vol_trans = vol_trans
        self.vol_truth = vol_truth
        self.vol_segmen = vol_segmen
        self.index_trans = index_trans
        self.index_truth = index_truth
        self.index_segmen = index_segmen
        
        # Set validation window dimension and title; and plot
        self.setWindowIcon(QIcon('menu_icon/uomLog.png'))
        self.setWindowTitle('Validation of Medical Image Segmentation')
        self.setGeometry(450, 50, 650, 650)
        self.plot_validate_image()
        
    # Plot two image side by side on the window
    def plot_validate_image(self):
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        ax_trans = fig.add_subplot(223, adjustable='box', aspect='auto')
        im_trans = ax_trans.imshow(self.vol_trans[self.index_trans[-1]], cmap="gray")
        ax_trans.set_title('Voxel Image', color = 'b')
        
        ax_truth = fig.add_subplot(221, adjustable='box', aspect='auto')
        im_truth = ax_truth.imshow(self.vol_truth[self.index_truth[-1]], cmap="gray")
        ax_truth.set_title('Ground Truth Image', color = 'b')
        
        ax_segmen = fig.add_subplot(222, adjustable='box', aspect='auto')
        im_segmen = ax_segmen.imshow(self.vol_segmen[self.index_segmen[-1]], cmap="gray")
        ax_segmen.set_title('Segmented Image', color = 'b')
        
        self.segmen_ctrl = ValidateWindowCtr(fig, im_trans, im_truth, im_segmen, self.vol_trans, self.vol_truth, 
                                             self.vol_segmen, ax_trans, ax_truth, ax_segmen, self.index_trans, 
                                             self.index_truth, self.index_segmen)
        
        # Display canvas of Matplotlib as central Widget
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QVBoxLayout())
        self.widget.layout().addWidget(self.canvas)
        
#   Window to display ROI data
class RoiWindow(QMainWindow):
    def __init__(self, roi_data):
        super().__init__()
        self.roi_data = roi_data
        self.roi_window()
        
    # ROI toolbar and window
    def roi_window(self):
        # Set roi window dimension and title
        self.setWindowIcon(QIcon('menu_icon/uomLog.png'))
        self.setWindowTitle('Current Region of Interest data')
        self.setGeometry(175, 75, 850, 350)
        
        # Create toolbar to save and close data
        # ROI save toolbar
        toolbar = self.addToolBar('ROI save and close')
        save_action = QAction(QIcon('menu_icon/file_save.png'), 'Save ROI data', self)
        save_action.triggered.connect(self.save_roi_data)
        toolbar.addAction(save_action)
        
        # ROI close toolbar
        close_action = QAction(QIcon('menu_icon/file_close.png'), 'Close ROI window', self)
        close_action.triggered.connect(self.close)
        toolbar.addAction(close_action)
        
        # Display current roi data
        self.create_table()
        self.main_widget = QWidget(self)
        layout = QVBoxLayout(self.main_widget)
        layout.addWidget(self.tableWidget)
        self.setCentralWidget(self.main_widget)
    
    # Function to save roi data
    def save_roi_data(self):
        text_file = open('roi_data_file.txt', 'a')
        print(len(self.roi_data))
        for items in self.roi_data:
            for item in items:
                text_file.write(str(item) + '     ')
            text_file.write('\n')
            
        # Open saved text file
        os.startfile('roi_data_file.txt')
        text_file.close()
    
    # Function to create table and show roi data     
    def create_table(self):
        table_headings = ['Patient_ID', 'Plane', 'Slice No', 'x_1', 'y_1', 'x_2', 'y_2', 'Remove']   
        self.tableWidget = QTableWidget()
        if len(self.roi_data) > 0:
            self.tableWidget.setRowCount(len(self.roi_data)+1)
            self.tableWidget.setColumnCount(len(table_headings))
            
            for i in range(len(self.roi_data)+1):
                for j in range(len(table_headings)):
                    if i == 0 or j == len(table_headings)-1:
                        if i == 0:
                            self.tableWidget.setItem(i, j, QTableWidgetItem(table_headings[j]))
                        else:
                            self.tableWidget.setItem(i,j, QTableWidgetItem("Delete"))
                            self.tableWidget.item(i,j).setBackground(QColor(66,116,245))
                    else:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.roi_data[i-1][j])))
        else:
            self.statusBar().showMessage('First update the region of interest!', 2500)
            
        # Double click to delete
        self.tableWidget.doubleClicked.connect(self.delete_row)
        
    # To delete the rows
    def delete_row(self):
        for tblItem in self.tableWidget.selectedItems():
            if tblItem.text() == 'Delete':
                self.roi_data.pop(tblItem.row()-1)
                self.tableWidget.removeRow(tblItem.row())
                
                
# Window to display image in single axes
class SingleWindow(QMainWindow):
    def __init__(self, ax_name, vol_data, ax_index, roi_data, pat_id):
        super().__init__()
        self.ax_name = ax_name
        self.vol_data = vol_data
        self.ax_index = ax_index
        self.roi_data = roi_data
        self.pat_id = pat_id
        
        self.roi_data_tem = []
        self.menu_single_window()
        
    # Menu and toolbar for the window
    def menu_single_window(self):
        # Set single window dimension and title
        self.setWindowIcon(QIcon('menu_icon/uomLog.png'))
        self.setWindowTitle('Single Axes Image ')
        self.setGeometry(750, 50, 600, 600)
        
        # Update roi data toolbar
        toolbar = self.addToolBar('Update roi data and clear window')
        update_action = QAction(QIcon('menu_icon/file_open.png'), 'Update ROI data', self)
        update_action.triggered.connect(self.updata_roi_data)
        toolbar.addAction(update_action)
        
        clear_action = QAction(QIcon('menu_icon/file_file_1.png'), 'Clear window', self)
        clear_action.triggered.connect(self.plot_single_image)
        toolbar.addAction(clear_action)
        
        close_action = QAction(QIcon('menu_icon/file_close.png'), 'Close single window', self)
        close_action.triggered.connect(self.close)
        toolbar.addAction(close_action)
        
        self.plot_single_image()
        
    # Update ROI data
    def updata_roi_data(self):
        self.roi_data.append(self.roi_data_tem[-1])
        self.statusBar().showMessage('Roi updated!', 1500)
        
    # Plot single image on window
    def plot_single_image(self):
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        ax_single = fig.add_subplot(111, adjustable='box', aspect='auto')
        im_single = ax_single.imshow(self.vol_data[self.ax_index[-1]], cmap="gray")
        ax_single.set_title(self.ax_name, color = 'b')
        
        self.roi_ctrl = SingleWindowCtr(fig, im_single, self.vol_data, ax_single, self.ax_index, self.roi_data_tem, 
                                        self.pat_id, self.ax_name)
        
        # Display canvas of Matplotlib as central Widget
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QVBoxLayout())
        self.widget.layout().addWidget(self.canvas)
        
        
#   Main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.roi_data, self.tran_index, self.fron_index, self.sagi_index = [], [0], [0], [0]
        self.index_truth, self.index_segmen = [0], [0]
        self.menu_window()
        
    # Menubar function
    def menu_window(self):
         # Set main window dimension and title
        self.setWindowIcon(QIcon('menu_icon/uomLog.png'))
        self.setWindowTitle('MP4 Medical Image Processor')
        self.setGeometry(75, 50, 700, 650)
        
        # Create main menu
        main_menu = self.menuBar()
        basic_menu = main_menu.addMenu('Basic')
        analysis_menu = main_menu.addMenu('Image Analysis')
        evalution_menu = main_menu.addMenu('Evaluation')
        
        # Create submenu action and add to main menu
        # Basic submenu
        nifti_action = QAction(QIcon('menu_icon/file_file.png'), 'Load Nifti', self)
        nifti_action.setShortcut('Ctrl+N')
        nifti_action.triggered.connect(self.load_nifti_file)
        basic_menu.addAction(nifti_action)
        
        # Image Analysis submenu
        segmen_action = QAction('Run Segmentation', self)
        segmen_action.triggered.connect(self.load_segmentation_file)
        analysis_menu.addAction(segmen_action)
        
        # Evalution submenu
        gtruth_action = QAction('Search round Truth', self)
        gtruth_action.triggered.connect(self.load_nifti_file)
        evalution_menu.addAction(gtruth_action)
        
        # Create toolbar for most common functions
        toolbar = self.addToolBar('Change Click or scroll View')
        
        # Make image clickable
        cursor_action = QAction(QIcon('menu_icon/mouse_click.png'), 'Image click', self)
        cursor_action.triggered.connect(self.set_click_enabled)
        toolbar.addAction(cursor_action)
        
        # Make image scrollable
        scroll_action = QAction(QIcon('menu_icon/mouse_scroll.png'), 'Image scroll', self)
        scroll_action.triggered.connect(self.set_scroll_enabled)
        toolbar.addAction(scroll_action)
        
        # Zoom Transverse plane image
        tran_action = QAction(QIcon('menu_icon/tran.png'), 'Show transverse plane', self)
        tran_action.triggered.connect(self.show_tran_plane)
        toolbar.addAction(tran_action)
        
        # Zoom Frontal plane image
        fron_action = QAction(QIcon('menu_icon/fron.png'), 'Show frontal plane', self)
        fron_action.triggered.connect(self.show_fron_plane)
        toolbar.addAction(fron_action)
        
        # Zoom Sagittal plane image
        sagi_action = QAction(QIcon('menu_icon/sagi.png'), 'Show sagittal plane', self)
        sagi_action.triggered.connect(self.show_sagi_plane)
        toolbar.addAction(sagi_action)
        
        # Display roi table
        roi_action = QAction(QIcon('menu_icon/table_layout.png'), 'Show roi data', self)
        roi_action.triggered.connect(self.show_roi_data)
        toolbar.addAction(roi_action)
        
        # Direct User to use Menu to display images
        self.statusBar().showMessage('Use Basic Menu to display medical images', 5000)
        
        
    # Extract pixel data from medical image file of NIFTI format
    def load_nifti_file(self):
        try:
            # To extract pixel data
            vol_file_path, _= QFileDialog.getOpenFileName(self, 'Select Medical image', '', 'Image Files (*.nii *.nii.gz)')
            folder_path, vol_name = os.path.split(vol_file_path)
            wexten_name = os.path.splitext(vol_name)[0]
            file_num = wexten_name.split('-')[-1]
            self.gtruth_file_path = folder_path+'\\'+'segmentation-'+file_num+'.nii'
            self.segmen_file_path = folder_path+'\\'+'prediction-'+file_num+'.h5'
            
            nifti_file = nib.load(vol_file_path)
            pixel_arr = nifti_file.get_fdata()*255
            
            tran_arr = pixel_arr.transpose(2, 1, 0)
            fron_arr = pixel_arr.transpose(1, 2, 0)
            sagi_arr = pixel_arr.transpose(0, 2, 1)
            
            self.vol_tran = np.flip(tran_arr)
            self.vol_fron = np.flip(fron_arr)
            self.vol_sagi = np.flip(sagi_arr)
            
            self.tran_index[0] = self.vol_tran.shape[0] // 3
            self.fron_index[0] = self.vol_fron.shape[0] // 2
            self.sagi_index[0] = self.vol_sagi.shape[0] // 2
            
            # To extract header data
            self.new_matdata_path = None
            for file in os.listdir(folder_path):
                if file.endswith('.mat'):                   
                    matdata_path = os.path.join(folder_path, file)
                    self.new_matdata_path = matdata_path.replace(os.sep, '/')
                    
            # Plot the image using pixel data
            self.plot_images()

        except:
            self.statusBar().showMessage('File type not supported or empty !', 2500)
    
    # Extract pixel data from h5 and ground truth file
    def load_segmentation_file(self):
        try:
            # To extract pixel data       
            nifti_file = nib.load(self.gtruth_file_path)
            voxel_nifti = nifti_file.get_fdata()*255
            voxel_segmen = h5py.File(self.segmen_file_path,"r")["predictions"].value
            
            nifti_pixel_arr = np.flip(voxel_nifti.transpose(2, 1, 0))
            segmen_pixel_arr = np.flip(voxel_segmen.transpose(2, 1, 0))
            
            self.index_truth[0] = nifti_pixel_arr.shape[0] // 3
            self.index_segmen[0] = segmen_pixel_arr.shape[0] // 3
            
            # Plot the image using pixel data
            self.valid_window = ValidateWindow(self.vol_tran, nifti_pixel_arr, segmen_pixel_arr, self.tran_index, 
                                               self.index_truth, self.index_segmen)
            self.valid_window.show()
            
        except FileNotFoundError:
            self.statusBar().showMessage(FileNotFoundError, 2500)
            
    # Make image clicking enabled
    def set_click_enabled(self):
        try:
            self.click_image = self.canvas.mpl_connect('button_press_event', self.click_ctrl.button_press_events)
            if self.scroll_image: self.canvas.mpl_disconnect(self.scroll_image)
            self.statusBar().showMessage('View mode change to clickable mode enabled!', 1500)
        except:
            self.statusBar().showMessage('Try loading image first or try again!', 2500)
            
    # Make image scrolling enabled
    def set_scroll_enabled(self):
        try:
            self.scroll_image = self.canvas.mpl_connect('axes_enter_event', self.scroll_ctrl.fig_enter_event)
            if self.click_image: self.canvas.mpl_disconnect(self.click_image)
            self.statusBar().showMessage('View mode change to scroll mode enabled!', 1500)
        except:
            self.statusBar().showMessage('Try loading image first or try again!', 2500)
            
    # Show Transverse plane on single window
    def show_tran_plane(self):
        try:
            self.single_window = SingleWindow('Transverse Plane', self.vol_tran, self.tran_index, self.roi_data, self.pat_id)
            self.single_window.show()
        except:
            self.statusBar().showMessage('Try loading image first or try again!', 1500)
            
    # Show Frontal plane on single window
    def show_fron_plane(self):
        try:
            self.single_window = SingleWindow('Frontal Plane', self.vol_fron, self.fron_index, self.roi_data, self.pat_id)
            self.single_window.show()
        except:
            self.statusBar().showMessage('Try loading image first or try again!', 1500)
            
    # Show Sagittal plane on single window
    def show_sagi_plane(self):
        try:
            self.single_window = SingleWindow('Sagittal Plane', self.vol_sagi, self.sagi_index, self.roi_data, self.pat_id)
            self.single_window.show()
        except:
            self.statusBar().showMessage('Try loading image first or try again!', 1500)
            
    # Open ROI table
    def show_roi_data(self):
        self.roi_window = RoiWindow(self.roi_data)
        self.roi_window.show()
               
    # Plot the image using pixel data
    def plot_images(self):    
        # Define fig, canvas, subplots and initialize roi data set
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        ax_tran = fig.add_subplot(221, adjustable='box', aspect='auto')
        ax_fron = fig.add_subplot(223, adjustable='box', aspect='auto')
        ax_sagi = fig.add_subplot(224, adjustable='box', aspect='auto')
        
        # To display Patient information
        ax_info = fig.add_subplot(222, adjustable='box', aspect='auto')
        ax_info.axis('off')
        
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
            
            ax_info.text(0.1, 0.8, 'patient ID: ' + patient_id[0], color='k')
            ax_info.text(0.1, 0.6, 'patient name: ' + patient_name[0], color='k')
            ax_info.text(0.1, 0.4, 'patient age: ' + patient_age[0], color='k')
            self.pat_id = patient_id[0]
        else:
            ax_info.text(0.1, 0.8, 'patient ID: ' + 'No dcmHeader.mat', color='k')
            self.pat_id = 'No dcmHeader.mat'
            
        # To display image, click image and scroll image 
        im_dis = ImageDisplay(self.vol_tran, self.vol_fron, self.vol_sagi, ax_tran, ax_fron, ax_sagi, self.tran_index, 
                              self.fron_index, self.sagi_index)
        self.click_ctrl = ClickController(fig, im_dis, self.vol_tran, self.vol_fron, self.vol_sagi, ax_tran, 
                                          ax_fron, ax_sagi, self.tran_index, self.fron_index, self.sagi_index)
        self.scroll_ctrl = ScrollController(fig, im_dis, self.vol_tran, self.vol_fron, self.vol_sagi, ax_tran, 
                                            ax_fron, ax_sagi, self.tran_index, self.fron_index, self.sagi_index)
        
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
    