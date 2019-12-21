###########################################################################################
#
#   Script name: xx-OncentraStruct
#
#   Description: Tool for processing of Oncentra structure files
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
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as colors
import argparse








def process_plan(filename,fig):
    dataset = pydicom.dcmread(filename)
    source_dataset=[]
    xs=[]
    ys=[]
    zs=[]
    ts=[]
    # print(dataset)
    # exit(0)
    # print(dataset[0x1001, 0x10af][0][0x1001, 0x10c4])  #<-- example of nested tag access
    # print(dataset[0x300a, 0x0230][0][0x300a, 0x0280].VM)
    # print(dataset[0x300a, 0x0230][0][0x300a, 0x0280][0][0x300a, 0x02d0].VM)
    # print(len(dataset[0x300a, 0x0230][0][0x300a, 0x0280]))



    for elem in dataset[0x300a, 0x0230][0][0x300a, 0x0280]:
    #     if elem[0x1001, 0x10c7].value != -1:
    #     print('--------------------------------------------------')
        # print(elem[0x300a, 0x0282]) # channel number
        # print(elem[0x300a, 0x0284]) # channel length
        # print(elem[0x300a, 0x0286]) # channel total time
        for pos in elem[0x300a, 0x02d0]:
            # print(pos[0x300a, 0x02d4]) # position (x,y,z)
            # print(pos[0x300a, 0x02d6]) # weight time
            # print(pos[0x300a, 0x0112]) # control point index
            # source_dataset.append([ elem[0x300a, 0x0282].value, elem[0x300a, 0x0284].value, elem[0x300a, 0x0286].value, pos[0x300a, 0x02d4].value, pos[0x300a, 0x02d6].value])
            x,y,z=pos[0x300a, 0x02d4].value
            source_dataset.append([ elem[0x300a, 0x0282].value, elem[0x300a, 0x0284].value, elem[0x300a, 0x0286].value, pos[0x300a, 0x0112].value, x , y, z, pos[0x300a, 0x02d6].value])

    source_dataset = np.asarray(source_dataset)
    print(source_dataset.shape)
    for i in range(1,source_dataset.shape[0],2):
        x=source_dataset[i,4]
        y=source_dataset[i,5]
        z=source_dataset[i,6]
        tw=source_dataset[i,7]-source_dataset[i-1,7]
        xs.append(x)
        ys.append(y)
        zs.append(z)
        ts.append(tw/100*source_dataset[i,2])
        #print('tw=',tw,source_dataset[i,7],source_dataset[i-1,7])

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs, ys, zs, s=ts)
    # ax.set_xlabel('x distance [mm]')
    # ax.set_ylabel('y distance [mm]')
    # ax.set_zlabel('z distance [mm]')

    # plt.show()


    # # print("slice thickness [mm]=", dataset.SliceThickness)
    # # SID = dataset.RTImageSID
    # # dx = 1 / (SID * (1 / dataset.ImagePlanePixelSpacing[0]) / 1000)
    # # dy = 1 / (SID * (1 / dataset.ImagePlanePixelSpacing[1]) / 1000)
    # dz = dataset.SliceThickness
    # dy,dx = dataset.PixelSpacing
    # print("pixel spacing depth [mm]=", dz)
    # print("pixel spacing row [mm]=", dy)
    # print("pixel spacing col [mm]=", dx)
    # print(dataset)
    # print('comment',dataset.DoseComment)
    #
    #
    # # Normal mode:
    # print()
    # print("File name.........:", filename)
    # print("Storage type.....:", dataset.SOPClassUID)
    # print()
    #
    # pat_name = dataset.PatientName
    # display_name = pat_name.family_name + ", " + pat_name.given_name
    # print("Patient's name...:", display_name)
    # print("Patient id.......:", dataset.PatientID)
    # print("Modality.........:", dataset.Modality)
    # print("Study Date.......:", dataset.StudyDate)
    # # print("Gantry angle......", dataset.GantryAngle)


















def process_struct(filename,fig):
    print('Starting struct calculation')
    dataset = pydicom.dcmread(filename)
    # print(dataset[0x3006,0x0039][0][0x3006,0x0040][0][0x3006,0x0050])




    roi_num=[]
    roi_color=[]

    xs_tot = []
    ys_tot = []
    zs_tot = []





    for elem in dataset[0x3006,0x0039]:
        # print(elem[0x3006, 0x0040].VM)
        # print(elem[0x3006, 0x002a])
        print(elem[0x3006, 0x0084])
        roi_color=elem[0x3006, 0x002a].value
        hex_color=colors.rgb2hex(np.asarray(roi_color)/255)
        roi_num.append(elem[0x3006, 0x0084].value)
        # try:
        #     print(elem[0x3006, 0x0040].VM)
        # except:
        #     print('invalid data')
        try:
            for contour in elem[0x3006,0x0040]:
                xs = []
                ys = []
                zs = []
                # print(contour[0x3006, 0x0046])
                # cdata=np.array(contour[0x3006,0x0050].value).astype(np.float)
                for i in range(0,contour[0x3006,0x0050].VM,3):
                    xs.append(contour[0x3006,0x0050][i])
                    ys.append(contour[0x3006, 0x0050][i+1])
                    zs.append(contour[0x3006, 0x0050][i+2])
                    xs_tot.append(contour[0x3006,0x0050][i])
                    ys_tot.append(contour[0x3006, 0x0050][i+1])
                    zs_tot.append(contour[0x3006, 0x0050][i+2])


                x=np.array(xs).astype(np.float)
                y=np.array(ys).astype(np.float)
                z=np.array(zs).astype(np.float)

                xtot=np.array(xs_tot).astype(np.float)
                ytot=np.array(ys_tot).astype(np.float)
                ztot=np.array(zs_tot).astype(np.float)
                # print(x, y, z)



                verts = [list(zip(x, y, z))]
                # print(verts)

                poly=Poly3DCollection(verts,alpha=0.5)
                poly.set_color(hex_color)
                poly.set_edgecolor('k')
                ax.add_collection3d(poly)
                # ax.auto_scale_xyz(x,y,z)
        except:
            print('no contour data')

    ax.set_xlim3d(np.min(xs_tot), np.max(xs_tot))
    ax.set_ylim3d(np.min(ys_tot), np.max(ys_tot))
    ax.set_zlim3d(np.min(zs_tot), np.max(zs_tot))
    print(roi_color)
    ax.view_init(elev=-140, azim=-25)
    # plt.show()


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





# try:
#     structname = str(sys.argv[1])
#     print(structname)
# except:
#     print('Please enter a valid filename')
#     print("Use the following command to run this script")
#     print("python xx-Oncentra.py \"[structures dicom]\" \"[plan dicom]\"")
#
# try:
#     planname = str(sys.argv[2])
#     print(planname)
# except:
#     print('Please enter a valid filename')
#     print("Use the following command to run this script")
#     print("python xx-Oncentra.py \"[structures dicom]\" \"[plan dicom]\"")


parser = argparse.ArgumentParser()
parser.add_argument('structure',type=str,help="Input the structure file")
parser.add_argument('-p', '--plan', nargs='?', type=argparse.FileType('r'), help='plan file, in DICOM format')
args=parser.parse_args()

structname=args.structure




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



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# ax.scatter(xs, ys, zs)
ax.set_xlabel('x distance [mm]')
ax.set_ylabel('y distance [mm]')
ax.set_zlabel('z distance [mm]')


if args.structure:
    structname=args.structure
    process_struct(structname, fig)
if args.plan:
    planname = args.plan
    process_plan(planname.name,fig)


plt.show()
