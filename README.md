Hello Everyone! I divided our GUI part to be 4 tasks:
1. plot x axis view in Matplotlib 
2. plot y axis view in Matplotlib
3. Embed matplotlib graphs into Tkinter
4. Load DICOM and patient info into Tkinter

Jane and Jin are trying to figure our how to plot x and y axis view.
Tenzin will do the embedding part.

This videos are about embedding for your reference:
https://www.youtube.com/watch?v=Zw6M-BnAPP0
https://www.youtube.com/watch?v=kfMSN7JEtAA

Some useful website for understanding DICOM:
https://nipy.org/nibabel/dicom/dicom.html

Some useful websites for plot 3D volumn:
https://www.researchgate.net/post/How_to_create_a_simple_project_to_convert_DICOM_images_to_3d_images
https://www.researchgate.net/post/How_to_measure_the_voxel_size_and_pixel_spacing
https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/

6 Registry of DICOM Data Elements
http://dicom.nema.org/dicom/2013/output/chtml/part06/chapter_6.html

By the way, I've tried some coding, but it doesn't work. You can see the class embed_mat.
I hope we can do the whole project in Object oriented form. And please write description to let others understand your code.
If anyone want to make modification, you can create another branch, if we all agreed than merge to the master branch.

We are a great team! We can do very well for this project!
------------------------------------------------------------------------------------------------------------------------------------------
04/03/2019
Jane:
I read the basic logic of representing 3D volumn through a 2D image, but do not quite understand so far.
I think we need to use Vessel. What is vessel?

Jin:
There are say 160 slices, which means we only have 160 pixels in column, but there are 250 pixels in row. 
Do we need to make 160 pixels to 250 pixels? How?

We understood the logic under 2D to 3D. It is simply 3 calculations:
Conversion from 2D to 3D
Voxel (x, y, z) = Image Plane Position + Row change in X + column change in Y
Where Row change in X = Row vector * Pixel size in X direction * 2D Point location in X direction
Column change in Y = Column vector * Pixel size in Y direction * 2D Point location in Y direction

Having got 3D volumn, how to convert to x,y views?
