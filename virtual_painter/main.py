import cv2
import HandTrackingModule as htm
import numpy as np

cap=cv2.VideoCapture(0)


detector=htm.handDetector()
draw_color=(0,0,255)
img_canvas=np.zeros((720,1280,3),np.uint8)


while True:
    success,img=cap.read()
    img=cv2.resize(img,(1280,720))
    img=cv2.rectangle(img,(20,10),(256,100),(0,0,255),-1)
    img=cv2.rectangle(img,(276,10),(512,100),(0,255,0),-1)
    img=cv2.rectangle(img,(522,10),(758,100),(255,0,0),-1)
    img=cv2.rectangle(img,(778,10),(1014,100),(0,255,255),-1)
    img=cv2.rectangle(img,(1034,10),(1270,100),(255,255,255),-1)
    cv2.putText(img,"ERASER",org=(1100,60),fontFace=cv2.FONT_HERSHEY_COMPLEX,fontScale=1,color=(0,0,0))



    #find hands
    img=detector.findHands(img)
    lmlist=detector.findPosition(img)
    #print(lmlist)

    if len(lmlist)!=0:
        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]
        #print(x1,y1)
    # chech if finger is up
        fingers=detector.fingersUp()
       # print(fingers)

    #selection mode - index and middle finger is up
        if fingers[1]and fingers[2]:
            print('selection_mode')
            
            xp,yp=0,0

            if y1<100:
                if 20<x1<256:
                    print('red')
                    draw_color=(0,0,255)
                elif 256<x1<512:
                    print('green')
                    draw_color=(0,255,0)
                elif 512<x1<758:
                    print('blue')
                    draw_color=(255,0,0)
                elif 758<x1<1014:
                    print('yellow')
                    draw_color=(0,255,255)
                elif 1014<x1<1270:
                    print('eraser')
                    draw_color=(0,0,0)
            cv2.rectangle(img,(x1,y1),(x2,y2),draw_color,cv2.FILLED)

    #drawing mode - only index finger is up
        if (fingers[1]and not fingers[2]):
            print('drawing_mode')


            if xp==0 and yp==0:
                xp=x1
                yp=y1

            if draw_color==(0,0,0):
                # for eraser size
                cv2.line(img,(xp.yp),(x1,y1),color=draw_color,thickness=50)
                cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_color,thickness=50)
            else:
                #color brush
                cv2.line(img,(xp,yp),(x1,y1),color=draw_color,thickness=10)
                cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_color,thickness=10)

            xp,yp=x1,y1

    img_gray=cv2.cvtColor(img_canvas,cv2.COLOR_BGR2GRAY)
    _,img_inv=cv2.threshold(img_gray,20,255,cv2.THRESH_BINARY_INV)
    img_inv=cv2.cvtColor(img_inv,cv2.COLOR_GRAY2BGR)
    
    img=cv2.bitwise_and(img,img_inv)
    img=cv2.bitwise_or(img,img_canvas)


    img=cv2.addWeighted(img,1,img_canvas,0.5,0)


    cv2.imshow('virtual painter',img)
    #cv2.imshow('canvas',img_canvas)
    if cv2.waitKey(1) & 0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()