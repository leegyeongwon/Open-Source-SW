import numpy as np
import cv2

xml = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+xml)

cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용
cap.set(3,640) # 너비
cap.set(4,480) # 높이

ans=int(input("Mosaic or pictures: "))#1이면 모자이크 2이면 사진

if ans == 1:
    while(True):
        ret, frame = cap.read() 
        frame = cv2.flip(frame, 1) # 좌우 대칭
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray,1.2,5) 
        print("Number of faces detected: " + str(len(faces)))

        if len(faces):
            for (x,y,w,h) in faces:
                face_img = frame[y:y+h, x:x+w] # 탐지된 얼굴 이미지 crop
                face_img = cv2.resize(face_img, dsize=(0, 0), fx=0.04, fy=0.04) # 축소
                face_img = cv2.resize(face_img, (w, h), interpolation=cv2.INTER_AREA) # 확대
                frame[y:y+h, x:x+w] = face_img # 탐지된 얼굴 영역 모자이크 처리

        cv2.imshow('result', frame)
        
        k = cv2.waitKey(30) & 0xff
        if k == 27: # Esc 키를 누르면 종료
            break

elif ans==2:
    pho=input("Write the name of the picture you want: ")
    mosaic_img = cv2.imread("./image/"+pho+".jpg")
    while(True):
        ret, frame = cap.read() 
        frame = cv2.flip(frame, 1) # 좌우 대칭
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray,1.2,5)
        print("Number of faces detected: " + str(len(faces)))

        if len(faces):
            for (x,y,w,h) in faces:
                """ 탐지된 얼굴 영역을 강건마 이미지로 바꾸는 코드"""
                # 탐지된 얼굴 영역에 맞도록 강건마 이미지의 높이와 너비를 바꿔줌.
                t = cv2.resize(mosaic_img, dsize=(h, w), interpolation= cv2.INTER_LINEAR)
                frame[y:y+h, x:x+w] = t # 탐지된 얼굴 영역을 강건마 이미지로 모자이크 처리

                """ 사람의 어깨선과 머리선이 강건마 이미지와 딱 맞게 이어지도록 구현한 코드
                    문제는 나한테만 딱 맞는다... """
                  #wi, hi = int(w*0.08/2), int(h*0.23/2)
                  #t = cv2.resize(mosaic_img, dsize=(w+wi*2, h+hi*2), interpolation=cv2.cv2.INTER_LINEAR)
                  #frame[y-hi:y+h+hi, x-wi:x+w+wi] = t

        cv2.imshow('result', frame)
        
        k = cv2.waitKey(30) & 0xff
        if k == 27: # Esc 키를 누르면 종료
            break
else:
    print("Invalid input")

cap.release()
cv2.destroyAllWindows()
