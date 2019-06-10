import nibabel as nib
import numpy as np
import h5py
import os


# only supports single file batch for now
def hdf5_it(path, hdf5_path, index):
	os.system("mkdir " + hdf5_path)
	print("Converting nii [%s]" % (index))
	# read nii
	raw=os.path.join(path,"volume-"+str(index)+".nii")
	if not os.path.isfile(raw):
		print("Cannot find file %s, Skip" % (index))
		return False
	label=os.path.join(path,"segmentation-"+str(index)+".nii")
	raw=nib.load(raw).get_fdata()
	label=nib.load(label).get_fdata()
	# select only tumors (2) as positive label
	label = (label == 2).astype(np.uint8)

	# write hdf5
	h5_file=h5py.File(os.path.join(hdf5_path,"data-"+str(index)+".hdf5"),"w")
	h5_file.create_dataset("label",label.shape,dtype="f8",data=label)
	h5_file.create_dataset("raw",raw.shape,dtype="f8",data=raw)
	h5_file.close()
	
	return hdf5_vrfy(hdf5_path,index)

def hdf5_vrfy(hdf5_path,idx):
	try:
		h5py.File(os.path.join(hdf5_path,"data-"+str(idx)+".hdf5"),"r")
		return True
	except:
		print("HDF5 data corrupted, skipped to next file")
		return False
		

