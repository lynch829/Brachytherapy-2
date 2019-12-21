###########################################################################################
#
#   Script name: xx-OncentraDose
#
#   Description: Tool for processing of Oncentra dose files
#
#   Example usage: python x-OncentraReportReader "/file/"
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
import matplotlib.pyplot as plt
from mayavi import mlab






# axial visualization and scrolling
def multi_slice_viewer(volume, origin, dx, dy, dz):
    # remove_keymap_conflicts({'j', 'k'})
    fig, ax = plt.subplots()
    ax.volume = volume
    ax.index = volume.shape[2] // 2
    # print(ax.index)
    print(origin,volume.shape)
    extent = (origin[0], origin[0] + (volume.shape[0] * dx),
              origin[1]+ (volume.shape[1] * dy), origin[1])
    ax.imshow(volume[:, :, ax.index], extent=extent, origin='upper')
    # ax.imshow(np.transpose(volume[:, :, ax.index]))
    ax.set_xlabel('x distance [mm]')
    ax.set_ylabel('y distance [mm]')
    ax.set_title("slice=" + str(ax.index)+ " , z="+ str(origin[2]-ax.index*dz)+' mm')
    fig.suptitle('Axial view', fontsize=16)
    args=[origin,dx,dy,dz]
    fig.canvas.mpl_connect('key_press_event', lambda event: process_key_axial(event, origin, dx, dy, dz))


def process_key_axial(event, origin, dx, dy, dz):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.key == 'b':
        previous_slice_axial(ax)
    elif event.key == 'n':
        next_slice_axial(ax)
    ax.set_title("slice=" + str(ax.index)+ " , z="+ str(origin[2]-ax.index*dz)+' mm')
    fig.canvas.draw()
from mayavi import mlab


def previous_slice_axial(ax):
    volume = ax.volume
    ax.index = (ax.index - 1) % volume.shape[2]  # wrap around using %
    print(ax.index, volume.shape[2])
    ax.images[0].set_array(np.transpose(volume[:, :, ax.index]))


def next_slice_axial(ax):
    volume = ax.volume
    ax.index = (ax.index + 1) % volume.shape[2]
    print(ax.index, volume.shape[2])
    ax.images[0].set_array(np.transpose(volume[:, :, ax.index]))









def process_file(filename):
    print('Starting dose calculation')
    dataset = pydicom.dcmread(filename)
    print(dataset)
    ArrayDicom = np.zeros((dataset.Rows, dataset.Columns, 0), dtype=dataset.pixel_array.dtype)
    ArrayDicom = dataset.pixel_array
    # print(np.shape(ArrayDicom))
    # plt.figure()
    # plt.imshow(ArrayDicom[:,:,5])
    # plt.show()



    # print("slice thickness [mm]=", dataset.SliceThickness)
    # SID = dataset.RTImageSID
    # dx = 1 / (SID * (1 / dataset.ImagePlanePixelSpacing[0]) / 1000)
    # dy = 1 / (SID * (1 / dataset.ImagePlanePixelSpacing[1]) / 1000)
    dz = dataset.SliceThickness
    dy,dx = dataset.PixelSpacing
    origin = dataset[0x0020, 0x0032].value
    print("pixel spacing depth [mm]=", dz)
    print("pixel spacing row [mm]=", dy)
    print("pixel spacing col [mm]=", dx)
    print('origin=',origin)
    # print(dataset)
    # print('comment',dataset.DoseComment)

    # x= np.linspace(origin[0],origin[0] + (ArrayDicom.shape[2] * dx)
    # y= np.linspace(origin[1],origin[1] + (ArrayDicom.shape[1] * dy)
    # z= np.linspace(origin[2],origin[2] - (ArrayDicom.shape[0] * dz)

    x, y, z = np.mgrid[origin[0]:origin[0] + (ArrayDicom.shape[2] * dx):dx,
              origin[1]:origin[1] + (ArrayDicom.shape[1] * dy):dy,
              origin[2] - (ArrayDicom.shape[0] * dz):origin[2]:dz]
    print(np.shape(x),np.shape(y),np.shape(z))
    print(np.shape(ArrayDicom))
    volume=np.flip(np.swapaxes(ArrayDicom,axis1=0,axis2=2),axis=2)
    print('shape_oncentra_dose=',np.shape(volume))
    

    # mlab.clf()
    # mlab.volume_slice(x, y, z, volume, plane_orientation='z_axes' )
    #
    #
    # mlab.show()





    multi_slice_viewer(volume, origin, dx, dy, dz)
    plt.show()


    # Normal mode:
    print()
    print("File name.........:", filename)
    print("Storage type.....:", dataset.SOPClassUID)
    print()

    pat_name = dataset.PatientName
    display_name = pat_name.family_name + ", " + pat_name.given_name
    print("Patient's name...:", display_name)
    print("Patient id.......:", dataset.PatientID)
    print("Modality.........:", dataset.Modality)
    print("Study Date.......:", dataset.StudyDate)
    # print("Gantry angle......", dataset.GantryAngle)





try:
    filename = str(sys.argv[1])
    print(filename)
except:
    print('Please enter a valid filename')
    print("Use the following command to run this script")
    print("python xx-OncentraDose.py \"[dirname]\"")




# while True:  # example of infinite loops using try and except to catch only numbers
#     line = input('Are the files compressed [yes(y)/no(n)]> ')
#     try:
        ##       if line == 'done':
        ##           break
        # poption = str(line.lower())
        # if poption.startswith(('y', 'yeah', 'yes', 'n', 'no', 'nope')):
        #     break
    #
    # except:
    #     print('Please enter a valid option:')



process_file(filename)
