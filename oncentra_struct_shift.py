###########################################################################################
#
#   Script name: oncentra_struct_shift
#
#   Description: Tool for processing of Oncentra structure files
#
#   Example usage: python ioncentra_struct_shift "/structure file/" -m dx dy dz -o "/output structure file/"
#
#   Author: Pedro Martinez
#   pedro.enrique.83@gmail.com
#   5877000722
#   Date:2019-05-10
#
###########################################################################################



import os
import sys
import argparse
import pydicom
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as colors
from matplotlib.patches import Polygon
import scipy.spatial as ss
from matplotlib.path import Path
from shapely import geometry
from descartes import PolygonPatch
import alphashape

import chart_studio.plotly as py
import plotly.graph_objects as go
from plotly import tools as tls






os.environ["ETS_TOOLKIT"] = "wx"
np.set_printoptions(threshold=sys.maxsize)






def PolyArea(x, y):
    return 0.5*np.abs(np.dot(x, np.roll(y, 1))-np.dot(y, np.roll(x, 1)))










def process_struct(filename, meas_params, dirname, structname_o, fig):
    print('Starting struct calculation')
    dataset = pydicom.dcmread(filename)




    k = 0
    for elem in dataset[0x3006, 0x0020]:
        print(elem[0x3006, 0x0028].value, k)
        k = k + 1



    while True:  # example of infinite loops using try and except to catch only numbers
        line = input("Select the structure to shift > ")
        try:
            num1 = int(line.lower())    # temporarily since allows any range of numbers
            break
        except ValueError:  # pylint: disable = bare-except
            print("Please enter a valid option:")


    struct_sel_name = dataset[0x3006, 0x0020][num1][0x3006, 0x0028].value


    dz = abs(dataset[0x3006, 0x0039][num1][0x3006, 0x0040][2][0x3006, 0x0050][2] - dataset[0x3006, 0x0039][num1][0x3006, 0x0040][1][0x3006, 0x0050][2])
    print('dz=', dz)
    print(meas_params)

    elem = dataset[0x3006, 0x0039][num1]

    try:
        for contour in elem[0x3006, 0x0040]:  #the area between the two surfaces must be calculated for every contour if there are two areas in each of the contours
            for i in range(0, contour[0x3006, 0x0050].VM, 3):
                contour[0x3006, 0x0050].value[i] = contour[0x3006, 0x0050].value[i] + meas_params[0]
                contour[0x3006, 0x0050].value[i+1]=contour[0x3006, 0x0050].value[i+1] + meas_params[1]
                contour[0x3006, 0x0050].value[i+2]=contour[0x3006, 0x0050].value[i+2] + meas_params[2]

    except:
        print('no contour data')




    if structname_o != 'None':
        print(dirname,structname_o)
        dataset.save_as(dirname + '/' + structname_o + '.dcm')
























parser = argparse.ArgumentParser()
# parser.add_argument('-s', '--structure', nargs='?', type=argparse.FileType('r'), help='structure file, in DICOM format')
parser.add_argument('structure',type=str,help="Input the structure file")
parser.add_argument("-o", "--output", nargs="?", type=argparse.FileType("w"), help="output structure filename, the file will be located in the same folder as the original, in DICOM format",)
parser.add_argument('-m' ,'--measurement' , nargs=3, metavar=('x', 'y', 'z'),
                        help="Specify the shift in x, y, z in mm", type=float,
                        default=[0,0,0])
args=parser.parse_args()

meas_params=args.measurement



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x distance [mm]')
ax.set_ylabel('y distance [mm]')
ax.set_zlabel('z distance [mm]')


if args.structure:
    structname = args.structure
    dirname = os.path.dirname(structname)
    if args.output:
        structname_o=args.output
        process_struct(structname, meas_params, dirname, structname_o.name, fig)
    else:
        process_struct(structname, meas_params, dirname, 'None', fig)
