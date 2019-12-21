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
from scipy.spatial.transform import Rotation as R
import datetime as dt
import random as rand
import oncstruct
import argparse










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
        roi_color=elem[0x3006, 0x002a].value # this value is the color of the lesion/structure
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

                poly=Poly3DCollection(verts,alpha=0.05)
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























def process_plan(filename,fig):
    dataset = pydicom.dcmread(filename)
    source_dataset=[]
    xs=[]
    ys=[]
    zs=[]
    ts=[]
    print(dataset[0x300a, 0x004])  #<-- example of nested tag access
    print(dataset[0x300a, 0x006])  #<-- example of nested tag access
    print(dataset[0x300a, 0x007])  #<-- example of nested tag access
    print(dataset[0x0008, 0x0018])  #<-- example of nested tag access
    dataset[0x0020,0x0011].value="9"
    #dataset[0x0020,0x000d].value=str(rand.randint(1,10000))
    instance_rand=str(rand.randint(1,10000))
    dataset[0x0020,0x000e].value=instance_rand # <-- creating a new random series instance
    dataset[0x300c,0x0002][0][0x0008,0x1155].value=instance_rand # <-- replacing the reference value

    new_UID=str(rand.randint(1,10000))
    dataset[0x0008, 0x0018].value=new_UID  #<-- creating a new random SOP instance UID

    print('Maximum number of catheters in dataset =',dataset[0x300a, 0x0230][0][0x300a, 0x0280].VM) # prints the number of catheters

    while True:  # example of infinite loops using try and except to catch only numbers
        line = input('Please enter the catheter number> ')
        try:
            #       if line == 'done':
            #           break
            catnum = int(line.lower())
            if catnum >= 1 and catnum <= dataset[0x300a, 0x0230][0][0x300a, 0x0280].VM:
                break
            else:
                print('Please select a value between 1 and the max number of catheters:')

        except:
            print('Please select a value between 1 and the max number of catheters:')

    catheter=dataset[0x300a, 0x0230][0][0x300a, 0x0280][catnum-1]

    tipcat = np.asarray(catheter[0x1001,0x1080][0][0x1001,0x1083].value) # this variable holds the tip of the catheter
    print('tip catheter=',tipcat)


    #print('Coordinates of the first point=',catheter[0x300a, 0x02d0][0][0x300a, 0x02d4].value)
    xoffset=dataset[0x300a, 0x0230][0][0x300a, 0x0280][catnum-1][0x300a, 0x02d0][0][0x300a, 0x02d4].value[0]
    yoffset=dataset[0x300a, 0x0230][0][0x300a, 0x0280][catnum-1][0x300a, 0x02d0][0][0x300a, 0x02d4].value[1]
    print('xoffset=',xoffset)
    print('yoffset=',yoffset)

    source_dataset=[]
    xs=[]
    ys=[]
    zs=[]
    ts=[]


    for pos in dataset[0x300a, 0x0230][0][0x300a, 0x0280][catnum-1][0x300a, 0x02d0]:
        # print(pos[0x300a, 0x02d4]) # position (x,y,z)
        # print(pos[0x300a, 0x02d6]) # weight time
        # print(pos[0x300a, 0x0112]) # control point index
        # source_dataset.append([ elem[0x300a, 0x0282].value, elem[0x300a, 0x0284].value, elem[0x300a, 0x0286].value, pos[0x300a, 0x02d4].value, pos[0x300a, 0x02d6].value])
        x, y, z = pos[0x300a, 0x02d4].value
        source_dataset.append([catheter[0x300a, 0x0282].value, catheter[0x300a, 0x0284].value, catheter[0x300a, 0x0286].value,
                               pos[0x300a, 0x0112].value, x, y, z, pos[0x300a, 0x02d6].value])

    source_dataset = np.asarray(source_dataset)
    coords=np.transpose(source_dataset[:,4:7])



    for i in range(1, source_dataset.shape[0], 2):
        x = source_dataset[i, 4]
        y = source_dataset[i, 5]
        z = source_dataset[i, 6]
        tw = source_dataset[i, 7] - source_dataset[i - 1, 7]
        xs.append(x)
        ys.append(y)
        zs.append(z)
        ts.append(tw / 100 * source_dataset[i, 2])

    #for matplotlib3d
    ax.scatter(xs, ys, zs, s=ts, label='Catheter(o)='+str(catnum))
    # print(ts)






    while True:  # example of infinite loops using try and except to catch only numbers
        line = input('Please enter the offset value in the z direction [cm]> ')
        try:
            #       if line == 'done':
            #           break
            offset = float(line.lower())
            break

        except:
            print('Please enter a valid option:')

    zoffset=(offset - tipcat[2]) #the point offset in the z direction is the value of the offset minus the tip of the catheter location

    coords_offset=np.zeros_like(coords)
    coords_offset[0,:]=coords[0,:]-xoffset
    coords_offset[1,:]=coords[1,:]-yoffset
    coords_offset[2,:]=coords[2,:]+zoffset

    # preparing the catheter for rotation
    tipcat_offset = np.zeros_like(tipcat)
    tipcat_offset[0] = tipcat[0] - xoffset
    tipcat_offset[1] = tipcat[1] - yoffset
    tipcat_offset[2] = tipcat[2] + zoffset

    print('zoffset=',zoffset)

    #here we update the catheter values where the bending occurs
    needle=catheter[0x1001,0x1080]
    # catheter[0x300a, 0x0291].value='M117X0004-CAT' # changing the type of catheter from virtual
    # dataset[0x1001, 0x10af][0][0x1001,0x10c2].value=-10 #testing this value
    # print(catheter[0x300a, 0x0291])
    x_dup,y_dup,z_dup=needle[0][0x10011083].value #we extract these coordinates from the tip and create another set located at the point where the catheter bends
    dup_elem=pydicom.Dataset()#creating a point where the catheter bends
    dup_elem.add_new(0x10010010,'LO',needle[0][0x1001,0x0010].value)
    dup_elem.add_new(0x10011081,'SL',needle[0][0x1001,0x1081].value+1)
    dup_elem.add_new(0x10011082,'SL',0)
    # dup_elem.add_new(0x10011083,'DS',[x_dup,y_dup,z_dup-zoffset])
    dup_elem.add_new(0x10011083,'DS',[x_dup,y_dup,-zoffset])
    print('elbow point z value=',-zoffset)
    seq_needle=pydicom.DataElement(0x10011080,'SQ',[needle[0],dup_elem,needle[1],needle[2],needle[3]])

    for needle_point in seq_needle[2:]:
        needle_point[0x1001,0x1081].value=needle_point[0x1001,0x1081].value+1
        # needle_point[0x1001,0x1082].value=needle_point[0x1001,0x1082].value+1

    dataset[0x300a, 0x0230][0][0x300a, 0x0280][catnum-1][0x1001,0x1080]=seq_needle


    # del(dataset[0x300c,0x0080]) #deleting the dose dependency (not necessary in a live catheter from Oncentra)




    #print('needle=',*dataset[0x300a, 0x0230][0][0x300a, 0x0280][catnum-1][0x1001,0x1080],sep='\n')

    while True:  # example of infinite loops using try and except to catch only numbers
        line = input('Please enter the theta value [deg]> ')
        try:
            #       if line == 'done':
            #           break
            theta = float(line.lower())
            break

        except:
            print('Please enter a valid option:')

    r1 = R.from_euler('x', theta, degrees=True)
    coords_rot1=np.matmul(np.asarray(r1.as_dcm()),coords_offset)
    tipcatrot1=np.matmul(np.asarray(r1.as_dcm()),tipcat_offset)


    print('coords_offset=',coords_offset,'r1=',r1)
    exit(0)



    while True:  # example of infinite loops using try and except to catch only numbers
        line = input('Please enter the phi value [deg]> ')
        try:
            #       if line == 'done':
            #           break
            phi = float(line.lower())
            break

        except:
            print('Please enter a valid option:')
    



    r2 = R.from_euler('z', phi, degrees=True)
    coords_rot2 = np.matmul(np.asarray(r2.as_dcm()), coords_rot1)
    tipcatrot2 = np.matmul(np.asarray(r2.as_dcm()), tipcatrot1)




    coords_f=coords # creating the array from the initial coordinates in order to "bend" the needle from a certain offset

    for i in range(0,np.shape(coords)[1]):
        if coords_f[2,i]>tipcat[2]-zoffset:
            coords_f[0,i]=coords_rot2[0,i]+xoffset
            coords_f[1,i]=coords_rot2[1,i]+yoffset
            coords_f[2,i]=coords_rot2[2,i]-zoffset

    tipcat_f = np.zeros_like(tipcat)
    tipcat_f[0] = tipcatrot2[0] + xoffset
    tipcat_f[1] = tipcatrot2[1] + yoffset
    tipcat_f[2] = tipcatrot2[2] - zoffset

    catheter[0x1001, 0x1080][0][0x1001, 0x1083].value = [tipcat_f[0], tipcat_f[1], tipcat_f[2]]

    print('theta=',theta,'phi=',phi)
    print('post-transformation',coords_f)
    print(tipcat, tipcatrot1,tipcat_f)
    # exit(0)

