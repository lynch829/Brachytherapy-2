###########################################################################################
#
#   Script name: Oncentra_DicomTag
#
#   Description: Tool for viewing Dicom tags
#
#   Example usage: python Oncentra_DicomTag "/file/"
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








def process_dicom(filename):
    dataset = pydicom.dcmread(filename)
    print(dataset)
    exit(0)


try:
    filename = str(sys.argv[1])
    print(filename)
except:
    print('Please enter a valid filename')
    print("Use the following command to run this script")
    print("python xx-Oncentra.py \"[structures dicom]\" \"[plan dicom]\"")


process_dicom(filename)
