#import libraries
from dronekit import *
import time
import speech_recognition as sr





#connect of vehicle
vehicle=connect('127.0.0.1:14551', baud=921600, wait_ready=True)


#takeoff function
def arm_takeoff(height):
    #check if drone is ready

    while not vehicle.is_armable:#staying in loop till vehicle isnt armed
        print("Waiting for drone")
        time.sleep(1)

    #change mode and arm
    print("arming")
    vehicle.mode=VehicleMode('GUIDED')#ensures if code is stuck vehicle is also stationary
    vehicle.armed=True

    #check if drone is armed
    while not vehicle.armed:
        print("Waiting for arm")
        time.sleep(1)

    #takeoff
    print("takeoff")
    vehicle.simple_takeoff(height) #simple take off is used

    #reporting altitude every 1s and finally break out

    while True:
        print("Reached", vehicle.location.global_relative_frame.alt)
        if (vehicle.location.global_relative_frame.alt>=height*0.95):#reached 95% of hight youve entered, firware allows for 5% error

            print("Reached target altitude")
            break

        time.sleep(1)

while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
    
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
            time.sleep(3)
            if text:
                if text == 'launch':
                    arm_takeoff(10)
                    time.sleep(10)
                elif text == 'land':
                    print("ok landing")
                    vehicle.mode=VehicleMode('RTL')
                    time.sleep(10)
                    vehicle.close()
            
                    break
    
        except:
            print("Sorry could not recognize what you said")
    
    
