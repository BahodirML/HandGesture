import cv2
import os
import numpy as np

#importing hand detector
from cvzone.HandTrackingModule import HandDetector


#camera setup
width, height = 1280, 720
    
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)


#get list of ppt images

folderPath = 'Presentation'
pathImages= sorted(os.listdir(folderPath), key = len)
#qprint(pathImages)


#variables
imageNumber = 0
hs, ws = int(120*1.2), int(213*1.2)
gestureThreshold = 500
buttonPressed = False
buttonCounter =0 
buttonDelay = 50
annotations = [[]] #[[(5,10), (20,30)], [], []]
annotationNumber = -1
annotationStart =False
#hand detector
detector = HandDetector (detectionCon=0.8, maxHands=1)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imageNumber])
    imgCurrent = cv2.imread(pathFullImage)



    hands, img = detector.findHands(img)
    




    if hands and buttonPressed is False:
        hand = hands[0]
        fingers=detector.fingersUp(hand)
        cx,cv = hand['center']
        lmList = hand['lmList']



        #Constrain values for easier drawing
        indexFinger = lmList[8][0], lmList[8][1]
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
        indexFinger = xVal, yVal


        if cv<=gestureThreshold: #if hand is at the height of the face
            annotationStart = False

            #Gesture 1 - Left
            if fingers ==[1,0,0,0,0]:
                annotationStart =False
                print('left')
                buttonPressed = True
                if imageNumber > 0:
                    imageNumber -= 1

                    annotations = [[]] 
                    annotationNumber = -1
                    
            #Gesture 2 - Right
            if fingers ==[0,0,0,0,1]:
                annotationStart =False
                print('Right')
                buttonPressed = True

                if imageNumber < len(pathImages)-1:
                    imageNumber += 1

                    annotations = [[]] 
                    annotationNumber = -1
                    

        #Gesture 3 - Show pointer
        if fingers ==[0,1,1,0,0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0,0,255), cv2.FILLED)   
            annotationStart = False

        #Gesture 4 - Draw pointer
        if fingers ==[0,1,0,0,0]:
            if annotationStart  is False:
                annotationStart = True
                annotationNumber +=1
                annotations.append([])
            
            cv2.circle(imgCurrent, indexFinger, 12, (0,0,255), cv2.FILLED)  
            annotations[annotationNumber].append(indexFinger)  

       


        #Gesture 5 - Erase
        if fingers ==[0,1,1,1,0]:
            if annotations:
                if annotationNumber> -1:
                    annotations.pop(-1)
                    annotationNumber -=1
                    buttonPressed= True
    else:
        annotationStart = False


    #button pressed iterations
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay :
            buttonCounter = 0
            buttonPressed = False


    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(imgCurrent, annotations[i][j-1], annotations[i][j], (0,0,200), 12)

    #adding webcam image on the slides
    imgsmall = cv2.resize(img, (ws,hs))
    h, w, _ = imgCurrent.shape

    #assigning metrics
    imgCurrent[0:hs, w - ws:w] = imgsmall




    cv2.imshow("Image", img)
    cv2.imshow('Slides', imgCurrent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break