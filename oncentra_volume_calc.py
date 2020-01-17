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




    k = 0
    for elem in dataset[0x3006, 0x0020]:
        print(elem[0x3006, 0x0028].value, k)
        k = k + 1



    print("Select the two surfaces to find intersection")
    while True:  # example of infinite loops using try and except to catch only numbers
        line = input("Select the first structure from the list > ")
        try:
            num1 = int(line.lower())    # temporarily since allows any range of numbers
            break
        except ValueError:  # pylint: disable = bare-except
            print("Please enter a valid option:")

    while True:  # example of infinite loops using try and except to catch only numbers
        line = input("Select the second structure from the list > ")
        try:
            num2 = int(line.lower())
            break
        except ValueError:  # pylint: disable = bare-except
            print("Please enter a valid option:")

    struct_intersect_list = [num1,num2]
    struct_intersect_names_list = [dataset[0x3006, 0x0020][num1][0x3006, 0x0028].value,dataset[0x3006, 0x0020][num2][0x3006, 0x0028].value]


    dz = abs(dataset[0x3006, 0x0039][num1][0x3006, 0x0040][2][0x3006, 0x0050][2] - dataset[0x3006, 0x0039][num1][0x3006, 0x0040][1][0x3006, 0x0050][2])
    print('dz=', dz)







    roi_num = []
    roi_color = []

    xs_tot = []
    ys_tot = []
    zs_tot = []
    el_tot = []



    k = 0 #iterator for the number of structures
    for j in struct_intersect_list:
        xs_elem = []
        ys_elem = []
        zs_elem = []
        elem = dataset[0x3006, 0x0039][j]
        roi_color = elem[0x3006, 0x002a].value # this value is the color of the lesion/structure
        hex_color = colors.rgb2hex(np.asarray(roi_color)/255)
        roi_num.append(elem[0x3006, 0x0084].value)
        Area = 0
        try:
            for contour in elem[0x3006, 0x0040]:  #the area between the two surfaces must be calculated for every contour if there are two areas in each of the contours
                xs = []
                ys = []
                zs = []
                for i in range(0, contour[0x3006, 0x0050].VM, 3):
                    xs_elem.append(contour[0x3006, 0x0050][i])
                    ys_elem.append(contour[0x3006, 0x0050][i+1])
                    zs_elem.append(contour[0x3006, 0x0050][i+2])

                    xs_tot.append(contour[0x3006, 0x0050][i])
                    ys_tot.append(contour[0x3006, 0x0050][i+1])
                    zs_tot.append(contour[0x3006, 0x0050][i+2])
                    el_tot.append(k)




                # x = np.array(xs).astype(np.float) #this is the collection of points for every slice
                # y = np.array(ys).astype(np.float)
                # z = np.array(zs).astype(np.float)
                #
                #
                #
                # Area = Area + PolyArea(x, y) * dz
                # print('Slice area = ', PolyArea(x, y), Area)







                # poly = Poly3DCollection(verts, alpha=0.5)
                # poly.set_color(hex_color)
                # poly.set_edgecolor('k')
                # ax.add_collection3d(poly)






            x_elem = np.array(xs_elem).astype(np.float)  # this is the collection of points for every element
            y_elem = np.array(ys_elem).astype(np.float)
            z_elem = np.array(zs_elem).astype(np.float)





            # points_total = np.stack((x_elem, y_elem, z_elem), axis=1)
            if k == 0: #if structure 0
                elem_0 = np.stack((x_elem, y_elem, z_elem), axis=1)
                hull = ss.ConvexHull(elem_0)
                print('hull0_stats(volume,area)',hull.volume,hull.area)
                sphericity_0=(np.pi**(1/3)*(6*hull.volume)**(2/3))/(hull.area)
                print('sphericity_0=',sphericity_0)


                points = go.Scatter3d(mode='markers',
                                   name='',
                                   x=x_elem,
                                   y=y_elem,
                                   z=z_elem,
                                   marker=dict(size=2,color='red')
                                   )

                # simplexes = go.Mesh3d(alphahull=2.0,
                #                    name='',
                #                    x=x_elem,
                #                    y=y_elem,
                #                    z=z_elem,
                #                    color='red',  # set the color of simplexes in alpha shape
                #                    opacity=0.15
                #                    )

                # fig = go.Figure(data=[points,simplexes])
                fig = go.Figure(data=[points])
                # fig.show()







            elif k == 1: #if structure 1
                elem_1 = np.stack((x_elem, y_elem, z_elem), axis=1)
                hull = ss.ConvexHull(elem_1)
                print('hull1_stats(volume,area)',hull.volume, hull.area)
                sphericity_1=(np.pi**(1/3)*(6*hull.volume)**(2/3))/(hull.area)
                print('sphericity_1=',sphericity_1)

                points = go.Scatter3d(mode='markers',
                                   name='',
                                   x=x_elem,
                                   y=y_elem,
                                   z=z_elem,
                                   marker=dict(size=2,color='red')
                                   )

                # simplexes = go.Mesh3d(alphahull=2.0,
                #                    name='',
                #                    x=x_elem,
                #                    y=y_elem,
                #                    z=z_elem,
                #                    color='red',  # set the color of simplexes in alpha shape
                #                    opacity=0.15
                #                    )

                # fig = go.Figure(data=[points,simplexes])
                fig = go.Figure(data=[points])
                # fig.show()



        except:
            print('no contour data')



        k = k + 1

    #the section below is for more accurate calculations of the volume
    # exit(0)



    volume_intersection = 0
    volume_0 = 0
    volume_1 = 0

    for i in range(0, np.shape(elem_0)[0] - 1):
        if elem_0[i, 2] != elem_0[i+1, 2]:
            elem_0_select = elem_0[elem_0[:, 2] == elem_0[i, 2]]
            poly0 = geometry.Polygon(elem_0_select[:, 0:2])
            volume_0 = volume_0 + poly0.area * dz

    #we also need to include the last layer/shape for a more accurate calculation
    elem_0_select = elem_0[elem_0[:, 2] == elem_0[np.shape(elem_0)[0]-1, 2]]
    poly0 = geometry.Polygon(elem_0_select[:, 0:2])
    volume_0 = volume_0 + poly0.area * dz




    for i in range(0, np.shape(elem_1)[0] - 1):
        if elem_1[i, 2] != elem_1[i+1, 2]:
            elem_1_select = elem_1[elem_1[:, 2] == elem_1[i, 2]]
            poly1 = geometry.Polygon(elem_1_select[:, 0:2])
            volume_1 = volume_1 + poly1.area * dz

    # we also need to include the last layer/shape for a more accurate calculation
    elem_1_select = elem_1[elem_1[:, 2] == elem_1[np.shape(elem_1)[0]-1, 2]]
    poly1 = geometry.Polygon(elem_1_select[:, 0:2])
    volume_1 = volume_1 + poly1.area * dz



    for i in range(0, np.shape(elem_0)[0]-1):
        if elem_0[i, 2] != elem_0[i+1, 2]:
            elem_0_select = elem_0[elem_0[:, 2] == elem_0[i, 2]]
            elem_1_select = elem_1[elem_1[:, 2] == elem_0[i, 2]]
            if len(elem_1_select) == 0 or len(elem_0_select) == 0:
                continue
            else:
                poly0 = geometry.Polygon(elem_0_select[:, 0:2])
                poly1 = geometry.Polygon(elem_1_select[:, 0:2])
                if poly0.intersects(poly1) == True:
                    poly_intersect = poly0.intersection(poly1)
                    if type(poly_intersect) == geometry.multipolygon.MultiPolygon:
                        for poly in list(poly_intersect):
                            volume_intersection = volume_intersection + poly.area * dz
                    elif type(poly_intersect) == geometry.polygon.Polygon:
                        volume_intersection = volume_intersection + poly_intersect.area * dz








    print('volume_intersection=', volume_intersection, 'mm^3')
    print('volume_0', struct_intersect_names_list[0], '=', volume_0, 'mm^3')
    print('volume_1', struct_intersect_names_list[1], '=', volume_1, 'mm^3')
    print('Ratio (volume_1/volume_0) (lesion/prostate)=', volume_1/volume_0)






    exit(0)















    x_total = np.array(xs_tot).astype(np.float)  # this is the total collection of points
    y_total = np.array(ys_tot).astype(np.float)
    z_total = np.array(zs_tot).astype(np.float)
    el_total = np.array(el_tot).astype(np.float)




    ax.set_xlim3d(np.min(xs_tot), np.max(xs_tot))
    ax.set_ylim3d(np.min(ys_tot), np.max(ys_tot))
    ax.set_zlim3d(np.min(zs_tot), np.max(zs_tot))
    plt.show()


















parser = argparse.ArgumentParser()
parser.add_argument('-s', '--structure', nargs='?', type=argparse.FileType('r'), help='structure file, in DICOM format')
args=parser.parse_args()



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x distance [mm]')
ax.set_ylabel('y distance [mm]')
ax.set_zlabel('z distance [mm]')


if args.structure:
    structname = args.structure
    process_struct(structname.name,fig)
