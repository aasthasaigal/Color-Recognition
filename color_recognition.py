import cv2 as cv
import pandas as pd  

#Reading the image
image = cv.imread("blocks.jpg")

#Resizing the image
resized_image = cv.resize(image, (600,400))

#Declaring variables
clicked = False
r = g = b = xpos = ypos = 0

#Reading csv file using pandas
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('color_dataset.csv', names=index, header=None)

#Function to calculate minimum distance from all colors and get the most matching color
def colorName(R,G,B):
    min = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=min):
            min = d
            cname = csv.loc[i,"color_name"]
    return cname

#Function to get x,y coordinates of mouse double click
def coord(event, x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos,clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = resized_image[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
       
cv.namedWindow('ColorRecognition')
cv.setMouseCallback('ColorRecognition',coord)

while(True):

    cv.imshow("ColorRecognition",resized_image)
    if (clicked):
   
        #Creating a rectangle to display values
        cv.rectangle(resized_image,(20,20), (590,60), (b,g,r), -1)
        cv.circle(resized_image,(40,100), 30 , (b,g,r), -1)

        #Text to display color name and RGB values
        text = colorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)

        #For dark colors-display text in white
        cv.putText(resized_image, text,(50,50),2,0.8,(255,255,255),2,cv.LINE_AA)

        #For light colors display text in black
        if(r+g+b>=600):
            cv.putText(resized_image, text,(50,50),2,0.8,(0,0,0),2,cv.LINE_AA)
            
        clicked=False

    #Breaking the loop using 'e'   
    if cv.waitKey(20) & 0xFF ==ord('e'):
        break
    
cv.destroyAllWindows()

