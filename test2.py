# 'import contents in test1'
# from test import Student
# student=Student()
# print(Student.name)
# print(str(Student.age))
# student.print_file()
# '先定义student=Student()再调用'
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#np.all(np.diff(xp) > 0)
# xp = [1, 2, 3]
# fp = [3, 2, 0]
# a=np.interp(2.5, xp, fp)
#
# b=np.interp([0, 1, 1.5, 2.72, 3.14], xp, fp)
#
# UNDEF = -99.0
#
# c=np.interp(3.14, xp, fp, right=UNDEF)

##########
from scipy import interpolate
# x = np.arange(-5.01, 5.01, 0.25)
# y = np.arange(-5.01, 5.01, 0.25)
# xx, yy = np.meshgrid(x, y)
# z = np.sin(xx**2+yy**2)
# f = interpolate.interp2d(x, y, z, kind='cubic')
#
# xnew = np.arange(-5.01, 5.01, 1e-2)
# ynew = np.arange(-5.01, 5.01, 1e-2)
# znew = f(xnew, ynew)
# plt.plot(x, z[0, :], 'ro-', xnew, znew[0, :], 'b-')
# plt.show()

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import imag from cap2
# Set up grid and array of values
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
x1 = np.arange(10)

# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
x2 = np.arange(10)

arr = x1 + x2[:, np.newaxis]

# Set up grid for plotting
X, Y = np.meshgrid(x1, x2)

# Plot the values as a surface plot to depict
fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, arr, rstride=1, cstride=1, cmap=cm.jet,
                       linewidth=0, alpha=0.8)
fig.colorbar(surf, shrink=0.5, aspect=5)

from scipy.interpolate import interpn

interp_x = 3.5           # Only one value on the x1-axis
interp_y = np.arange(10) # A range of values on the x2-axis

# Note the following two lines that are used to set up the
# interpolation points as a 10x2 array!
interp_mesh = np.array(np.meshgrid(interp_x, interp_y))
interp_points = np.rollaxis(interp_mesh, 0, 3).reshape((10, 2))

# Perform the interpolation
interp_arr = interpn((x1, x2), arr, interp_points)

# Plot the result
ax.scatter(interp_x * np.ones(interp_y.shape), interp_y, interp_arr, s=20,
           c='k', depthshade=False)
plt.xlabel('x1')
plt.ylabel('x2')

plt.show()