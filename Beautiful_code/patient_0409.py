# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:49:57 2019
Title: MP4-Medical Image Processing
@author: MP4 Team

"""
import numpy as np
import scipy.io
import re

class Patient(object):
    def __init__(self, path, title):
        self.path = path
        self.title = title
        self.dicts = {}
        self.variable = scipy.io.whosmat(self.path)
        self.my_struct = scipy.io.loadmat(self.path)
        self.field_list = np.array(self.variable, dtype=object)
        self.patient_info = self.my_struct[self.field_list[0][0][0]]
        self.info_titles = (self.patient_info[0][0][0][0][0]).dtype
        self.length = len(self.patient_info[0][0][0][0][0])

    def patient_dict(self):
        for i in range(self.length - 1):
            key = str(self.info_titles.descr[i][0])
            value = str(self.patient_info[0][0][0][0][0][i])
            self.dicts.update({key: value})

        return self.dicts[self.title]
