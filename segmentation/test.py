import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from sklearn import preprocessing

import os.path

# path = r"E:\Training Batch 1\segmentation-0.nii"
# struct = nib.load(path)
# struct_arr = struct.get_fdata()

# source_folder = r'E:\Training Batch 1'
#
# for file_name in os.listdir(source_folder):
#     data = nib.load(os.path.join(source_folder, file_name))
#     data = data.get_data()
#     test = 1

'''
path = r"E:\Training Batch 1\volume-118.nii"
struct = nib.load(path)
struct_arr = struct.get_fdata()
# test_arr = struct_arr[200].T
std = np.std(struct_arr, dtype=np.float64)

# print(norm_arr)
print(std)
std_arr = struct_arr/std
std_arr2 = np.clip(struct_arr, -200, 200) / 400.0
norm_arr = preprocessing.normalize(struct_arr[200])
std_arr3 = preprocessing.StandardScaler().fit_transform(struct_arr[200])



# print ("pixel array = ", ds1.pixel_array.shape)
print("minimum value = ", np.amin(std_arr2)) # find minimum pixel value in the image array
print("maximum value = ", np.amax(std_arr2)) # find maximum pixel value in the image array

print("minimum value = ", np.amin(struct_arr)) # find minimum pixel value in the image array
print("maximum value = ", np.amax(struct_arr)) # find maximum pixel value in the image array

plt.figure()
plt.subplot(121)
plt.hist(norm_arr.flatten(), bins=64)  # calculate a histogram of our image
plt.subplot(122)
# plt.imshow(norm_arr, cmap="gray")
plt.hist(struct_arr[200].flatten(), bins=64)  # calculate a histogram of our image
test = 1
plt.show()

'''

'''
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
zipped = zip(x[len(x)//2:], x[:len(x)//2])
# a, b = zipped
for i in zipped:
    print(i)
'''

import torch
import torch.nn as nn
from torch.autograd import Variable

output = Variable(torch.FloatTensor([0, 0, 0, 1])).view(1, -1)
target = Variable(torch.LongTensor([3]))

criterion = nn.CrossEntropyLoss()
loss = criterion(output, target)
print(loss)

a = torch.FloatTensor([0, 0, 0, 1]).view(1, -1)
print(a)