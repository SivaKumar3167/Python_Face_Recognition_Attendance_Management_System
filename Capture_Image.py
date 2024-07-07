import csv
import cv2
import os

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def takeImages():
    Id = input("Enter Your Id: ")
    name = input("Enter Your Name: ")

    if is_number(Id) and name.isalpha():
        if not os.path.exists("TrainingImage"):
            os.makedirs("TrainingImage")
        if not os.path.exists("StudentDetails"):
            os.makedirs("StudentDetails")

        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while True:
            ret, img = cam.read()
            faces = detector.detectMultiScale(img, 1.3, 5, minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (10, 159, 255), 2)
                sampleNum = sampleNum + 1
                cv2.imwrite(f"TrainingImage/{name}.{Id}.{sampleNum}.jpg", img[y:y+h, x:x+w])
                cv2.imshow('frame', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name
        header = ["Id", "Name"]
        row = [Id, name]
        with open("StudentDetails/StudentDetails.csv", 'a+') as csvFile:
            writer = csv.writer(csvFile)
            if os.path.getsize("StudentDetails/StudentDetails.csv") == 0:
                writer.writerow(header)
            writer.writerow(row)
        csvFile.close()
    else:
        if is_number(Id):
            print("Enter Alphabetical Name")
        if name.isalpha():
            print("Enter Numeric ID")

if __name__ == "__main__":
    takeImages()
