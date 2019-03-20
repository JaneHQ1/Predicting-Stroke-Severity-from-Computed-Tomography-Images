'''

'''
import nibabel as nib
import matplotlib.pyplot as plt
from fig_events import *


path = r"C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\TestSample\nifti_2\ARTERIELLE.nii.gz"
struct = nib.load(path)
struct_arr = struct.get_fdata()
# multi_plane_viewer(struct_arr)

vol_tran = struct_arr.transpose(2, 1, 0)
vol_fron = struct_arr.transpose(1, 2, 0)
vol_sagi = struct_arr.transpose(0, 2, 1)

fig = plt.figure()
ax_tran = fig.add_subplot(221)
# plt.axis('off')
ax_tran.index = vol_tran.shape[0] // 2
ax_tran.imshow(vol_tran[ax_tran.index], cmap="gray")

ax_fron = fig.add_subplot(223)
# plt.axis('off')
ax_fron.index = vol_fron.shape[0] // 2
ax_fron.imshow(vol_fron[ax_fron.index], cmap="gray")

ax_sagi = fig.add_subplot(224)
# plt.axis('off')
ax_sagi.index = vol_sagi.shape[0] // 2
ax_sagi.imshow(vol_sagi[ax_sagi.index], cmap="gray")

im_update = ImUpdate(vol_tran, vol_fron, vol_sagi, ax_tran, ax_fron, ax_sagi)
fig.canvas.mpl_connect('button_press_event', im_update.control_events)

# cursor = Cursor(ax_tran, ax_fron, ax_sagi, vol_tran, vol_fron, vol_sagi)
# plt.connect('button_press_event', Cursor.check)


plt.show()
