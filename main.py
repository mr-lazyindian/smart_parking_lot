import RPi.GPIO as p
import time
p.setwarnings(False)
p.setmode(p.BCM)
import http.client
import urllib
from gpiozero import Servo
key="7TWCEBP60VRLMW6G"
p.setup(18,p.IN) #IR1
p.setup(19,p.IN) #IR2
p.setup(25,p.IN) #IR3
p.setup(21,p.IN) #IR4
p.setup(23,p.IN) #USC-ECHO
p.setup(24,p.OUT)#USC-TRIG
p.setup(31,p.OUT) #IR-LED1
p.setup(26,p.OUT)#IR-LED2
p.setup(33,p.OUT)#IR-LED3
p.setup(35,p.OUT)#IR-LED4
p.setup(8,p.OUT)#SERVO-LED
p.setup(36,p.OUT)#USC-LED
servo=Servo(29)
a=p.input(18)
b=p.input(19)
c=p.input(25)
d=p.input(21)
print("Welcome to Parking lot")
print("You can see lot vacancies with this link (your thingspeak channel link)")
print("We need some details to get you there, hope you co-operates with us :)")
n=int(input("Enter type of vehicle (Only allowed vehicles are 2,3 and 4 wheeler only): "))
if(n==2):
    if(a==1):
        print("Sorry, not enough space to park :(")
    else:
        print("Note: Format is vehicle No - Vehicle type(2,3,4)")
        in1=str(input("Enter vehicle details separated by '-'(AB00AB0000-2): "))
        f = open("2wheeler_det.txt", "a")
        f.write("\n"+in1)
        f.close()
        print("Park at lot 1")
        print("Have a great day :)")
        servo.mid()
        p.output(8,p.HIGH)
        time.sleep(20)
elif(n==3):
    if(b==1):
        print("Sorry, not enough space to park :(")
    else:
        print("Note: Format is vehicle No - Vehicle type(2,3,4)")
        in2=str(input("Enter vehicle details separated by '-'(AB00AB0000-2): "))
        f = open("3wheeler_det.txt", "a")
        f.write("\n"+in2)
        f.close()
        print("Park at lot 2")
        print("Have a great day :)")
        servo.mid()
        p.output(8,p.HIGH)
        time.sleep(20)
elif(n==4):
    e=str(input("Enter model of car (sedan, suv or hatchback): "))
    if(e=="sedan"):
        if(c==1):
            print("Sorry, not enough space in parking lot")
        else:
            print("Note: Format is vehicle No - Vehicle type(2,3,4)")
            in3=str(input("Enter vehicle details separated by '-'(AB00AB0000-2)- suv/sedan/hatchback: "))
            f = open("sedan.txt", "a")
            f.write("\n"+in3)
            f.close()
            print("Park at lot 3")
            print("Have a great day :)")
            servo.mid()
            p.output(8,p.HIGH)
            time.sleep(20)
    elif(e=="suv" or e=="hatchback"):
        if(d==1):
            print("Sorry, not enough space in parking lot :(")
        else:
            print("Note: Format is vehicle No - Vehicle type(2,3,4)- suv/sedan/hatchback")
            in4=str(input("Enter vehicle details separated by '-'(AB00AB0000-2): "))
            f = open("suv.txt", "a")
            f.write("\n"+in4)
            f.close()
            print("Park at lot 4")
            print("Have a great day :)")
            servo.mid()
            p.output(8,p.HIGH)
            time.sleep(20)
else:
    print("Sorry for the inconvenience :(")
    print("We're looking forward to increase parking space for better experience ;{")

#Ultrasonic code
while True:
    p.output(24,False)
    time.sleep(1)
    p.output(24,True)
    time.sleep(0.000001)
    p.output(24,False)
    while(p.input(23)==0):
        startTime=time.time()
    while(p.input(23)==1):
        stopTime=time.time()
    timeElapsed=stopTime-startTime
    d=(timeElapsed*34400/2)
    D=round(d)
    time.sleep(0.1)
    if(d<20):
        p.output(36,p.HIGH)
        servo.mid()
    #Thingspeak 
    params = urllib.parse.urlencode({'field1': a,'field2':b,'field3':c,'field4':d, 'key':key })
    headers = {"Content-typZZe": "application/x-www-form- urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print (response.status, response.reason)
        data = response.read()
        conn.close()
    except:
        print ("connection failed")
        break

    #Parking lot vacancy
    if(a==1):
        p.output(31,p.HIGH)
    else:
        p.output(31,p.LOW)
    if(b==1):
        p.output(31,p.HIGH)
    else:
        p.output(31,p.LOW)
    if(c==1):
        p.output(31,p.HIGH)
    else:
        p.output(31,p.LOW)
    if(d==1):
        p.output(31,p.HIGH)
    else:
        p.output(31,p.LOW)

