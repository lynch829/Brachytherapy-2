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
    CTV_V100 = []
    CTV_V150=[]
    CTV_V200 = []
    CTV_D90 = []
    CTV_V90 = []
    U_D10 = []
    U_V100 = []
    R_V80 = []
    Dmean_3mm =[]
    Dmean_5mm = []
    Dmean_7mm = []
    Dmean_9mm = []
    D90_3mm =[]
    D90_5mm = []
    D90_7mm = []
    D90_9mm = []
    V100_3mm = []
    V100_5mm = []
    V100_7mm = []
    V100_9mm = []
    V120_3mm = []
    V120_5mm = []
    V120_7mm = []
    V120_9mm = []
    V125_3mm = []
    V125_5mm = []
    V125_7mm = []
    V125_9mm = []
    V150_3mm =[]
    V150_5mm = []
    V150_7mm = []
    V150_9mm = []
    V175_3mm = []
    V175_5mm = []
    V175_7mm = []
    V175_9mm = []
    V200_3mm =[]
    V200_5mm = []
    V200_7mm = []
    V200_9mm = []
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
                        for j in range(0,len(page_text)):
                            if page_text[j]=='CTV1 (CTV1)':
                                try:
                                    CTV_D90.append(page_text[j+page_text[j:].index('D90')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i + 1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    CTV_D90.append(next_page_text[next_page_text.index('D90') + 1])
                                try:
                                    CTV_V90.append(page_text[j+page_text[j:].index('V90')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i + 1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    CTV_V90.append(next_page_text[next_page_text.index('V90') + 1])
                                try:
                                    CTV_V100.append(page_text[j+page_text[j:].index('V100')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i + 1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    CTV_V100.append(next_page_text[next_page_text.index('V100') + 1])
                                try:
                                    CTV_V150.append(page_text[j+page_text[j:].index('V150')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i + 1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    CTV_V150.append(next_page_text[next_page_text.index('V150') + 1])
                                try:
                                    CTV_V200.append(page_text[j + page_text[j:].index('V200') + 1])
                                except:
                                    nextPageObj = pdfReader.getPage(i + 1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    CTV_V200.append(next_page_text[next_page_text.index('V200') + 1])

                            if page_text[j] == 'Urethra (OAR)':
                                try:
                                    U_D10.append(page_text[j+page_text[j:].index('D10')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i + 1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    U_D10.append(next_page_text[next_page_text.index('D10') + 1])


                            if page_text[j] == 'Urethra (OAR)':
                                try:
                                    U_V100.append(page_text[j+page_text[j:].index('V100')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i + 1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    U_V100.append(next_page_text[next_page_text.index('V100') + 1])

                            if page_text[j] == 'V80':
                                try:
                                    R_V80.append(page_text[j+page_text[j:].index('V80')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i + 1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    R_V80.append(next_page_text[next_page_text.index('V80') + 1])

                            if page_text[j] == 'LI-3mmD-3mmd (CTV3)':
                                try:
                                    Dmean_3mm.append(page_text[j+page_text[j:].index('Dmean')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    Dmean_3mm.append(next_page_text[next_page_text.index('Dmean')+1])
                            if page_text[j] == 'LI-5mmD-5mmd (CTV3)':
                                try:
                                    Dmean_5mm.append(page_text[j+page_text[j:].index('Dmean')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    Dmean_5mm.append(next_page_text[next_page_text.index('Dmean')+1])
                            if page_text[j] == 'LI-7mmD-7mmd (CTV3)':
                                try:
                                    Dmean_7mm.append(page_text[j+page_text[j:].index('Dmean')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    Dmean_7mm.append(next_page_text[next_page_text.index('Dmean')+1])
                            if page_text[j] == 'LI-9mmD-9mmd (CTV3)':
                                try:
                                    Dmean_9mm.append(page_text[j+page_text[j:].index('Dmean')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    Dmean_9mm.append(next_page_text[next_page_text.index('Dmean')+1])

                            if page_text[j] == 'LI-3mmD-3mmd (CTV3)':
                                try:
                                    D90_3mm.append(page_text[j+page_text[j:].index('D90')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    D90_3mm.append(next_page_text[next_page_text.index('D90')+1])
                            if page_text[j] == 'LI-5mmD-5mmd (CTV3)':
                                try:
                                    D90_5mm.append(page_text[j+page_text[j:].index('D90')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    D90_5mm.append(next_page_text[next_page_text.index('D90')+1])
                            if page_text[j] == 'LI-7mmD-7mmd (CTV3)':
                                try:
                                    D90_7mm.append(page_text[j+page_text[j:].index('D90')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    D90_7mm.append(next_page_text[next_page_text.index('D90')+1])
                            if page_text[j] == 'LI-9mmD-9mmd (CTV3)':
                                try:
                                    D90_9mm.append(page_text[j+page_text[j:].index('D90')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    D90_9mm.append(next_page_text[next_page_text.index('D90')+1])
                                    
                                    
                                    
                            if page_text[j] == 'LI-3mmD-3mmd (CTV3)':
                                try:
                                    V150_3mm.append(page_text[j+page_text[j:].index('V150')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V150_3mm.append(next_page_text[next_page_text.index('V150')+1])
                                try:
                                    V100_3mm.append(page_text[j+page_text[j:].index('V100')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V100_3mm.append(next_page_text[next_page_text.index('V100')+1])
                                try:
                                    V125_3mm.append(page_text[j+page_text[j:].index('V125')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V125_3mm.append(next_page_text[next_page_text.index('V125')+1])
                                try:
                                    V175_3mm.append(page_text[j+page_text[j:].index('V175')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V175_3mm.append(next_page_text[next_page_text.index('V175')+1])



                            if page_text[j] == 'LI-5mmD-5mmd (CTV3)':
                                try:
                                    V150_5mm.append(page_text[j+page_text[j:].index('V150')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V150_5mm.append(next_page_text[next_page_text.index('V150')+1])
                                try:
                                    V100_5mm.append(page_text[j+page_text[j:].index('V100')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V100_5mm.append(next_page_text[next_page_text.index('V100')+1])
                                try:
                                    V125_5mm.append(page_text[j+page_text[j:].index('V125')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V125_5mm.append(next_page_text[next_page_text.index('V125')+1])
                                try:
                                    V175_5mm.append(page_text[j+page_text[j:].index('V175')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V175_5mm.append(next_page_text[next_page_text.index('V175')+1])
                                    
                                    
                                    
                            if page_text[j] == 'LI-7mmD-7mmd (CTV3)':
                                try:
                                    V150_7mm.append(page_text[j+page_text[j:].index('V150')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V150_7mm.append(next_page_text[next_page_text.index('V150')+1])
                                try:
                                    V100_7mm.append(page_text[j+page_text[j:].index('V100')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V100_7mm.append(next_page_text[next_page_text.index('V100')+1])
                                try:
                                    V125_7mm.append(page_text[j+page_text[j:].index('V125')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V125_7mm.append(next_page_text[next_page_text.index('V125')+1])
                                try:
                                    V175_7mm.append(page_text[j+page_text[j:].index('V175')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V175_7mm.append(next_page_text[next_page_text.index('V175')+1])
                                    
                                    
                                    
                            if page_text[j] == 'LI-9mmD-9mmd (CTV3)':
                                try:
                                    V150_9mm.append(page_text[j+page_text[j:].index('V150')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V150_9mm.append(next_page_text[next_page_text.index('V150')+1])
                                try:
                                    V100_9mm.append(page_text[j+page_text[j:].index('V100')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V100_9mm.append(next_page_text[next_page_text.index('V100')+1])
                                try:
                                    V125_9mm.append(page_text[j+page_text[j:].index('V125')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V125_9mm.append(next_page_text[next_page_text.index('V125')+1])
                                try:
                                    V175_9mm.append(page_text[j+page_text[j:].index('V175')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V175_9mm.append(next_page_text[next_page_text.index('V175')+1])

                                    


                                    
                            if page_text[j] == 'LI-3mmD-3mmd (CTV3)':
                                try:
                                    V200_3mm.append(page_text[j+page_text[j:].index('V200')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V200_3mm.append(next_page_text[next_page_text.index('V200')+1])
                            if page_text[j] == 'LI-5mmD-5mmd (CTV3)':
                                try:
                                    V200_5mm.append(page_text[j+page_text[j:].index('V200')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V200_5mm.append(next_page_text[next_page_text.index('V200')+1])
                            if page_text[j] == 'LI-7mmD-7mmd (CTV3)':
                                try:
                                    V200_7mm.append(page_text[j+page_text[j:].index('V200')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V200_7mm.append(next_page_text[next_page_text.index('V200')+1])
                            if page_text[j] == 'LI-9mmD-9mmd (CTV3)':
                                try:
                                    V200_9mm.append(page_text[j+page_text[j:].index('V200')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V200_9mm.append(next_page_text[next_page_text.index('V200')+1])
                                    
                                    
                                    
                                    
                            if page_text[j] == 'LI-3mmD-3mmd (CTV3)':
                                try:
                                    V120_3mm.append(page_text[j+page_text[j:].index('V120')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V120_3mm.append(next_page_text[next_page_text.index('V120')+1])
                            if page_text[j] == 'LI-5mmD-5mmd (CTV3)':
                                try:
                                    V120_5mm.append(page_text[j+page_text[j:].index('V120')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V120_5mm.append(next_page_text[next_page_text.index('V120')+1])
                            if page_text[j] == 'LI-7mmD-7mmd (CTV3)':
                                try:
                                    V120_7mm.append(page_text[j+page_text[j:].index('V120')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V120_7mm.append(next_page_text[next_page_text.index('V120')+1])
                            if page_text[j] == 'LI-9mmD-9mmd (CTV3)':
                                try:
                                    V120_9mm.append(page_text[j+page_text[j:].index('V120')+1])
                                except:
                                    nextPageObj = pdfReader.getPage(i+1)
                                    next_page_text = re.split(':|\n|%', nextPageObj.extractText())
                                    V120_9mm.append(next_page_text[next_page_text.index('V120')+1])




    #Data_dict = {'filename': filename_set,'CTV_V100': CTV_V100,'CTV_V90': CTV_V90,'CTV_V150': CTV_V150,'CTV_V200': CTV_V200, 'CTV_D90': CTV_D90, 'U_D10': U_D10, 'U_V100': U_V100, 'R_V80': R_V80, 'Dmean_3mm':Dmean_3mm, 'Dmean_5mm':Dmean_5mm, 'Dmean_7mm':Dmean_7mm, 'Dmean_9mm':Dmean_9mm, 'D90_3mm':D90_3mm, 'D90_5mm':D90_5mm, 'D90_7mm':D90_7mm, 'D90_9mm':D90_9mm, 'V175_3mm':V175_3mm, 'V175_5mm':V175_5mm, 'V175_7mm':V175_7mm, 'V175_9mm':V175_9mm, 'V125_3mm':V125_3mm, 'V125_5mm':V125_5mm, 'V125_7mm':V125_7mm, 'V125_9mm':V125_9mm, 'V150_3mm':V150_3mm, 'V150_5mm':V150_5mm, 'V150_7mm':V150_7mm, 'V150_9mm':V150_9mm, 'V200_3mm':V200_3mm, 'V200_5mm':V200_5mm, 'V200_7mm':V200_7mm, 'V200_9mm':V200_9mm, 'V120_3mm':V120_3mm, 'V120_5mm':V120_5mm, 'V120_7mm':V120_7mm, 'V120_9mm':V120_9mm}
    Data_dict = {'filename': filename_set,'CTV_V100': CTV_V100,'CTV_V90': CTV_V90,'CTV_V150': CTV_V150,'CTV_V200': CTV_V200, 'CTV_D90': CTV_D90, 'U_D10': U_D10, 'U_V100': U_V100, 'R_V80': R_V80}

    for k, v in Data_dict.items():
        print(k,v)


    #df = pd.DataFrame(Data_dict,columns=['filename','CTV_V100','CTV_V90','CTV_V150','CTV_V200','CTV_D90','U_D10','U_V100','R_V80','Dmean_3mm','Dmean_5mm','Dmean_7mm','Dmean_9mm','D90_3mm','D90_5mm','D90_7mm','D90_9mm', 'V175_3mm','V175_5mm','V175_7mm','V175_9mm','V125_3mm','V125_5mm','V125_7mm','V125_9mm', 'V150_3mm','V150_5mm','V150_7mm','V150_9mm','V200_3mm','V200_5mm','V200_7mm','V200_9mm','V120_3mm','V120_5mm','V120_7mm','V120_9mm'])
    df = pd.DataFrame(Data_dict,columns=['filename','CTV_V100','CTV_V90','CTV_V150','CTV_V200','CTV_D90','U_D10','U_V100','R_V80'])


    df.to_excel('output.xlsx',sheet_name='Sheet1')






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
