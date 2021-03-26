#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import copy
import imutils
import sys
import math

start_x = int(input("Enter starting x-coordinate (6-395): "))       #user inputs the starting and finishing coordinates
start_y = int(input("Enter starting y-coordinate (6-295): "))
goal_x = int(input("Enter finishing x-coordinate (6-395): "))
goal_y = int(input("Enter finishing y-coordinate (6-295): "))
print()
d = int(input("Enter the step distance for each movement (1-10): "))

image = np.ones((801,601,1),np.uint8)*255     #creates blank image

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

goal_x = goal_x*2
goal_y = goal_y*2
goalx,goaly = CoordToString(goal_x,goal_y) 
goal_loc = str(goalx+str(int(goal_x))+goaly+str(int(goal_y)))

d = d*2
d1 = copy.deepcopy(d)

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
    print("Starting coordinates are in an obstacle. Please try again.")
    sys.exit()
   
if start_loc in clearance:
    print("Starting coordinates are too close to an obstacle/boundary. Please try again.")  
    sys.exit()

if goal_loc in obstacles:
    print("Goal coordinates are in an obstacle. Please try again.")
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
    
if d > 20 or d < 2:
    print("Invalid step distance entered. Please try again.")
    sys.exit()

def checkGoal(x,y):
    if (goal_x - 3 <= x <= goal_x + 3) and (goal_y - 3 <= y <= goal_y + 3):
        return True
    else:
        return False

travelled = {start_loc : [0,'I']}
current_x = copy.deepcopy(start_x)
current_y = copy.deepcopy(start_y)
current_p = travelled[start_loc][1]
current_cost = travelled[start_loc][0]

locations = [start_loc]

def move00(x,y,cost,p):    
    p = p + 'A'
    xmap = copy.deepcopy(x)
    ymap = copy.deepcopy(y)
    x = x + (d*math.cos(math.radians(0)))
    y = y + (d*math.sin(math.radians(0)))
    ctg = math.sqrt(((goal_x-x)**2)+((goal_y-y)**2))
    x = round(x)
    y = round(y)
    cost = ctg + ((len(p)-1)*d1)
    stringx,stringy = CoordToString(x,y) 
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    if (location not in locations) and (location not in travelled) and (location not in clearance) and x > 0 and x < 800 and y > 0 and y < 600:
        cv2.arrowedLine(image, (ymap,xmap), (y,x), (0, 255, 0), 1)
        update = {location : [cost,p]}
        travelled.update(update)
        for i in range(x-3,x+3):
            for j in range(y-3,y+3):
                stringx,stringy = CoordToString(i,j) 
                location = str(stringx+str(int(i))+stringy+str(int(j)))
                locations.append(location)
        return x,y,location,cost,p
    else:
        pass

def move30(x,y,cost,p):    
    p = p + 'B'
    xmap = copy.deepcopy(x)
    ymap = copy.deepcopy(y)
    x = x + (d*math.cos(math.radians(30)))
    y = y + (d*math.sin(math.radians(30)))
    ctg = math.sqrt(((goal_x-x)**2)+((goal_y-y)**2))
    x = round(x)
    y = round(y)
    cost = ctg + ((len(p)-1)*d1)
    stringx,stringy = CoordToString(x,y) 
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    if (location not in locations) and (location not in travelled) and (location not in clearance) and x > 0 and x < 800 and y > 0 and y < 600:
        cv2.arrowedLine(image, (ymap,xmap), (y,x), (0, 255, 0), 1)
        update = {location : [cost,p]}
        travelled.update(update)
        for i in range(x-3,x+3):
            for j in range(y-3,y+3):
                stringx,stringy = CoordToString(i,j) 
                location = str(stringx+str(int(i))+stringy+str(int(j)))
                locations.append(location)
        return x,y,location,cost,p
    else:
        pass

