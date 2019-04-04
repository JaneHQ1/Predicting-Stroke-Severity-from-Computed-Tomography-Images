'''
print patient information from matdata
Key:
PatientName
PatientID
PatientAge
'''

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


# path_mat = r"C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\TestSample\nifti_2\dcmHeaders.mat"
# id = Patient(path_mat, 'PatientID')
# name = Patient(path_mat, 'PatientName')
# age = Patient(path_mat, 'PatientAge')
#
# id_str = id.patient_dict()
# name_str = name.patient_dict()
# age_str = age.patient_dict()
#
# patient_id = re.findall('\d+', id_str)
# patient_name = re.findall('\w+', name_str)
# patient_age = re.findall('\w+', age_str)


# print(patient_id[0])
# print(patient_name[0])
# print(patient_age[0])


# path_mat = r"C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\TestSample\nifti_2\dcmHeaders.mat"
