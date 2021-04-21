# Python-based-AFM-image-analyzer
# Contains Python algorithms for making Atomic Force Microscopic image analysis easier 
# Refer the user manual and the user article uploaded in the repository 
# email me at nsaini3012@gmail.com if you go through any issue to run this application 
#
# Description
# There are three python tools in this application ( slider.py, brightest_point_nm.py, height_finder.py)
# slider.py - this will help you create a mask, and overlap of mask and original AFM image ( try with sample_image.png provided in the repository )
# brightest_point_nm.py - this will help you in in processing mask, overlap of mask and original AFM image and the ASCII XYZ file you will get from the AFM machine (NOTE-ASCII XYZ file is required for this application, if you dont know how to get ASCII XYZ file for your AFM image please refer user manual). After processing this tool will give you centre coorinates of each particle in image (a coordinate CSV file will be created), particle count and radius of the particles.
# height_finder.py - this will process your ASCII XYZ file and overlap of mask + original AFM image, and will provide you with histogram with height destribution. It will give you two excel files, one with heights with the background and other excel file will have heights without background (actual heights ). 

# NOTES - this application works really well on AFM images of nanostructures which are symmetrical and nicely distributed over the surface with homogenous seperation. 
