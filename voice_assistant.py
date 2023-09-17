import os
import cv2
import boto3
import pyaudio
import smtplib
import pywhatkit
import pyttsx3 as px
from twilio.rest import Client
import speech_recognition as sr
import datetime
from datetime import date
import wikipedia

rec = sr.Recognizer()


def ec2launch():
    session = boto3.Session(aws_access_key_id='acess key id',
                            aws_secret_access_key='secret key', region_name='region name')
    launch = session.client('ec2', region_name='region name')
    launch.run_instances(ImageId="ami-id",
                         InstanceType="t2.micro",
                         MaxCount=1,
                         MinCount=1)


def create_s3_bucket():
    buck = input("enter unique bucket name")
    session = boto3.Session(aws_access_key_id='acesss key',
                            aws_secret_access_key='secret key', region_name='region name')

    bucket = session.client('s3')
    bucket.create_bucket(
        Bucket=buck,
        ACL='private',
        CreateBucketConfiguration={'LocationConstraint': 'region name'})


def simple_message():
    m = input("enter msg to send")
    account_sid = 'auth_sid'
    auth_token = 'auth_token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+virtual no from twilio',
        to='+91 phone no',
        body=m
    )

def image_cap():
    cap = cv2.VideoCapture(0)
    status, pic = cap.read()

    cv2.imshow("hi", pic)
    cv2.waitKey()
    cv2.destroyAllWindows()


def email(to_email, subject, content):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        msg = MIMEMultipart()
        msg['From'] = 'sender mail id'
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("sender mail id",'app pw key')
        text = msg.as_string()
        server.sendmail('sender mail id', to_email, text)
        server.quit()


def check_status(text, open_list, not_list):
    isPresent = False
    for t in open_list:
        if t in text:
            isPresent = True
            break

    for t in not_list:
        if t in text:
            isPresent = False
            break

    return isPresent


isSpeaking = True
while isSpeaking:
    with sr.Microphone() as mic:
        spk = px.init()
        spk.setProperty('rate', 150)
        spk.setProperty('Volume', 1.0)
        spk.say("say something ")
        spk.runAndWait()
        print("speak")
        audio = rec.listen(mic)
        try:
            choice = rec.recognize_google(audio)
            text = choice.lower()
            # text = choice.split(" ")
            print("you might have said : ", text, end="\n\n")

            open_statements = ["open", "start", "launch", "run", "create", "send","click"]
            not_statements = ["dont", "don't", "do not", "not", "never", "donot"]
            exit_statements = ["exit", "quit", "close", "stop", "terminate", "end", "finish", "bye", "goodbye",
                               "see you", "bye", "later", "soon"]

            if "chrome" in text:
                if not check_status(text, open_statements, not_statements):
                    spk.say("okay!")
                    spk.runAndWait()

                else:
                    os.system("start chrome")
                    spk.say("chrome has been opened.")
                    spk.runAndWait()

            elif "notepad" in text:
                    os.system("notepad")
                    spk.say("notepad has been opened.")
                    spk.runAndWait()

            elif "ec2 instance" in text:
                    ec2launch()
                    spk.say("ec2 instance has been launched. check on your aws console.")
                    spk.runAndWait()

            elif "whatsapp" in text:
                if not check_status(text, open_statements, not_statements):
                    spk.say("okay!")
                    spk.runAndWait()

                else:
                    number = input("Enter the number : ")
                    message = input("Enter the message : ")
                    pywhatkit.sendwhatmsg_instantly("+91" + number, message)
                    spk.say("Message has been sent on whatsapp")
                    spk.runAndWait()

            elif "email" in text:
                if not check_status(text, open_statements, not_statements):
                    spk.say("okay!")
                    spk.runAndWait()

                else:
                    to = input("Enter the email address : ")
                    subject = input("Enter the subject : ")
                    content = input("Enter the body of the email : ")
                    email(to, subject, content)
                    spk.say("email has been sent on mail")
                    spk.runAndWait()

            elif "message" in text:
                if not check_status(text, open_statements, not_statements):
                    spk.say("okay!")
                    spk.runAndWait()

                else:
                  #  n = input("Enter the number : ")
                 #   m = input("Enter message to be sent : ")
                    simple_message()
                    spk.say("Message has been sent through simple message")
                    spk.runAndWait()



            elif "s3 bucket" in text:
                    create_s3_bucket()
                    spk.say("bucket has been created ")
                    spk.runAndWait()

            elif "camera" in text:
                image_cap()
                spk.say("picture clicked")
                spk.runAndWait()
                
            elif "play" in text:
                                                         # if command.startswith("play "):
                song = text.replace("play ", '')
                pywhatkit.playonyt(song)
                spk.say("song has been played")
                spk.runAndWait()
                
            elif "information" in text:
                person = text.replace('information',' ')
                info = wikipedia.summary(person,3)
                print(info)
                spk.say(info)
                spk.runAndWait()
                
            elif "time" in text:
                time = datetime.datetime.now().strftime('%I %M  %p')
                print(time)
                spk.say("curent time"+ time)
                spk.runAndWait()

            elif "date" in text: 
                date =date.today()
                print(date)
                spk.say(date)
                spk.runAndWait()
        
           
            else:
                if not check_status(text, exit_statements, not_statements):
                    spk.say("Okay!")
                    spk.runAndWait()

                else:
                    isSpeaking = False
                    spk.say("Thank you for using me")
                    spk.runAndWait()
                    break

        except Exception as err:
            print("Error : ", err, end="\n\n")
