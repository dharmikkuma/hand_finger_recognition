import cv2
import mediapipe as mp
#################################
width, height = 640, 480
cap = cv2.VideoCapture(1)
cap.set(3, width)
cap.set(4, height)
################################

def findHands(img):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = mp.solutions.hands.Hands().process(imgRGB)
    points = []
    if result.multi_hand_landmarks:
        for id, lm in enumerate(result.multi_hand_landmarks[0].landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            points.append([id, cx, cy])
    return points


tip = [4, 8, 12, 16, 20]
pTime = 0
while True:
    success, img = cap.read()
    points = findHands(img)
    if len(points) !=0:
        finger = []
        # Thumb point
        if points[tip[0]][1] > points[tip[0] - 1][1]:
            finger.append(1)
        else: 
            finger.append(0)
        # fingers point
        for id in range(1,5):
            if points[tip[id]][2] < points[tip[id]- 2][2]:
                finger.append(1)
            else: 
                finger.append(0)
        fincount = finger.count(1)

        cv2.rectangle(img, (20,225), (170,425), (255,0,255),cv2.FILLED)
        cv2.putText(img,str(fincount),(45,375),cv2.FONT_HERSHEY_COMPLEX,5,(255,0,0),10)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break