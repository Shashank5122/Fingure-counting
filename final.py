import cv2
import math
import numpy as np

capture = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier('hand_cascade.xml')
while(True):
    ret, img = capture.read()
    blur = cv2.GaussianBlur(img,(5,5),0) 
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY) 
    retval2,thresh1 = cv2.threshold(gray,10,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    hand = cascade.detectMultiScale(thresh1, 2.3, 5) 
    mask = np.zeros(thresh1.shape, dtype = "uint8") 
    for (x,y,w,h) in hand: # MARKING THE DETECTED ROI
        cv2.rectangle(img,(x,y),(x+w,y+h), (122,122,0), 2) 
        cv2.rectangle(mask, (x,y),(x+w,y+h),255,-1)
    img2 = cv2.bitwise_and(thresh1, mask)
    final = cv2.GaussianBlur(img2,(7,7),0)	
    _,contours,_ = cv2.findContours(final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, 0, (255,255,0), 3)
    cv2.drawContours(final, contours, 0, (255,255,0), 3)
    if len(contours) > 0:
        cnt=contours[0]
        hull = cv2.convexHull(cnt, returnPoints=False)
		# finding convexity defects
        defects = cv2.convexityDefects(cnt, hull)
        count_defects = 0
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]

            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])

    # finding length of all sides of triangle
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

    # applying cosine rule here
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            if angle <= 90:
                count_defects += 1
                cv2.circle(img, far, 1, [0,0,255], -1)
            cv2.line(img,start, end, [0,255,0],3)

        if count_defects == 1:
            cv2.putText(img,"1", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 3, 3)
        elif count_defects == 2:
            cv2.putText(img, "2", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 3, 3)
        elif count_defects == 3:
            cv2.putText(img,"3", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 3, 3)
        elif count_defects == 4:
            cv2.putText(img,"4", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 3, 3)
        else:
            cv2.putText(img,"5", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 3, 3)
        
    cv2.imshow('img',thresh1)
    cv2.imshow('img1',img)

    if(cv2.waitKey(1) & 0xff==ord("q")):
        break
capture.release()
cv2.destroyAllWindows()
