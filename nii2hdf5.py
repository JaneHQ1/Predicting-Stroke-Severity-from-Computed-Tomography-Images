import nibabel as nib
import h5py
import os

path="D:/DiCom/Model/pytorch-3dunet/resources/nii_data"
amount=110		# change this to total file number
zip=10


for i in range(amount):
	raw=os.path.join(path,"volume-"+str(i)+".nii")
	label=os.path.join(path,"segmentation-"+str(i)+".nii")
	raw=nib.load(raw).get_fdata()
	label=nib.load(label).get_fdata()
	
	h5_file=h5py.File(os.path.join(path,"data-"+str(i)+".hdf5"),"w")
	h5_file.create_dataset("label",label.shape,dtype="f8",data=label)
	h5_file.create_dataset("raw",raw.shape,dtype="f8",data=raw)
	h5_file.close()
	
	if (i%zip == 0) and (i != 0):
		cmd="WinRAR a -r test.rar "
		for j in range(i-zip,i):
			cmd += "data-"+str(j)+".hdf5 "
		os.system(cmd)
		
		for j in range(i-zip,i):
			os.remove("data-"+str(j)+".hdf5")
	
