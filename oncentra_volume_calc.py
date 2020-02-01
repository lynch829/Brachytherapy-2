



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










def process_struct(filename, fig):
    print('Starting struct calculation')
    dataset = pydicom.dcmread(filename)




    roi_num = []
    roi_color = []

    xs_tot = []
    ys_tot = []
    zs_tot = []
    el_tot = []

    k=0
    for ROI_seq in dataset[0x3006, 0x0020]:
        print(ROI_seq[0x3006, 0x0026],k)
        k=k+1

    #iterator for the number of structures
    k=0
    for elem in dataset[0x3006, 0x0039]:
        dz = abs(dataset[0x3006, 0x0039][k][0x3006, 0x0040][2][0x3006, 0x0050][2] - dataset[0x3006, 0x0039][k][0x3006, 0x0040][1][0x3006, 0x0050][2])
        # print('dz',k,'=', dz)

        xs_elem = []
        ys_elem = []
        zs_elem = []
        roi_color = elem[0x3006, 0x002a].value # this value is the color of the lesion/structure
        hex_color = colors.rgb2hex(np.asarray(roi_color)/255)
        roi_num.append(elem[0x3006, 0x0084].value)
        try:
            for contour in elem[0x3006, 0x0040]:  #the area between the two surfaces must be calculated for every contour if there are two areas in each of the contours
                for i in range(0, contour[0x3006, 0x0050].VM, 3):
                    xs_elem.append(contour[0x3006, 0x0050][i])
                    ys_elem.append(contour[0x3006, 0x0050][i+1])
                    zs_elem.append(contour[0x3006, 0x0050][i+2])

                    xs_tot.append(contour[0x3006, 0x0050][i])
                    ys_tot.append(contour[0x3006, 0x0050][i+1])
                    zs_tot.append(contour[0x3006, 0x0050][i+2])


            x_elem = np.array(xs_elem).astype(np.float)  # this is the collection of points for every element
            y_elem = np.array(ys_elem).astype(np.float)
            z_elem = np.array(zs_elem).astype(np.float)

            structure = np.stack((x_elem, y_elem, z_elem), axis=1)
            # print(structure,k)

            # hull = ss.ConvexHull(structure)
            # print('hull0_stats(volume,area)', hull.volume, hull.area)

            volume_0=0

            for i in range(0, np.shape(structure)[0] - 1):
                if structure[i, 2] != structure[i+1, 2]:
                    structure_select = structure[structure[:, 2] == structure[i, 2]]
                    poly0 = geometry.Polygon(structure_select[:, 0:2])
                    volume_0 = volume_0 + poly0.area * dz

            #we also need to include the last layer/shape for a more accurate calculation
            structure_select = structure[structure[:, 2] == structure[np.shape(structure)[0]-1, 2]]
            poly0 = geometry.Polygon(structure_select[:, 0:2])
            volume_0 = volume_0 + poly0.area * dz



            print('volume', k, '=', volume_0, 'mm^3')

        except Exception as e:
            # print('An error occurred while calculating the volume of structure',k)
            # print(e)
            hull = ss.ConvexHull(structure)
            print('volume', k, '=', hull.volume, 'mm^3')


        k=k+1

    exit(0)








    # x_total = np.array(xs_tot).astype(np.float)  # this is the total collection of points
    # y_total = np.array(ys_tot).astype(np.float)
    # z_total = np.array(zs_tot).astype(np.float)
    # el_total = np.array(el_tot).astype(np.float)
    #
    #
    #
    #
    # ax.set_xlim3d(np.min(xs_tot), np.max(xs_tot))
    # ax.set_ylim3d(np.min(ys_tot), np.max(ys_tot))
    # ax.set_zlim3d(np.min(zs_tot), np.max(zs_tot))
    # plt.show()


















parser = argparse.ArgumentParser()
#parser.add_argument('-s', '--structure', nargs='?', type=argparse.FileType('r'), help='structure file, in DICOM format')
parser.add_argument('structure',type=str,help="Input the structure file, in DICOM format")
args=parser.parse_args()



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x distance [mm]')
ax.set_ylabel('y distance [mm]')
ax.set_zlabel('z distance [mm]')


if args.structure:
    structname = args.structure
    process_struct(structname,fig)
    #process_struct(structname.name,fig)
