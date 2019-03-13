# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 00:06:27 2019

@author: janej
"""
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np


def multi_plane_viewer(struct):
    struct_tran = struct.T
    struct_fron = struct.transpose(1, 2, 0)
    struct_sagi = struct.transpose(0, 2, 1)

    fig = plt.figure()
    ax_tran = fig.add_subplot(221)
    ax_tran.volumn = struct_tran
    ax_tran.index = struct_tran.shape[0] // 2
    ax_tran.imshow(struct_tran[ax_tran.index], cmap="gray")

    ax_fron = fig.add_subplot(223)
    ax_fron.volumn = struct_fron
    ax_fron.index = struct_fron.shape[0] // 2
    ax_fron.imshow(struct_fron[ax_fron.index], cmap="gray")

    ax_sagi = fig.add_subplot(224)
    ax_sagi.volumn = struct_sagi
    ax_sagi.index = struct_sagi.shape[0] // 2
    ax_sagi.imshow(struct_sagi[ax_sagi.index], cmap="gray")

    # fig.canvas.mpl_connect('button_press_event', transverse_view)
    # fig.canvas.mpl_connect('button_press_event', frontal_view)
    # fig.canvas.mpl_connect('button_press_event', sagittal_view)
    fig.canvas.mpl_connect('button_press_event', check_axes)


def check_axes(event):
    fig = event.canvas.figure
    ax_tran = fig.axes[0]
    ax_fron = fig.axes[1]
    ax_sagi = fig.axes[2]
    x_index = np.int_(event.xdata)
    y_index = np.int_(event.ydata)

    if ax_tran.contains(event):
        fig.canvas.mpl_connect('button_press_event', frontal_view(event, x_index))
        fig.canvas.mpl_connect('button_press_event', sagittal_view(event, y_index))

    elif ax_fron.contains(event):
        fig.canvas.mpl_connect('button_press_event', transverse_view(event, y_index))
        fig.canvas.mpl_connect('button_press_event', sagittal_view( event, x_index))

    elif ax_sagi.contains(event):
        fig.canvas.mpl_connect('button_press_event', transverse_view(event, y_index))
        fig.canvas.mpl_connect('button_press_event', frontal_view(event,x_index))


def transverse_view(event, index):
    fig = event.canvas.figure
    ax_tran = fig.axes[0]
    volumn = ax_tran.volumn
    # ax_tran.index = np.int_(event.xdata)
    ax_tran.index = index
    ax_tran.images[0].set_array(volumn[ax_tran.index])
    fig.canvas.draw()


def frontal_view(event, index):
    fig = event.canvas.figure
    ax_fron = fig.axes[1]
    volumn = ax_fron.volumn
    # ax_fron.index = np.int_(event.xdata)
    ax_fron.index = index
    ax_fron.images[0].set_array(volumn[ax_fron.index])
    fig.canvas.draw()


def sagittal_view(event, index):
    fig = event.canvas.figure
    ax_sagi = fig.axes[2]
    volumn = ax_sagi.volumn
    # ax_sagi.index = np.int_(event.ydata)
    ax_sagi.index = index
    ax_sagi.images[0].set_array(volumn[ax_sagi.index])
    fig.canvas.draw()


path = r"C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\TestSample\nifti_2\ARTERIELLE.nii.gz"
struct = nib.load(path)
struct_arr = struct.get_fdata()
multi_plane_viewer(struct_arr)
plt.show()