def move60(x,y,cost,p):    
    p = p + 'C'
    xmap = copy.deepcopy(x)
    ymap = copy.deepcopy(y)
    x = x + (d*math.cos(math.radians(60)))
    y = y + (d*math.sin(math.radians(60)))
    ctg = math.sqrt(((goal_x-x)**2)+((goal_y-y)**2))
    x = round(x)
    y = round(y)
    cost = ctg + ((len(p)-1)*d1)
    stringx,stringy = CoordToString(x,y) 
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    if (location not in locations) and (location not in travelled) and (location not in clearance) and x > 0 and x < 800 and y > 0 and y < 600:
        cv2.arrowedLine(image, (ymap,xmap), (y,x), (0, 255, 0), 1)
        update = {location : [cost,p]}
        travelled.update(update)
        for i in range(x-3,x+3):
            for j in range(y-3,y+3):
                stringx,stringy = CoordToString(i,j) 
                location = str(stringx+str(int(i))+stringy+str(int(j)))
                locations.append(location)
        return x,y,location,cost,p
    else:
        pass

def move90(x,y,cost,p):    
    p = p + 'D'
    xmap = copy.deepcopy(x)
    ymap = copy.deepcopy(y)
    x = x + (d*math.cos(math.radians(90)))
    y = y + (d*math.sin(math.radians(90)))
    ctg = math.sqrt(((goal_x-x)**2)+((goal_y-y)**2))
    x = round(x)
    y = round(y)
    cost = ctg + ((len(p)-1)*d1)
    stringx,stringy = CoordToString(x,y) 
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    if (location not in locations) and (location not in travelled) and (location not in clearance) and x > 0 and x < 800 and y > 0 and y < 600:
        cv2.arrowedLine(image, (ymap,xmap), (y,x), (0, 255, 0), 1)
        update = {location : [cost,p]}
        travelled.update(update)
        for i in range(x-3,x+3):
            for j in range(y-3,y+3):
                stringx,stringy = CoordToString(i,j) 
                location = str(stringx+str(int(i))+stringy+str(int(j)))
                locations.append(location)
        return x,y,location,cost,p
    else:
        pass

def move120(x,y,cost,p):    
    p = p + 'E'
    xmap = copy.deepcopy(x)
    ymap = copy.deepcopy(y)
    x = x + (d*math.cos(math.radians(120)))
    y = y + (d*math.sin(math.radians(120)))
    ctg = math.sqrt(((goal_x-x)**2)+((goal_y-y)**2))
    x = round(x)
    y = round(y)
    cost = ctg + ((len(p)-1)*d1)
    stringx,stringy = CoordToString(x,y) 
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    if (location not in locations) and (location not in travelled) and (location not in clearance) and x > 0 and x < 800 and y > 0 and y < 600:
        cv2.arrowedLine(image, (ymap,xmap), (y,x), (0, 255, 0), 1)
        update = {location : [cost,p]}
        travelled.update(update)
        for i in range(x-3,x+3):
            for j in range(y-3,y+3):
                stringx,stringy = CoordToString(i,j) 
                location = str(stringx+str(int(i))+stringy+str(int(j)))
                locations.append(location)
        return x,y,location,cost,p
    else:
        pass

def move150(x,y,cost,p):    
    p = p + 'F'
    xmap = copy.deepcopy(x)
    ymap = copy.deepcopy(y)
    x = x + (d*math.cos(math.radians(150)))
    y = y + (d*math.sin(math.radians(150)))
    ctg = math.sqrt(((goal_x-x)**2)+((goal_y-y)**2))
    x = round(x)
    y = round(y)
    cost = ctg + ((len(p)-1)*d1)
    stringx,stringy = CoordToString(x,y) 
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    if (location not in locations) and (location not in travelled) and (location not in clearance) and x > 0 and x < 800 and y > 0 and y < 600:
        cv2.arrowedLine(image, (ymap,xmap), (y,x), (0, 255, 0), 1)
        update = {location : [cost,p]}
        travelled.update(update)
        for i in range(x-3,x+3):
            for j in range(y-3,y+3):
                stringx,stringy = CoordToString(i,j) 
                location = str(stringx+str(int(i))+stringy+str(int(j)))
                locations.append(location)
        return x,y,location,cost,p
    else:
        pass

