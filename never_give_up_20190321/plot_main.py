'''

'''
import nibabel as nib
import matplotlib.gridspec as gridspec
from fig_events import *
from patient_info import *



path = r"C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\TestSample\nifti_2\ARTERIELLE.nii.gz"
path_matdata = r"C:\Users\janej\OneDrive\MelbUni\MASTER OF ENGINEERING\CapstoneProject_2018\Test_Images\TestSample\nifti_2\dcmHeaders.mat"
struct = nib.load(path)
struct_arr = struct.get_fdata()
# multi_plane_viewer(struct_arr)

tran_arr = struct_arr.transpose(2, 1, 0)
fron_arr = struct_arr.transpose(1, 2, 0)
sagi_arr = struct_arr.transpose(0, 2, 1)

vol_tran = np.flip(tran_arr)
vol_fron = np.flip(fron_arr)
vol_sagi = np.flip(sagi_arr)

fig = plt.figure()
# fig = plt.figure(constrained_layout=True)
# gs0 = gridspec.GridSpec(1, 2, figure=fig)
# gs1 = gridspec.GridSpecFromSubplotSpec(2, 2, subplot_spec=gs0[0], width_ratios=[2, 2], height_ratios=[2, 2])
# gs2 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[1])
# ax_tran = fig.add_subplot(gs1[0, :])
ax_tran = fig.add_subplot(221, adjustable='box', aspect='auto')
# fig.ax_tran.set_size_inches(10, 10)
# plt.axis('off')
ax_tran.index = vol_tran.shape[0] // 2
ax_tran.imshow(vol_tran[ax_tran.index], cmap="gray")

ax_fron = fig.add_subplot(325, adjustable='box', aspect='auto')
# plt.axis('off')
ax_fron.index = vol_fron.shape[0] // 2
ax_fron.imshow(vol_fron[ax_fron.index], cmap="gray")

ax_sagi = fig.add_subplot(326, adjustable='box', aspect='auto')
# plt.axis('off')
ax_sagi.index = vol_sagi.shape[0] // 2
ax_sagi.imshow(vol_sagi[ax_sagi.index], cmap="gray")

ax_info = fig.add_subplot(222, adjustable='box', aspect='auto')
plt.axis('off')

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

plt.tight_layout()
# gs0.tight_layout(fig, rect=[0, 0, 1, 1], h_pad=0.1, w_pad=0.1)
# gs2.tight_layout(fig, rect=[0, 0, 1, 1], h_pad=0.5)



im_update = ImUpdate(vol_tran, vol_fron, vol_sagi, ax_tran, ax_fron, ax_sagi)
fig.canvas.mpl_connect('button_press_event', im_update.control_events)
plt.show()

