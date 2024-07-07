import datetime
import os
import time

import cv2
import pandas as pd


def recognize_attendance():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel/Trainner.yml")
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    if not os.path.exists("StudentDetails/StudentDetails.csv"):
        print("StudentDetails.csv not found.")
        return

    df = pd.read_csv("StudentDetails/StudentDetails.csv")
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)

    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, im = cam.read()
        if not ret:
            print("Failed to capture frame.")
            break

        faces = faceCascade.detectMultiScale(im, 1.5, 5, minSize=(int(minW), int(minH)))

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (10, 159, 255), 2)
            face_roi = im[y:y + h, x:x + w]
            Id, conf = recognizer.predict(cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY))
            print(conf)



            if conf < 100:
                aa = df.loc[df['Id'] == Id]['Name'].values
                confstr = "  {0}%".format(round(100 - conf))
                tt = str(Id) + "-" + aa
            else:
                Id = 'Unknown'
                tt = str(Id)
                confstr = "  {0}%".format(round(100 - conf))

            if (100 - conf) > 30:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

            if (100 - conf) > 30:
                tt = tt + " [Pass]"
                

                cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (0, 255, 0), 2)
            else:
                tt = tt + " [Rejected]"
                cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (0, 0, 255), 2)


        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('Attendance', im)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "Attendance"+os.sep+"Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName, index=False)
    print("Attendance Successful")
    cam.release()
    cv2.destroyAllWindows()


