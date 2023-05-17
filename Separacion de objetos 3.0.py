from ast import Break
import cv2
import numpy as np
def dibujar(mask,color):
  contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  for c in contornos:
    area = cv2.contourArea(c)
    if area > 3000:
      M = cv2.moments(c)
      if (M["m00"]==0): M["m00"]=1
      x = int(M["m10"]/M["m00"])
      y = int(M['m01']/M['m00'])
      nuevoContorno = cv2.convexHull(c)
      cv2.circle(frame,(x,y),7,(0,255,0),-1)
      cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
      cv2.drawContours(frame, [nuevoContorno], 0, color, 3)
cap = cv2.VideoCapture(0)
azulBajo = np.array([94,80, 2],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)
amarilloBajo = np.array([15,100,20],np.uint8)
amarilloAlto = np.array([45,255,255],np.uint8)
verdeBajo = np.array([25, 52, 72],np.uint8)
verdeAlto = np.array([102, 255, 255],np.uint8)
redBajo1 = np.array([0,100,20],np.uint8)
redAlto1 = np.array([5,255,255],np.uint8)
redBajo2 = np.array([175,100,20],np.uint8)
redAlto2 = np.array([179,255,255],np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret,frame = cap.read()
    if ret == True:
        frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        maskAzul = cv2.inRange(frameHSV,azulBajo,azulAlto)
        maskAmarillo = cv2.inRange(frameHSV,amarilloBajo,amarilloAlto)
        maskverde = cv2.inRange(frameHSV,verdeBajo,verdeAlto)
        maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1)
        maskRed2 = cv2.inRange(frameHSV,redBajo2,redAlto2)
        maskRed = cv2.add(maskRed1,maskRed2)
        dibujar(maskAzul,(255,0,0))
        dibujar(maskAmarillo,(0,255,255))
        dibujar(maskverde,(0,255,0))
        dibujar(maskRed,(0,0,255))
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):

            break
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# Color rojo
    low_red = np.array([127, 110,77])
    high_red = np.array([255, 255,255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.bitwise_and(frame, frame, mask=red_mask)
    pb_red = dibujar(maskRed,(0,0,255))
# Color Azul
    low_blue = np.array([94,80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
    pb_blue = dibujar(maskAzul,(255,0,0))
    # Green color
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)
    pb_green = (maskverde,(0,255,0))
    # Every color except white
    low = np.array([0, 42, 0])
    high = np.array([179, 255, 255])
    mask = cv2.inRange(hsv_frame, low, high)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    pb_red = dibujar(maskRed,(0,0,255))
    pb_green = dibujar(maskverde,(0,255,0))
    pb_blue =  dibujar(maskAzul,(255,0,0))
    pb_amarillo=dibujar(maskAmarillo,(0,255,255))  
# Color Azul
#We finally show the result:
    #cv2.imshow("Frame", frame)
    cv2.imshow("Red", red)
    cv2.imshow("Blue", blue)
    cv2.imshow("Green", green)
    cv2.imshow("Result", result)
    #cv2.imshow('image',  im)
    key = cv2.waitKey(1)
    if key == 27:
        break