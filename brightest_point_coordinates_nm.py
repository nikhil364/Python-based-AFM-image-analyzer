#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created program will output three files, file named "coordinates.csv" is the one in nanometers and is always used in dislocate
NOTE - the format of ascii file really matters and if that format changes in future then this program will give problems because it only knows how to read a particular format of ascii file, but nothing to worry, there will only be need to chnage some parts of the
program and it is easily fixable

"""

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as img
import cv2
import seaborn as sns
from scipy import stats
import statistics
import argparse
import cv2
import pylab
from scipy import ndimage
import numpy as np
import imutils
from imutils import contours
from skimage import measure
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", help = "path to the ascii file")
ap.add_argument("-i_bw", "--image_bw", help = "path to the bw_image file")
ap.add_argument("-i_md", "--image_md", help = "path to the bw_image file")


args = vars(ap.parse_args())

# open the acii file

open_file = open((args["file"]), "r")
#open_file = open("/Users/biotechnology/Desktop/CirclePython/z_axis/height_finding/sample2/ascii.txt", "r")

x = []
y = []
z = []

#reading the ascii file


for line in open_file:
    #print(line)
    split = line.split()
    if (len(split) == 3):
       
        x.append(split[0])
        y.append(split[1])
        z.append(split[2])
        
x_copy = x.copy()
y_copy = y.copy()
z_copy = z.copy()        
       
x_x = x.remove(x[0])
y_y = y.remove(y[0])
z_z = z.remove(z[0])


x_int = []
y_int = []
z_int = []



for i in range(len(x)):
    x_int.append(float(x[i]))
    y_int.append(float(y[i]))
    z_int.append(float(z[i]))


# conversion from pixels to measurable scales (nm or um ) ( but finally ouput will be in nanomaters )

        

scale_of_image= max(x_int)

if x_copy[0] == 'X[µm]' :
    scale_of_image_in_nm = scale_of_image * 1000
elif   x_copy[0] == 'X[nm]' :   
    
   scale_of_image_in_nm = scale_of_image

# read black and white mask 

black_white = cv2.imread(args["image_bw"])


# counting number of particles from masked data 
labelarray, particle_count = ndimage.measurements.label(black_white)


print ("Total number of particles is ", particle_count)

print('coordinates (x,y) of the brightest point:')
#print(labelarray)

#masked_data = cv2.bitwise_and(src, src, mask=black_white)
#cv2.imwrite("WSXM_original_maskedData.jpg", masked_data)


#masked_data = cv2.imread('/Users/biotechnology/Desktop/CirclePython/images_munir/masked_data3.png')

# reading the masked data 
masked_data = cv2.imread(args["image_md"])
# find the object from the label array created " labelarray "


# looking at the x axis pixels in masked data image and then converting it to scaleable units 
pixels_in_x_axis = masked_data.shape[0]

conversion_factor = scale_of_image_in_nm/pixels_in_x_axis

objectising_from_label = ndimage.find_objects(labelarray)

# finding the location of each object 

all_particles = []   # all particles are in BGR 

for index in range(len(objectising_from_label)):
    particle = masked_data[objectising_from_label[index]]
    all_particles.append(particle)







imgy = gray_masked_data = cv2.cvtColor(masked_data, cv2.COLOR_BGR2GRAY)


#max_channels = np.amax([np.amax(imgy[:,:,0]), np.amax(imgy[:,:,1]), np.amax(imgy[:,:,2])])


# finding the coordinates of brightest point 


Brightest_point_cordinates_x = []
Brightest_point_cordinates_y = []


for location_index in range(len(objectising_from_label)):
   #print(location_index)
    location = objectising_from_label[location_index]
   #print(location)
    x_axis = location[0]
    x_axis_start = x_axis.start
    x_axis_end = x_axis.stop
    y_axis = location[1]
    y_axis_start = y_axis.start
    y_axis_end = y_axis.stop
        
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray_masked_data[x_axis.start:x_axis.stop, y_axis_start:y_axis_end  ] )
   # print(maxLoc)
   # print(maxVal)
    print(y_axis_start+maxLoc[0], x_axis_start+maxLoc[1])
    Brightest_point_cordinates_x.append(y_axis_start+maxLoc[0])
    Brightest_point_cordinates_y.append( x_axis_start+maxLoc[1])
    cv2.circle(masked_data, ( y_axis_start+maxLoc[0], x_axis_start+maxLoc[1]), 0, (255, 0, 0), 2) 
 
#cv2.imwrite("/Users/biotechnology/Desktop/CirclePython/highest_peak.jpg", masked_data)


# adding brightest poits on the image with approximate circle centre 
"""
approx_circle_centre = cv2.imread("/Users/biotechnology/Desktop/CirclePython/centre_approx_circle copy.jpg")

