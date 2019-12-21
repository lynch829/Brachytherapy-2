###########################################################################################
#
#   Script name: oncdvh
#
#   Description: Tool for processing of Oncentra structure files
#
#   Example usage: python oncdvh "/file/"
#
#   Author: Pedro Martinez
#   pedro.enrique.83@gmail.com
#   5877000722
#   Date:2019-05-10
#
###########################################################################################



import os
import sys
sys.path.append('C:\Program Files\GDCM 2.8\lib')
import pydicom
import numpy as np
import re
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as colors
import scipy as sp
import oncstruct
import oncdose
from mayavi import mlab
from dicompylercore import dicomparser, dvh, dvhcalc
from matplotlib.path import Path
import dvhcalc
import argparse


matplotlib.use('Qt5Agg')


def argmin_values_along_axis(arr, value, axis):
    argmin_idx = np.abs(arr - value).argmin(axis=axis)
    shp = arr.shape
    indx = list(np.ix_(*[np.arange(i) for i in shp]))
    indx[axis] = np.expand_dims(argmin_idx, axis=axis)
    # return np.squeeze(arr[indx])
    return np.squeeze(indx)


try:
    structname = str(sys.argv[1])
    print(structname)
except:
    print('Please enter a valid filename')
    print("Use the following command to run this script")
    print("python oncdvh \"[structures dicom]\" \"[dose dicom]\"")


try:
    dosename = str(sys.argv[2])
    print(dosename)
except:
    print('Please enter a valid filename')
    print("Use the following command to run this script")
    print("python oncdvh  \"[dose dicom]\" \"[structures dicom]\"")


parser = argparse.ArgumentParser()
parser.add_argument('dose',type=str,help="Input the dose file")
parser.add_argument('structure',type=str,help="Input the structure file")
#parser.add_argument('-s', '--structure', nargs='?', type=argparse.FileType('r'), help='structure file, in DICOM format')
args=parser.parse_args()

if args.dose:
    dosename=args.dose
    x,y,z,dx,dy,dz,volume=oncdose.process_file(dosename)  
    print('dx=',dx,'dy=',dy,'dz=',dz,'dose volume',np.shape(volume))

if args.structure:
    structname = args.structure
    structures = pydicom.dcmread(structname)

    

plt.figure()

#we need to get an accurate dose resolution to perform the calculations



for k in range(0,structures[0x3006,0x0039].VM):
    print(dx,dy)
    calcdvh = dvhcalc.get_dvh(structname, dosename, k, interpolation_resolution=(dy,dx), interpolation_segments_between_planes=10).relative_volume
    # calcdvh = dvhcalc.get_dvh(structname, dosename, k).relative_volume
    # calcdvh.volume_units = '%'
    # print(calcdvh.relative_volume)
    calcdvh.plot()

plt.show()


# calcdvh=dvhcalc.get_dvh(structname,dosename,0)
# print(calcdvh.describe())
# print(calcdvh.cumulative)
# plt.figure()
# calcdvh.plot()
# plt.show()
exit(0)



























