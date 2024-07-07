import yagmail
import os
import datetime

receivers = [ ""]  # Add more recipients as needed
body = "Attendance"
date = datetime.date.today().strftime("%B %d, %Y")
path = 'Attendance'
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
newest = files[-1]
filename = newest
sub = "Attendance Report for " + str(date)

yag = yagmail.SMTP("", "")  # Replace with your email and password(which is an app password)

for receiver in receivers:
    yag.send(
        to=receiver,
        subject=sub,
        contents=body,
        attachments=filename
    )

yag.close()
print("Emails Sent!")