#    print(ts)




    ax.scatter(coords_f[0,:], coords_f[1,:], coords_f[2,:], s=ts,label='Catheter(m)='+str(catnum))

    ax.legend()

    k=0
    for pos in dataset[0x300a, 0x0230][0][0x300a, 0x0280][catnum-1][0x300a, 0x02d0]:
        # print(pos[0x300a, 0x02d4]) # position (x,y,z)
        #print('after transformation=',pos[0x300a, 0x02d6]) # weight time
        # print(pos[0x300a, 0x0112]) # control point index
        # source_dataset.append([ elem[0x300a, 0x0282].value, elem[0x300a, 0x0284].value, elem[0x300a, 0x0286].value, pos[0x300a, 0x02d4].value, pos[0x300a, 0x02d6].value])
        pos[0x300a, 0x02d4].value=[coords_f[0,k],coords_f[1,k],coords_f[2,k]]
        k=k+1

    

    while True:  # example of infinite loops using try and except to catch only numbers
        line = input('Please enter a comment for the output file> ')
        try:
            #       if line == 'done':
            #           break
            desc = str(line.lower())
            break

        except:
            print('Please enter a valid option:')
    

    date=dt.date.today().strftime('%Y%m%d')
    now=dt.datetime.now().strftime('%H%M%S')

    dataset[0x300a, 0x004].value=desc
    dataset[0x300a, 0x006].value=date
    dataset[0x300a, 0x007].value=now
    


    dirname = os.path.dirname(filename)
    dataset.save_as(dirname+'/mod-plan.dcm')







# try:
#     structname = str(sys.argv[1])
#     print(structname)
# except:
#     print('Please enter a valid filename')
#     print("Use the following command to run this script")
#     print("python xx-Oncentra.py \"[structures dicom]\" \"[plan dicom]\"")
#
#
# try:
#     planname = str(sys.argv[2])
#     print(planname)
# except:
#     print('Please enter a valid filename')
#     print("Use the following command to run this script")
#     print("python xx-Oncentra.py \"[structures dicom]\" \"[plan dicom]\"")



parser = argparse.ArgumentParser()
parser.add_argument('plan',type=str,help="Input the plan file")
parser.add_argument('-s', '--structure', nargs='?', type=argparse.FileType('r'), help='structure file, in DICOM format')
args=parser.parse_args()

planname=args.plan


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x distance [mm]')
ax.set_ylabel('y distance [mm]')
ax.set_zlabel('z distance [mm]')

# process_struct(structname,fig)
# process_plan(planname,fig)

if args.plan:
    planname=args.plan
    process_plan(planname, fig)
if args.structure:
    structname = args.structure
    process_struct(structname.name,fig)


plt.show()
