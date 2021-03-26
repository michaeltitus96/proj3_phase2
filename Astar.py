#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import copy
import imutils
import sys

start_x = int(input("Enter starting x-coordinate (5-395): "))       #user inputs the starting and finishing coordinates
start_y = int(input("Enter starting y-coordinate (5-295): "))
goal_x = int(input("Enter finishing x-coordinate (5-395): "))
goal_y = int(input("Enter finishing y-coordinate (5-295): "))
print()
d = int(input("Enter the step distance for each movement (1-10): "))

image = np.ones((801,601,1),np.uint8)*255       #creates blank image

def CoordToString(x,y):
    if x // 10 < 1:        #lists location as a string with 6 integers (x and y coords) (000000 to 800600)
        stringx = '00'
    elif x // 10 < 10:
        stringx = '0'
    else:
        stringx = ''     
    if y // 10 < 1:
        stringy = '00'
    elif y // 10 < 10:
        stringy = '0'
    else:
        stringy = '' 
    return stringx,stringy

start_x = start_x*2
start_y = start_y*2
startx,starty = CoordToString(start_x,start_y) 
start_loc = str(startx+str(int(start_x))+starty+str(int(start_y)))
print(start_loc)

goal_x = goal_x*2
goal_y = goal_y*2
goalx,goaly = CoordToString(goal_x,goal_y) 
goal_loc = str(goalx+str(int(goal_x))+goaly+str(int(goal_y)))
print(goal_loc)

obstacles = []      #lists obstacle points that cannot be traversed

for i in range(0,601):      #left boundary
    x = 0
    y = i
    stringx,stringy = CoordToString(x,y)
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    obstacles.append(location)
      
for i in range(0,801):      #bottom boundary
    x = i
    y = 0
    stringx,stringy = CoordToString(x,y)
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    obstacles.append(location)
    
for i in range(0,601):      #right boundary
    x = 800
    y = i
    stringx,stringy = CoordToString(x,y)
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    obstacles.append(location)
    
for i in range(0,801):      #top boundary
    x = i
    y = 600
    stringx,stringy = CoordToString(x,y)
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    obstacles.append(location)
    
for i in range(110,252):     #obstacle 1: circle
    for j in range(70,212):
        if ((i-180)**2 + (j-140)**2 < 70**2):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y)
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            obstacles.append(location)
        else:
            pass
        
for i in range(70,270):     #obstacle 2: slanted rectangle
    for j in range(216,372):
        if (j > (0.7*i) + (744/5)) and (j < (0.7*i) + (998/5)) and (j > ((-357/250)*i) + (44102/125)) and (j < ((-357/250)*i) + (90088/125)):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y)
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            obstacles.append(location)
        else:
            pass

for i in range(400,462):        #obstacle 3: part 1 of U-shape
    for j in range(460,482):
        if (i > 400) and (i < 462) and (j > 460) and (j < 482):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y)
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            obstacles.append(location)
        else:
            pass

for i in range(400,422):        #obstacle 4: part 2 of U-shape
    for j in range(480,542):
        if (i > 400) and (i < 422) and (j > 480) and (j < 542):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y) 
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            obstacles.append(location)
        else:
            pass

for i in range(400,462):        #obstalce 5: part 3 of U-shape
    for j in range(540,562):
        if (i > 400) and (i < 462) and (j > 540) and (j < 562):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y)
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            obstacles.append(location)
        else:
            pass
        
for i in range(372,614):        #obstacle 6: ellipse
    for j in range(230,352):
        if ((((i-492)**2)/14400) + (((j-290)**2)/3600) < 1):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y)
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            obstacles.append(location)
        else:
            pass
    
clearance = []

for i in range(0,801):        #bottom clearance
    for j in range(0,11):
        if (i > 0) and (i < 801) and (j > 0) and (j < 11):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y)
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            clearance.append(location)
        else:
            pass
        
for i in range(0,11):        #left clearance
    for j in range(0,601):
        if (i > 0) and (i < 11) and (j > 0) and (j < 601):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y)
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            clearance.append(location)
        else:
            pass
        
for i in range(791,801):        #right clearance
    for j in range(0,601):
        if (i > 791) and (i < 801) and (j > 0) and (j < 601):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y)
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            clearance.append(location)
        else:
            pass
        
for i in range(0,801):        #top clearance
    for j in range(591,601):
        if (i > 0) and (i < 801) and (j > 591) and (j < 601):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y)
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            clearance.append(location)
        else:
            pass
        
for i in range(100,262):     #clearance 1: circle
    for j in range(60,222):
        if ((i-180)**2 + (j-140)**2 < 80**2):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y) 
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            clearance.append(location)
        else:
            pass

for i in range(50,290):     #clearance 2: slanted rectangle
    for j in range(196,392):
        if (j > (0.7*i) + (694/5)) and (j < (0.7*i) + (1048/5)) and (j > ((-357/250)*i) + (42352/125)) and (j < ((-357/250)*i) + (91838/125)):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y) 
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            clearance.append(location)
        else:
            pass

for i in range(390,472):        #clearance 3: part 1 of U-shape
    for j in range(450,492):
        if (i > 390) and (i < 472) and (j > 450) and (j < 492):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y) 
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            clearance.append(location)
        else:
            pass

for i in range(390,432):        #clearance 4: part 2 of U-shape
    for j in range(470,552):
        if (i > 390) and (i < 432) and (j > 470) and (j < 552):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y) 
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            clearance.append(location)
        else:
            pass

for i in range(390,472):        #clearance 5: part 3 of U-shape
    for j in range(530,572):
        if (i > 390) and (i < 472) and (j > 530) and (j < 572):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y) 
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            clearance.append(location)
        else:
            pass

for i in range(362,624):        #clearance 6: ellipse
    for j in range(220,362):
        if ((((i-492)**2)/16900) + (((j-290)**2)/4900) < 1):
            x = i
            y = j
            stringx,stringy = CoordToString(x,y) 
            location = str(stringx+str(int(x))+stringy+str(int(y)))
            clearance.append(location)
        else:
            pass
   
if start_loc in obstacles:
    print("Starting coordinates are in an obstalce. Please try again.")
    sys.exit()
   
if start_loc in clearance:
    print("Starting coordinates are too close to an obstacle/boundary. Please try again.")  
    sys.exit()

if goal_loc in obstacles:
    print("Goal coordinates are in an obstalce. Please try again.")
    sys.exit()
   
if goal_loc in clearance:
    print("Goal coordinates are too close to an obstacle/boundary. Please try again.")  
    sys.exit()

if start_x > 800 or start_x < 0 or start_y > 600 or start_y < 0:
    print("Starting coordinates are outside boundaries. Please try again.")
    sys.exit()
    
if goal_x > 800 or goal_x < 0 or goal_y > 600 or goal_y < 0:
    print("Goal coordinates are outside boundaries. Please try again.")
    sys.exit()
    
for i in clearance:     #displays obstacles as black pixels on image map
    locx = int(i[0:3])
    locy = int(i[3:])
    image[locx,locy] = 127    
   
for i in obstacles:     #displays obstacles as black pixels on image map
    locx = int(i[0:3])
    locy = int(i[3:])
    image[locx,locy] = 0

rotated = imutils.rotate_bound(image,-90)       #rotates image to match rubric
cv2.imshow('image',rotated)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)  