#from here below I was trying to do the DVH by myself. exercise to do in the future!!

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.set_xlabel('x distance [mm]')
# ax.set_ylabel('y distance [mm]')
# ax.set_zlabel('z distance [mm]')
#
#
# mlab.figure(bgcolor=(1,1,1), fgcolor=(0.,0.,0.))
# scene = mlab.gcf().scene
# scene.renderer.use_depth_peeling=1
#
# #using mayavi
# x,y,z,volume=oncdose.process_file(dosename)
# # print(np.shape(z),z[1,:,:])
# mlab.volume_slice(x, y, z, volume, plane_orientation='z_axes')
# mlab.colorbar(title='Dose [cGy]', orientation='vertical', )
# elem_data=oncstruct.process_file(structname)
#
#
# #lets get the first polygon
# xp=[]
# yp=[]
# zp=[]
# color_r=[]
# color_g=[]
# color_b=[]
# layer=[]
# for i in range(0,2000):
#     if elem_data[i,6]=='18':
#         xp.append(elem_data[i,7])
#         yp.append(elem_data[i,8])
#         zp.append(elem_data[i,9])
#         color_r=elem_data[i,3]
#         color_g=elem_data[i,4]
#         color_b=elem_data[i,5]
#         layer.append(elem_data[i,6])
#
#
# # print(layer,xp,yp,zp)
# color_rgb=[color_r,color_g,color_b]
# xt=np.asarray(xp).astype(np.float)
# yt=np.asarray(yp).astype(np.float)
# zt=np.asarray(zp).astype(np.float)
#
#
# ax.set_xlim3d(np.min(xt), np.max(xt))
# ax.set_ylim3d(np.min(yt), np.max(yt))
# ax.set_zlim3d(np.min(zt), np.max(zt))
# hex_color = colors.rgb2hex(np.asarray(color_rgb).astype(np.float) / 255)
#
#
# #code to create a mask to apply to the dose volume
# #-------------------------------------------------------
# # import numpy as np
# # from matplotlib.path import Path
# #
# # nx, ny = 10, 10
# # poly_verts = [(1,1), (5,1), (5,9),(3,2),(1,1)]
# #
# # # Create vertex coordinates for each grid cell...
# # # (<0,0> is at the top left of the grid in this system)
# # x, y = np.meshgrid(np.arange(nx), np.arange(ny))
# # x, y = x.flatten(), y.flatten()
# #
# # points = np.vstack((x,y)).T
# #
# # path = Path(poly_verts)
# # grid = path.contains_points(points)
# # grid = grid.reshape((ny,nx))
# #
# # print grid
# #-------------------------------------------------------
#
#
# print(np.shape(xt),np.shape(x),x[:,0,0],x[0,:,0],x[0,0,:])
# xdim=np.shape(x)[0]
# ydim=np.shape(x)[1]
# x=x[:,:,0].flatten()
# y=y[:,:,0].flatten()
# points=np.vstack((x,y)).T
# # for matplotlib3d
# verts = [list(zip(xt, yt, zt))]
# # print(np.vstack((xt,yt)))
# path=Path(np.vstack((xt,yt)).T)
# mask=path.contains_points(points)
# mask=mask.reshape((xdim,ydim))
#
# plt.figure()
# plt.imshow(mask.astype(float))
# plt.show(block=False)
#
#
#
#
#
#
#
# poly=Poly3DCollection(verts,alpha=1)
# #poly.set_color(hex_color)
# poly.set_edgecolor('k')
# ax.add_collection3d(poly)
# ax.view_init(elev=-140,azim=-25)
# plt.show(block=False)
#
#
#
#
#
#
#
#
#
# # nearest volume layer
# # print(np.shape(volume),np.shape(argmin_values_along_axis(arr=z,value=zt[0],axis=2)),argmin_values_along_axis(arr=z,value=zt[0],axis=2))
# nvollay=int(argmin_values_along_axis(arr=z,value=zt[0],axis=2)[2][0][0])
# print('nearest volume layer=',nvollay)
# #print(np.shape(argmin_values_along_axis(arr=z,value=zt[0],axis=2)))
# print('Nearest slice=',np.shape(volume)[2]-nvollay) # since volume matrix starts from the back
# print(zt[0],np.shape(z),z[0][0][nvollay]) # since matrix z starts from the begining
# #zt -> value from the structure
# #z  -> value from the dose matrix
#
#
# #show nearest slide
# # plt.figure()
# # plt.imshow(np.transpose(volume[:,:,np.shape(volume)[2]-nvollay]))
# # #plt.imshow(np.transpose(volume[:,:,1]))
# # #plt.imshow(np.transpose(volume[:,:,20]))
# # plt.title(str(np.shape(volume)[2]-nvollay))
# # plt.show()
# plt.figure()
# plt.imshow(np.multiply(mask,volume[:,:,np.shape(volume)[2]-nvollay]))
# plt.show()
#
#
# if zt[0] > z[0][0][nvollay]:
#     print('1',z[0][0][nvollay],zt[0],z[0][0][nvollay+1])
# else:
#     print('2',z[0][0][nvollay-1],zt[0],z[0][0][nvollay])
#
#
# exit(0)
#
# # ax=mlab.axes(nb_labels=8)
# # ax.axes.font_factor=1
# # mlab.show()

