import cv2
import smtplib
import os
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import boto3
from twilio.rest import Client


listener = sr.Recognizer() #to recogniize voice
speak = pyttsx3.init()
voices = speak.getProperty('voices')     #to set all the voices
speak.setProperty('voice', voices[1].id)  # to speak in female voice

#we are calling the talk fun and when talk fun is called it whatever says the paramenter we are passing the function

def talk(text):
    speak.say(text)
    speak.runAndWait()

#to ans our ques
def take_command():
  command = ""  # Initialize command with an empty string
    try:
        with sr.Microphone() as source: # use the microphone
            print("  listening....")
            
#use our microphone as source and calling speechrecognizier to listen this source
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa','')
                print(command)
    except:
     pass
    return command

def image_cap():
    cap = cv2.VideoCapture(0)
    status, pic = cap.read()

    cv2.imshow("hi", pic)
    cv2.waitKey()
    cv2.destroyAllWindows()
 

def ec2launch():
    myec2 = boto3.client("ec2")  # connected with ec2 service in aws directly

    response = myec2.run_instances(ImageId='ami id ',
                                   InstanceType="t2.micro",
                                   MaxCount=1,
                                   MinCount=1
                                   )

def sms():
    account_sid = 'account_sid from twilio'
    auth_token = 'auth_token from twilio'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='virtual number from twilio account ',
        to='your no with country code',
        body="msg u want to send"
    )
    print("succesfully sent msg")

def create_s3_bucket(bucket_name, region):
    # Create a new S3 client with the specified region
    s3 = boto3.client('s3', region_name=region)

    # Create the bucket with the specified region
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})

    print(f"Bucket '{bucket_name}' created successfully in region '{region}'.")


def whatsap():
    ch=input("enter an no")
    msg = input("enter msg")
    pywhatkit.sendwhatmsg_instantly(ch, msg)

def email():
    from email.message import EmailMessage
    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = "holla holla!!"
    msg['From'] = "sender mail id"
    msg['To'] = "receiver mail id"
    msg.set_content(" enter msg u want to send")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("sender mail id", 'app password key')
        smtp.send_message(msg)

def run():
    command = take_command()
    print(command)
       if command.startswith("play "):
        song = command.replace("play ", '')
        talk("playing " + song)
        pywhatkit.playonyt(song)

    elif ("chrome") in command:
        os.system("start chrome")
        speak.say("chrome has been open")
        speak.runAndWait()

    elif ("notepad") in command:
        os.system("notepad")
        speak.say("notepad has been open")
        speak.runAndWait()

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I %M  %p')
        print(time)
        talk('current time is' + time)

    elif  ('information')in command:
            person = command.replace('information',' ')
            info = wikipedia.summary(person,3)
            print(info)
            talk(info)

    elif ("whatsapp" ) in command:
        whatsap()
        speak.say("Message has been sent on whatsapp")
        speak.runAndWait()

    elif ("click picture") in command:
        image_cap()
        speak.say("picture clicked")
        speak.runAndWait()

    elif ("send mail" ) in command:
        email()
        speak.say("email has been sent on mail")
        speak.runAndWait()

    elif ("send sms")in command:
        sms()
        speak.say("Message had been sent through sms")
        speak.runAndWait()



    elif ("launch instatance") in command:
        ec2launch()
        speak.say('instance launched')
        speak.runAndWait()

   
    elif ("create s3 bucket")in command:
        create_s3_bucket("mybucket", "ap-south-1")
        speak.say("bucket has been created with name mybucket")
        speak.runAndWait()

    else:
        talk("please say again!")


while True:
    run()
