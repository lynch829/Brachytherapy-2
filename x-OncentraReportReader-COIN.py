###########################################################################################
#
#   Script name: x-OncentraReportReader
#
#   Description: Tool for processing of Oncentra report files
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
import re
from astropy.io import ascii
import pandas as pd
from openpyxl import Workbook, cell, load_workbook
from math import *
import scipy.integrate as integrate
from scipy.signal import find_peaks, peak_prominences, peak_widths
import PyPDF2







def process_folder(dirname):
    COIN=[]
    filename_set = []
    # for subdir, dirs, files in os.walk(dirname):
    with os.scandir(dirname) as entries:
        for filename in entries:
            if filename.is_file():
                if os.path.splitext(filename.name)[1]=='.pdf':
                    print(filename.name)
                    filename_set.append(filename.name)
                    pdfFileObj = open(dirname+filename.name,'rb')
                    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                    print('Number of pages',pdfReader.numPages)
                    for i in range(0,pdfReader.numPages):
                        pageObj = pdfReader.getPage(i)
                        page_text=re.split(':|\n|%', pageObj.extractText())
                        try:
                            COIN.append(page_text[page_text.index('COIN')+1])
                        except:
                            nextPageObj = pdfReader.getPage(i + 1)
                            next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                            COIN.append(next_page_text[next_page_text.index('COIN') + 1])





    Data_dict = {'filename': filename_set,'COIN': COIN}
    df = pd.DataFrame(Data_dict,columns=['filename','COIN'])


    df.to_excel('output-COIN.xlsx',sheet_name='Sheet1')






try:
    dirname = str(sys.argv[1])
    print(dirname)
except:
    print('Please enter a valid filename')
    print("Use the following command to run this script")
    print("python test_pydicom3D.py \"[dirname]\"")


try:
    lesion = str(sys.argv[2])
    print(lesion)
except:
    print('Please enter a valid lesion name')
    print("Use the following command to run this script")
    print("python test_pydicom3D.py \"[dirname]\"")

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



process_folder(dirname,)