def move180(x,y,cost,p):    
    p = p + 'G'
    xmap = copy.deepcopy(x)
    ymap = copy.deepcopy(y)
    x = x + (d*math.cos(math.radians(180)))
    y = y + (d*math.sin(math.radians(180)))
    ctg = math.sqrt(((goal_x-x)**2)+((goal_y-y)**2))
    x = round(x)
    y = round(y)
    cost = ctg + ((len(p)-1)*d1)
    stringx,stringy = CoordToString(x,y) 
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    if (location not in locations) and (location not in travelled) and (location not in clearance) and x > 0 and x < 800 and y > 0 and y < 600:
        cv2.arrowedLine(image, (ymap,xmap), (y,x), (0, 255, 0), 1)
        update = {location : [cost,p]}
        travelled.update(update)
        for i in range(x-3,x+3):
            for j in range(y-3,y+3):
                stringx,stringy = CoordToString(i,j) 
                location = str(stringx+str(int(i))+stringy+str(int(j)))
                locations.append(location)
        return x,y,location,cost,p
    else:
        pass

def move210(x,y,cost,p):    
    p = p + 'H'
    xmap = copy.deepcopy(x)
    ymap = copy.deepcopy(y)
    x = x + (d*math.cos(math.radians(210)))
    y = y + (d*math.sin(math.radians(210)))
    ctg = math.sqrt(((goal_x-x)**2)+((goal_y-y)**2))
    x = round(x)
    y = round(y)
    cost = ctg + ((len(p)-1)*d1)
    stringx,stringy = CoordToString(x,y) 
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    if (location not in locations) and (location not in travelled) and (location not in clearance) and x > 0 and x < 800 and y > 0 and y < 600:
        cv2.arrowedLine(image, (ymap,xmap), (y,x), (0, 255, 0), 1)
        update = {location : [cost,p]}
        travelled.update(update)
        for i in range(x-3,x+3):
            for j in range(y-3,y+3):
                stringx,stringy = CoordToString(i,j) 
                location = str(stringx+str(int(i))+stringy+str(int(j)))
                locations.append(location)
        return x,y,location,cost,p
    else:
        pass

def move240(x,y,cost,p):    
    p = p + 'I'
    xmap = copy.deepcopy(x)
    ymap = copy.deepcopy(y)
    x = x + (d*math.cos(math.radians(240)))
    y = y + (d*math.sin(math.radians(240)))
    ctg = math.sqrt(((goal_x-x)**2)+((goal_y-y)**2))
    x = round(x)
    y = round(y)
    cost = ctg + ((len(p)-1)*d1)
    stringx,stringy = CoordToString(x,y) 
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    if (location not in locations) and (location not in travelled) and (location not in clearance) and x > 0 and x < 800 and y > 0 and y < 600:
        cv2.arrowedLine(image, (ymap,xmap), (y,x), (0, 255, 0), 1)
        update = {location : [cost,p]}
        travelled.update(update)
        for i in range(x-3,x+3):
            for j in range(y-3,y+3):
                stringx,stringy = CoordToString(i,j) 
                location = str(stringx+str(int(i))+stringy+str(int(j)))
                locations.append(location)
        return x,y,location,cost,p
    else:
        pass

