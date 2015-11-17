import Myro
from Myro import *
from Graphics import *
from random import *

width = 500
height = 500
sim = Simulation("Maze World", width, height, Color("gray"))

#outside walls
sim.addWall((10, 10), (490, 20), Color("black"))
sim.addWall((10, 10), (20, 490), Color("black"))
sim.addWall((480, 10), (490, 490), Color("black"))
sim.addWall((10, 480), (490, 490), Color("black"))

#blue spot
poly = Circle((50, 50), 45)
poly.bodyType = "static"
poly.color = Color("blue")
poly.outline = Color("black")
sim.addShape(poly)

#red spot
poly = Circle((450, 50), 45)
poly.bodyType = "static"
poly.color = Color("red")
poly.outline = Color("black")
sim.addShape(poly)

#green spot
poly = Circle((50, 450), 45)
poly.bodyType = "static"
poly.color = Color("green")
poly.outline = Color("black")
sim.addShape(poly)

#yellow spot
poly = Circle((450, 450), 45)
poly.bodyType = "static"
poly.color = Color("yellow")
poly.outline = Color("black")
sim.addShape(poly)

#begin simulation and sets robot's position
makeRobot("SimScribbler", sim)
sim.setPose(0, width/2, height/2, 0)

sim.setup()

# 1-RED
# 2-GREEN
# 3-BLUE
# 4-YELLOW

#The following is a helper function 
#Inputs: A picture and a color represented by the list above
#Returns the average x location of the color in the picture or -1 if the robot has found the color spot
totalPixelNum = 0
def findColorSpot(picture, color):
    xPixelSum = 0
    totalPixelNum = 0
    averageXPixel = 0

    show(picture)

    for pixel in getPixels(picture):
        if(color == 1 and getRed(pixel) > 200 and getGreen(pixel) == 0 and getBlue(pixel) == 0):
            xPixelSum += getX(pixel)
            totalPixelNum += 1
        elif(color == 2 and getRed(pixel)== 0 and getGreen(pixel) > 100 and getBlue(pixel) == 0):
            xPixelSum += getX(pixel)
            totalPixelNum += 1
        elif(color == 3 and getRed(pixel) == 0 and getGreen(pixel) == 0 and getBlue(pixel) > 200):
          
            xPixelSum += getX(pixel)
            totalPixelNum += 1
        elif(color == 4 and getRed(pixel) > 200 and getGreen(pixel) > 200 and getBlue(pixel) == 0):
            
            xPixelSum += getX(pixel)
            totalPixelNum += 1
    if(totalPixelNum != 0):
        averageXPixel = xPixelSum/totalPixelNum

    #Handles the case where robot has found the spot if it is near it
    #If necessary adjust the value
    if(totalPixelNum/(getWidth(picture)*getHeight(picture)) > 0.5): #Changed from 0.21 to 0.5 to make robot actually touch blob
        averageXPixel = -1

    return averageXPixel


# Use the following integers for colors:
# 1-RED
# 2-GREEN
# 3-BLUE
# 4-YELLOW

######################Code Starts Here##################################

def moveToBlob(color):
    colorFound = 0
    while colorFound == 0: #while color found=0 repeat the process to get desired pixels in the field of view
        turnBy(30)
        pic = takePicture()
        #show(pic)
        avg = findColorSpot(pic, color)
        print(avg)
        wait(.2)
        if avg >20:
            colorFound =1   #when the desired colored pictures in the field of view, set color found to 1
        else:
            colorFound = 0

    colorCenter = 0         #if desired color is found in the field of view, set colorCenter=0
    if colorFound ==1:
    
        while colorCenter == 0:     #while colorCenter=0 (desired pixels are in field of view)
            pic = takePicture()     #take picture, print (findColorSpot)
            #show(pic)
            avg = findColorSpot(pic, color)
            print(avg)
            wait(.2)
            if avg > (256/2)+10:    #if the colored pixels are right of center (20 pixels wide), turn 3 degrees left
                turnBy(-3)
            elif avg < (256/2)-10:  #if the colored pixels are left of center (20 pixels wide), turn 3 degrees right
                turnBy(3)
            elif avg > (256/2)-10 and avg < (256/2)+10: #if the colored pixels are in the center of field of view, set colorCenter=1
                colorCenter = 1

    if colorCenter == 1: #if colored pixels are centered
        onColor = 0     #set onColor=0 (you are not touching the blob)
        while onColor == 0:
            forward(1,.3)   #move forward, take a picture, print (findColorSpot)
            pic = takePicture()
            #show(pic)
            avg = findColorSpot(pic, color)
            print(avg)
            if (avg == -1): #if avg=-1, robot is touching the blob
                onColor = 1
                

    if onColor == 1: #I think theres a problem with the onColor function (I don't thing findColorSpot is ever reaching -1, which could be the problem)
        stop()
        speak('blob found.')

user_choice = raw_input("Please put color choice here. 1 = red, 2 = green, 3 = blue, 4 = yellow.")
int_choice = int(user_choice)

moveToBlob(int_choice)