for number in range(len(Brightest_point_cordinates_x)):
    x_cordinate = Brightest_point_cordinates_x[number]
    y_cordinate = Brightest_point_cordinates_y[number]
    cv2.circle( approx_circle_centre, (x_cordinate, y_cordinate), 0, (255, 0, 0), 0)
    
cv2.imwrite('/Users/biotechnology/Desktop/CirclePython/both_highestPeak_approxCircle.jpg', approx_circle_centre)
"""


# write in the file of coordinates in pixels 
with open('x_cordinates.txt', 'w' ) as f:
  for n in range(len(Brightest_point_cordinates_x)):
    x_cordinate = Brightest_point_cordinates_x[n]
    f.writelines(str(x_cordinate)) 

with open('y_cordinates.txt', 'w' ) as f:
  for n in range(len(Brightest_point_cordinates_y)):
    y_cordinate = Brightest_point_cordinates_y[n]
    f.writelines(str(y_cordinate)) 
# writing the coordinates.csv in nanometers scale and is used in dislocate 

import csv

with open('coordinates.csv', 'w', newline='') as file:
    
        writer = csv.writer(file)
        writer.writerow(['x', 'y'])

        for n in range(len(Brightest_point_cordinates_x)):
                x_cordinate = Brightest_point_cordinates_x[n]*conversion_factor
                y_cordinate = Brightest_point_cordinates_y[n]*conversion_factor
                writer.writerow([x_cordinate, y_cordinate])
                
                



            



"""
### waste piece 

for location_index in range(len(objectising_from_label)):
   #print(location_index)
    location = objectising_from_label[location_index]
   #print(location)
    x_axis = location[0]
    x_axis_start = x_axis.start
    x_axis_end = x_axis.stop
    y_axis = location[1]
    y_axis_start = y_axis.start
    y_axis_end = y_axis.stop
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray_masked_data[x_axis.start:x_axis.stop, y_axis_start:y_axis_end  ] )
    print(maxLoc)
    print(maxVal)
    #cv2.circle(gray_masked_data, maxLoc, 0, (255, 0, 0), 0) 

    
    



for index in range(len(objectising_from_label)):
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray_masked_data[objectising_from_label[index]])
    cv2.circle(gray_masked_data, maxLoc, 0, (0, 255, 255), 0) 



matched_array = []
for p in range(len(all_particles)):
 templet =  all_particles[p]         #all_particles[0]
 h, w, c  = templet.shape[::] 
 img_gray = cv2.cvtColor(masked_data, cv2.COLOR_BGR2GRAY)
 matched = cv2.matchTemplate(img_gray, templet, cv2.TM_SQDIFF)
 matched_array.append(matched)
 cv2.waitKey(delay=10000)
    






    
    
   
p_0 = all_particles[8]
p_1 = all_particles[1]


all_particles_RGB = []

for BGR_particles in all_particles:
    x = cv2.cvtColor( BGR_particles, cv2.COLOR_BGR2RGB)
    all_particles_RGB.append(x)
    

p_0_BGR = all_particles_RGB[8]
p_1_BGR = all_particles_RGB[1]

    

gray = cv2.cvtColor(p_0, cv2.COLOR_BGR2GRAY)   

(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
cv2.circle(p_0, maxLoc, 0, (255, 0, 0), 0) 


    
#for each_particle in all_particles:
    
   
# using Contours 

#cnts = cv2.startfindContours_Impl(masked_data, cv2.RETR_FLOODFILL, cv2.CHAIN_APPROX_SIMPLE)   
cnts = cv2.findContours(black_white, cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = contours.sort_contours(cnts)[0]
# loop over the contours
for (i, c) in enumerate(cnts):
	# draw the bright spot on the image
	(x, y, w, h) = cv2.boundingRect(c)
	((cX, cY), radius) = cv2.minEnclosingCircle(c)
	cv2.circle(masked_data, (int(cX), int(cY)), 0,
		(0, 0, 255), 0)
   # cv2.circle(masked_data, (int(cX), int(cY)), int(radius), (0, 0, 255), 1)



pylab.imshow(  masked_data)
cv2.waitKey(0)


#for i in labelarray:
    #print(i)

### waste piece 

"""






    