def move270(x,y,cost,p):    
    p = p + 'J'
    xmap = copy.deepcopy(x)
    ymap = copy.deepcopy(y)
    x = x + (d*math.cos(math.radians(270)))
    y = y + (d*math.sin(math.radians(270)))
    ctg = math.sqrt(((goal_x-x)**2)+((goal_y-y)**2))
    x = round(x)
    y = round(y)
    cost = ctg + ((len(p)-1)*d1)
    stringx,stringy = CoordToString(x,y) 
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    if (location not in locations) and (location not in travelled) and (location not in clearance) and x > 0 and x < 800 and y > 0 and y < 600:
        cv2.arrowedLine(image, (ymap,xmap), (y,x), (0, 255, 0), 1)
        update = {location : [cost,p]}
        travelled.update(update)
        for i in range(x-3,x+3):
            for j in range(y-3,y+3):
                stringx,stringy = CoordToString(i,j) 
                location = str(stringx+str(int(i))+stringy+str(int(j)))
                locations.append(location)
        return x,y,location,cost,p
    else:
        pass

def move300(x,y,cost,p):    
    p = p + 'K'
    xmap = copy.deepcopy(x)
    ymap = copy.deepcopy(y)
    x = x + (d*math.cos(math.radians(300)))
    y = y + (d*math.sin(math.radians(300)))
    ctg = math.sqrt(((goal_x-x)**2)+((goal_y-y)**2))
    x = round(x)
    y = round(y)
    cost = ctg + ((len(p)-1)*d1)
    stringx,stringy = CoordToString(x,y) 
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    if (location not in locations) and (location not in travelled) and (location not in clearance) and x > 0 and x < 800 and y > 0 and y < 600:
        cv2.arrowedLine(image, (ymap,xmap), (y,x), (0, 255, 0), 1)
        update = {location : [cost,p]}
        travelled.update(update)
        for i in range(x-3,x+3):
            for j in range(y-3,y+3):
                stringx,stringy = CoordToString(i,j) 
                location = str(stringx+str(int(i))+stringy+str(int(j)))
                locations.append(location)
        return x,y,location,cost,p
    else:
        pass

def move330(x,y,cost,p):    
    p = p + 'L'
    xmap = copy.deepcopy(x)
    ymap = copy.deepcopy(y)
    x = x + (d*math.cos(math.radians(330)))
    y = y + (d*math.sin(math.radians(330)))
    ctg = math.sqrt(((goal_x-x)**2)+((goal_y-y)**2))
    x = round(x)
    y = round(y)
    cost = ctg + ((len(p)-1)*d1)
    stringx,stringy = CoordToString(x,y) 
    location = str(stringx+str(int(x))+stringy+str(int(y)))
    if (location not in locations) and (location not in travelled) and (location not in clearance) and x > 0 and x < 800 and y > 0 and y < 600:
        cv2.arrowedLine(image, (ymap,xmap), (y,x), (0, 255, 0), 1)
        update = {location : [cost,p]}
        travelled.update(update)
        for i in range(x-3,x+3):
            for j in range(y-3,y+3):
                stringx,stringy = CoordToString(i,j) 
                location = str(stringx+str(int(i))+stringy+str(int(j)))
                locations.append(location)
        return x,y,location,cost,p
    else:
        pass

while checkGoal(current_x,current_y) == False:
    move00(current_x,current_y,current_cost,current_p)
    move30(current_x,current_y,current_cost,current_p)
    move60(current_x,current_y,current_cost,current_p)
    move90(current_x,current_y,current_cost,current_p)
    move120(current_x,current_y,current_cost,current_p)
    move150(current_x,current_y,current_cost,current_p)
    move180(current_x,current_y,current_cost,current_p)
    move210(current_x,current_y,current_cost,current_p)
    move240(current_x,current_y,current_cost,current_p)
    move270(current_x,current_y,current_cost,current_p)
    move300(current_x,current_y,current_cost,current_p)
    move330(current_x,current_y,current_cost,current_p)

    del travelled[start_loc]
    travelled = {k: v for k, v in sorted(travelled.items(), key=lambda item: item[1])}   
    start_loc = list(travelled.keys())[0]
    current_x = int(start_loc[0:3])
    current_y = int(start_loc[3:])
    current_cost = list(travelled.values())[0][0]
    current_p = list(travelled.values())[0][1]
    print(current_x,current_y,current_cost)
 
