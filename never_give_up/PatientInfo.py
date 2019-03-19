'''
Jin Ma
'''
import nibabel as nib
import os
import numpy as np
import scipy.io
import struct

class Patient(object):
    def __init__(self,path,title):
        self.path=path
        self.title=title
        self.dicts = {}
        self.variable = scipy.io.whosmat(self.path)
        self.my_struct = scipy.io.loadmat(self.path)
        self.field_list = np.array(self.variable)
        self.patient_info = self.my_struct[self.field_list[0][0][0]]
        self.info_titles = (self.patient_info[0][0][0][0][0]).dtype
        self.length= len(self.patient_info[0][0][0][0][0])

    def mydict(self):
        for i in range(self.length - 1):
            key = str(self.info_titles.descr[i][0])
            value = str(self.patient_info[0][0][0][0][0][i])
            self.dicts.update({key:value})

        a = 1

    def print_info(self):
        print(self.dicts[self.title])

path = r"C:\Users\Jin\Downloads\dcmHeaders.mat"
p1 = Patient(path, 'PatientName')
p1.mydict()
p1.print_info()


