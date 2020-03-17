# 2020 Maximiliano Palay
# This program contains portions of code extracted from some of the tutorials followed.
# Surveillance system that sends an email when it detects motion


#####   IMPORTS    #####
from compare_images import compare_images
from email_sender import EmailSender
from email_receiver import EmailReceiver

# libraries for image processing
import cv2
import picamera
import picamera.array

# libraries for thread
from time import sleep
import threading

# libraries to get date and time
from datetime import datetime

#####   constants/variables definitions    #####
email_server_address = "smtp.gmail.com"   # email provider server address
email_server_port = 465  # Port of server For SMTP SSL connection

body = "This is an email sent from Python security system."
email_system_address = "" # example@gmail.com
email_system_password = ""          # password

commanders = ["example1@gmail.com", "example2@gmail.com"] # emails that can do changes to the system
commands = ["arm", "disarm", "status", "sens"]  # commands supported by the system

system_is_armed = False
firstrun = True
prev_frame=None
actual_frame=None
image_diff_threshold = 16

emailSender = EmailSender(email_server_address, email_server_port, email_system_address, email_system_password)
emailReceiver = EmailReceiver(email_server_address, email_system_address, email_system_password)

#####   FUNCTION TO BE USED BY MAIN    #####

def arm_system():
    global system_is_armed
    global firstrun
    firstrun = True
    system_is_armed = True
    print(get_time()+" - System armed.")

def disarm_system():
    global system_is_armed
    system_is_armed = False
    print(get_time()+" - System disarmed.")

def send_arm_confirmation(sender):
    global emailSender
    date_time = get_time()
    print(date_time+" - Sending confirmation of arm to "+sender)
    emailSender.send_email(sender, "System is now armed.", "{} - {}".format(body, date_time), None) 

def send_disarm_confirmation(sender):
    global emailSender
    date_time = get_time()
    print(date_time+" - Sending confirmation of disarm to "+sender)
    emailSender.send_email(sender, "System is now disarmed.", "{} - {}".format(body, date_time), None) 

def send_status(sender):
    global firstrun
    global emailSender
    date_time = get_time()
    firstrun = True
    print(date_time+" - Sending status to {}".format(sender))
    if system_is_armed:
        emailSender.send_email(sender, "System status is armed.", "{} - {}".format(body, date_time), None) 
    else:
        emailSender.send_email(sender, "System status is disarmed.", "{} - {}".format(body, date_time), None) 

def send_threshold(sender):
    global firstrun
    global emailSender
    date_time = get_time()
    firstrun = True
    print(date_time+" - Sending threshold confirmation to "+sender)
    emailSender.send_email(sender, "System threshold has been changed to {}.".format(image_diff_threshold), "{} - {}".format(body, date_time), None)

def send_command_not_found(subject, sender):
    global emailSender
    date_time = get_time()
    print(date_time+" - \"{}\" is not recognized. No action has been taken".format(subject))
    emailSender.send_email(sender, "Your last email was ignored by the system.", "{} - {}".format(body, date_time), None) 

def send_alert(image):
    global emailSender
    date_time = get_time()
    print(date_time+" - alerting motion...")
    emailSender.send_email(commanders[1], "Alert! Motion detected!", "{} - {}".format(body, date_time), image)

def get_time():
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

#####   FUNCTIONS TO BE USED BY OTHER FUNCTIONS    #####

def check_email_and_act(): 
    ''' Checks for new email and acts accordingly'''
    global image_diff_threshold
    global firstrun
    global emailReceiver
    (sender, subject) = emailReceiver.get_new_emails()
    if sender and subject:
        if sender in commanders:    # only if sender is among the commanders
            print(get_time()+" - New message has been received! Sender is recognized!")
            if subject == commands[0]:  # arm
                arm_system()
                send_arm_confirmation(sender)
            elif subject == commands[1]:    # disarm
                disarm_system()
                send_disarm_confirmation(sender)
            elif subject == commands[2]:    # check status
                send_status(sender)
            elif commands[3] in subject:    # threshold set
                temp=subject.split(",")
                if len(temp)>1 and temp[1].isnumeric():
                    print(get_time()+" - Setting threshold to "+temp[1])
                    image_diff_threshold = int(temp[1])
                    send_threshold(sender)
                    firstrun = True
                else:
                    send_command_not_found(subject, sender)
            else: # command is not recognized
                send_command_not_found(subject, sender)
        else:   # sender is not recognized
            print(get_time()+" - New message has been received! Sender is not recognized! Ignoring email")
    else:   # no new emails
        print(get_time()+" - No new emails.")

#####   THREAD  #####

def check_email_periodically():
    ''' Function to be executed as thread to check for new emails and act accordingly.'''
    global email
    while True:
        check_email_and_act()
        sleep(15)

#####   MAIN    #####

if __name__ == "__main__":
    # begin email thread
    email_thread = threading.Thread(target=check_email_periodically, daemon=True)
    email_thread.start()
    # system startup
    date_time = get_time()
    print(date_time+" - starting system...")
    emailSender.send_email(commanders[1], "Starting system", "{} {} - {}".format("System is now up.", body, date_time), None)
    camera = picamera.PiCamera()
    stream = picamera.array.PiRGBArray(camera)
    camera.resolution = (1280,720)
    camera.framerate = 20
    camera.iso = 800
    sleep(1)
    # main loop
    while True:
        if system_is_armed:
            mse = 0
            camera.capture(stream, 'bgr')
            # stream.array now contains the image data in BGR order
            actual_frame = stream.array
            if not firstrun:
                image1 = cv2.cvtColor(actual_frame, cv2.COLOR_BGR2GRAY)
                image2 = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
                mse = compare_images(image1, image2)
            firstrun = False
            # do the MSE calculations
            print(mse)
            if mse > image_diff_threshold:
                check_email_and_act()
                cv2.imwrite("image.jpg", actual_frame)
                if system_is_armed:
                    send_alert("image.jpg")
                firstrun = True
            prev_frame = actual_frame
            stream.seek(0)
            stream.truncate()
        sleep(0.01)