print("Solution found! Optimal path marked in red.")
x1 = copy.deepcopy(start_x)
y1 = copy.deepcopy(start_y)

image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)

for i in current_p:         #shows optimal path by back tracking from first parent node to reach solution
    if i == 'I':
        x2 = round(x1)
        y2 = round(y1)
    elif i == 'A':
        x2 = round(x1 + (d*math.cos(math.radians(0))))
        y2 = round(y1 + (d*math.sin(math.radians(0))))
        cv2.arrowedLine(image, (y1,x1), (y2,x2), (0,0,255), 1)
    elif i == 'B':
        x2 = round(x1 + (d*math.cos(math.radians(30))))
        y2 = round(y1 + (d*math.sin(math.radians(30))))
        cv2.arrowedLine(image, (y1,x1), (y2,x2), (0,0,255), 1)
    elif i == 'C':
        x2 = round(x1 + (d*math.cos(math.radians(60))))
        y2 = round(y1 + (d*math.sin(math.radians(60))))
        cv2.arrowedLine(image, (y1,x1), (y2,x2), (0,0,255), 1)
    elif i == 'D':
        x2 = round(x1 + (d*math.cos(math.radians(90))))
        y2 = round(y1 + (d*math.sin(math.radians(90))))
        cv2.arrowedLine(image, (y1,x1), (y2,x2), (0,0,255), 1)
    elif i == 'E':
        x2 = round(x1 + (d*math.cos(math.radians(120))))
        y2 = round(y1 + (d*math.sin(math.radians(120))))
        cv2.arrowedLine(image, (y1,x1), (y2,x2), (0,0,255), 1)
    elif i == 'F':
        x2 = round(x1 + (d*math.cos(math.radians(150))))
        y2 = round(y1 + (d*math.sin(math.radians(150))))
        cv2.arrowedLine(image, (y1,x1), (y2,x2), (0,0,255), 1)
    elif i == 'G':
        x2 = round(x1 + (d*math.cos(math.radians(180))))
        y2 = round(y1 + (d*math.sin(math.radians(180))))
        cv2.arrowedLine(image, (y1,x1), (y2,x2), (0,0,255), 1)
    elif i == 'H':
        x2 = round(x1 + (d*math.cos(math.radians(210))))
        y2 = round(y1 + (d*math.sin(math.radians(210))))
        cv2.arrowedLine(image, (y1,x1), (y2,x2), (0,0,255), 1)  
    elif i == 'I':
        x2 = round(x1 + (d*math.cos(math.radians(240))))
        y2 = round(y1 + (d*math.sin(math.radians(240))))
        cv2.arrowedLine(image, (y1,x1), (y2,x2), (0,0,255), 1)
    elif i == 'J':
        x2 = round(x1 + (d*math.cos(math.radians(270))))
        y2 = round(y1 + (d*math.sin(math.radians(270))))
        cv2.arrowedLine(image, (y1,x1), (y2,x2), (0,0,255), 1)
    elif i == 'K':
        x2 = round(x1 + (d*math.cos(math.radians(300))))
        y2 = round(y1 + (d*math.sin(math.radians(300))))
        cv2.arrowedLine(image, (y1,x1), (y2,x2), (0,0,255), 1)
    elif i == 'L':
        x2 = round(x1 + (d*math.cos(math.radians(330))))
        y2 = round(y1 + (d*math.sin(math.radians(330))))
        cv2.arrowedLine(image, (y1,x1), (y2,x2), (0,0,255), 1)
    x1 = x2
    y1 = y2
   
for i in obstacles:     #displays obstacles as black pixels on image map
    locx = int(i[0:3])
    locy = int(i[3:])
    image[locx,locy] = 0

rotated = imutils.rotate_bound(image,-90)       #rotates image to match rubric
cv2.imshow('image',rotated)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)  