'''
Name: csv_to_xml_dir.py
Created by: Roberto Rodriguez
Date Created: 4/24/2020
Last Updated: 4/25/2020
Purpose: Create PascvalVOC annotations from ImageJ auto-detection
'''

# Libraries
import csv
import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import glob

# Ask for path to image (assume CSV and XML will match)
root = tk.Tk()
path_to_directory = filedialog.askdirectory(initialdir = "/", title = "Select Directory Containing Images")

# Ask for object name
object = simpledialog.askstring("Object Name", "Enter name for the object annotation:", parent = root)
#object = 'grasshopper'


for filename in glob.glob(path_to_directory+"/*.jpg"):
    # Paths to files
    path_to_img = filename
    print(filename)
    path_to_csv = filename[:-4]+'.csv'
    path_to_xml = filename[:-4]+'.xml'
    path_to_print = filename.replace('/', '\\')

    # Open and read CSV
    f=open(path_to_csv)
    csv_f = csv.reader(f)

    # Open and read image information
    img = Image.open(path_to_img)
    width, height = img.size
    depth = len(img.getbands())

    # Create annotation header
    annotations = open(path_to_xml, 'w')

    print('<annotation>', file = annotations)
    print('\t'+'<folder>'+os.path.basename(os.path.dirname(path_to_img))+'</folder>', file = annotations)
    print('\t'+'<filename>'+os.path.basename(path_to_img)+'</filename>', file = annotations)
    print('\t'+'<path>'+path_to_print+'</path>', file = annotations)
    print('\t'+'<source>', file = annotations)
    print('\t'+'\t'+'<database>Unknown</database>', file = annotations)
    print('\t'+'</source>', file = annotations)
    print('\t'+'<size>', file = annotations)
    print('\t'+'\t'+'<width>'+str(width)+'</width>', file = annotations)
    print('\t'+'\t'+'<height>'+str(height)+'</height>', file = annotations)
    print('\t'+'\t'+'<depth>'+str(depth)+'</depth>', file = annotations)
    print('\t'+'</size>', file = annotations)
    print('\t'+'<segmented>0</segmented>', file = annotations)

    # Convert CSV bounding boxes to PascalVOC
    for row in csv_f:
        if row[1].isdigit():
            xmin = int(row[1])
            ymin = int(row[2])
            xmax = xmin + int(row[3])
            ymax = ymin + int(row[4])
            print('\t'+'<object>', file = annotations)
            print('\t'+'\t'+'<name>'+object+'</name>', file = annotations)
            print('\t'+'\t'+'<pose>Unspecified</pose>', file = annotations)
            print('\t'+'\t'+'<truncated>0</truncated>', file = annotations)
            print('\t'+'\t'+'<difficult>0</difficult>', file = annotations)
            print('\t'+'\t'+'<bndbox>', file = annotations)
            print('\t'+'\t'+'\t'+'<xmin>'+str(xmin)+'</xmin>', file = annotations)
            print('\t'+'\t'+'\t'+'<ymin>'+str(ymin)+'</ymin>', file = annotations)
            print('\t'+'\t'+'\t'+'<xmax>'+str(xmax)+'</xmax>', file = annotations)
            print('\t'+'\t'+'\t'+'<ymax>'+str(ymax)+'</ymax>', file = annotations)
            print('\t'+'\t'+'</bndbox>', file = annotations)
            print('\t'+'</object>', file = annotations)

    print('</annotation>', file = annotations)
    annotations.close()

