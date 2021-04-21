

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as img
import cv2
import seaborn as sns
from scipy import stats
import statistics
import argparse

# arguements to access this from terminal

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", help = "path to the ascii file")
ap.add_argument( "-m", "--md_image", help = "path to masked data image")
args = vars(ap.parse_args())


# reading and processing ascii file 

open_file = open((args["file"]), "r")

x = []
y = []
z = []

for line in open_file:
    #print(line)
    split = line.split()
    if (len(split) == 3):
       
        x.append(split[0])
        y.append(split[1])
        z.append(split[2])
       
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

masked_data = cv2.imread(args["md_image"])

# removing the z heights wanted and removing the background from the histogram  

number_of_black_pixels = np.count_nonzero((masked_data == [0, 0, 0]).all(axis = 2))

total_pixels = (len(masked_data))*(len(masked_data[0]))

percent_of_black_pixels = ((number_of_black_pixels / total_pixels))

take_z_height = z_int.copy() 

take_z_height.sort(reverse=False)

total_z = len(z_int)

Zs_to_be_removed = int((percent_of_black_pixels)*(total_z))

z_arranged = take_z_height.copy()



z_arranged_number = []

for r in z_arranged:
    rr = float(r)
    z_arranged_number.append(rr)
    

numbers_wanted  = z_arranged_number[Zs_to_be_removed:(len(z_arranged_number))]




# making histogram

#sns.set_style('darkgrid')
#ttttt = sns.distplot(numbers_wanted, kde=False, axlabel='Z_heights(nm)', norm_hist=False, vertical=False, color=[0,0,0])

#putting the wanted heights in a text file for reference 
float_number_wanted = []
for f in range(len(numbers_wanted)):
    float_number_wanted.append(float(numbers_wanted[f]))
    
average_height = sum(float_number_wanted)/len(float_number_wanted)    

file_wanted_height = open("wanted_heights.txt", 'w') # these are the height with background 

with file_wanted_height as f:
    f.write("heights\n")
    for i in float_number_wanted:
      f.write("{}\n".format(str(i)))
         





# calculating the average surface height ( reverse masking) and removing it from the heights of the histograms

z_arranged_copy = take_z_height.copy()

backgoound_heights = z_arranged_copy[0:Zs_to_be_removed]

backgoound_heights_int = []

for h in backgoound_heights:
    backgoound_heights_int.append(float(h))
    

average_back_height = statistics.mean(backgoound_heights_int)
    
corrected_height = []
for c in float_number_wanted:
    cc = c - int(average_back_height)
    corrected_height.append(cc)

# making corrected histogram with the applied reverse mask and removed background heights

average_corrected_height = statistics.mean(corrected_height)
sns.set_style('darkgrid')
tttyt = sns.distplot(corrected_height, kde=False, axlabel='Z_heights(nm)', norm_hist=False, vertical=False, color=[0,1,0])


# this file created now will contain the actual heights associated with nanopaticles only 

file_wanted_height_corrected = open("wanted_heights_corrected.txt", 'w') # these are the corrected heights, without background

with file_wanted_height_corrected as f:
    f.write("heights\n")
    for i in corrected_height:
      f.write("{}\n".format(str(i)))
         


plt.show()                             
    


