# -*- coding: utf-8 -*-
#h25 v4

import time
import sys
from naoqi import ALProxy, ALModule, ALBroker
import motion
import select
import vision_showimages as vis
import numpy as np
import almath
from PyQt4.QtGui import QWidget, QImage, QApplication, QPainter, QPushButton
from optparse import OptionParser


robotIP = "172.20.27.244" #Rouge
#robotIP = "172.20.28.103" #Bleu
#robotIP = "172.20.12.49" 
#robotIP = "172,20,11,237"
#robotIP = "172.20.28.103"


port = 9559
CameraID = 0
Frequency = 0.0 #low speed
t=1.0


try:
    motionProxy = ALProxy("ALMotion", robotIP, port)
except Exception, e:
    print"Could not create proxy to ALMotion"
    print"Error was: ", e
try:
    postureProxy = ALProxy("ALRobotPosture", robotIP, port)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e
try:
    sonarProxy = ALProxy("ALSonar", robotIP, port)
    sonarProxy.subscribe("myApplication")
except Exception, e:
    print "Could not create proxy to ALSonar"
    print "Error was: ", e

try :
    audio = ALProxy("ALAudioDevice", robotIP,port)
    audio.setOutputVolume(30)
except Exception, e: 
    print "Could not create proxy to ALaudioProxy"
    print "Error was: ", e
try :
    tts = ALProxy("ALTextToSpeech", robotIP, port)
    tts.setLanguage("French")
except Exception, e: 
    print "Could not create proxy to ALTextToSpeech"
    print "Error was: ", e

try:
    memoryProxy = ALProxy("ALMemory",robotIP, port)
except Exception, e:
    print "Could not create proxy to ALMemory"
    print "Error was: ", e
    
try:
    BatteryProxy = ALProxy("ALBattery",robotIP, port)
except Exception, e:
    print "Could not create proxy to AlBattery"
    print "Error was: ", e
    
try :
    audioProxy = ALProxy("ALAudioPlayer", robotIP, port)
except Exception, e:
    print'Could not create proxy to ALMotion'
    print"Error was: ",e




#stiffness for real NAO Robot
def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def doInitialisation():
    print">>>>>> Initialisation"
    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)    
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    

#class Battery(ALModule):
#    """ Mandatory docstring.
#        comment needed to create a new python module
#    """
#    def __init__(self, name):
#        ALModule.__init__(self, name)
#        # No need for IP and port here because
#        # we have our Python broker connected to NAOqi broker
#        # Create a proxy to ALTextToSpeech for later use
#        self.battery = BatteryProxy
#        self.level = 0
#
#        # Subscribe to the BatteryChange event:
#        self.battery.subscribeToEvent("BatteryChargeChanged",
#            "BatteryRob",
#            "callBackBattery")
#        
#    def callBackBattery(self, *_args):
#        """ Mandatory docstring.
#        comment needed to create a bound method
#        """
#        self.battery.unsubscribeToEvent("BatteryChargeChanged",
#                                        "BatteryRob") 
#        print 'im right here'
#        print self.percentage
#        self.battery.unsubscribeToEvent("BatteryChargeChanged",
#                                            "BatteryRob") 
#    

#==============================================================================
# Classe de test de toutes les articulations
#==============================================================================



def configRob(HeadYawAngle, HeadPitchAngle, ShoulderPitchAngle, ShoulderRollAngle, ElbowYawAngle, ElbowRollAngle,WristYawAngle, HandAngle, kneeAngle, torsoAngle, spreadAngle):
    robotConfig = motionProxy.getRobotConfig()
    robotName = ""
    for i in range(len(robotConfig[0])):
        if (robotConfig[0][i] == "Model Type"):
            robotName = robotConfig[1][i]
    
        if robotName == "naoH25":
    
            Head     = [HeadYawAngle, HeadPitchAngle]
    
            LeftArm  = [ShoulderPitchAngle, +ShoulderRollAngle, +ElbowYawAngle, +ElbowRollAngle, +WristYawAngle, HandAngle]
            RightArm = [ShoulderPitchAngle, -ShoulderRollAngle, -ElbowYawAngle, -ElbowRollAngle, -WristYawAngle, HandAngle]
    
            LeftLeg  = [0.0,                      #hipYawPitch
                        spreadAngle,              #hipRoll
                        -kneeAngle/2-torsoAngle,  #hipPitch
                        kneeAngle,                #kneePitch
                        -kneeAngle/2,             #anklePitch
                        -spreadAngle]             #ankleRoll
            RightLeg = [0.0, -spreadAngle, -kneeAngle/2-torsoAngle, kneeAngle, -kneeAngle/2,  spreadAngle]
    
        elif robotName == "naoH21":
    
            Head     = [HeadYawAngle, HeadPitchAngle]
    
            LeftArm  = [ShoulderPitchAngle, +ShoulderRollAngle, +ElbowYawAngle, +ElbowRollAngle]
            RightArm = [ShoulderPitchAngle, -ShoulderRollAngle, -ElbowYawAngle, -ElbowRollAngle]
    
            LeftLeg  = [0.0,  spreadAngle, -kneeAngle/2-torsoAngle, kneeAngle, -kneeAngle/2, -spreadAngle]
            RightLeg = [0.0, -spreadAngle, -kneeAngle/2-torsoAngle, kneeAngle, -kneeAngle/2,  spreadAngle]
    
        elif robotName == "naoT14":
    
            Head     = [HeadYawAngle, HeadPitchAngle]
    
            LeftLeg  = [0.0,  spreadAngle, -kneeAngle/2-torsoAngle, kneeAngle, -kneeAngle/2, -spreadAngle]
            RightLeg = [0.0, -spreadAngle, -kneeAngle/2-torsoAngle, kneeAngle, -kneeAngle/2,  spreadAngle]
    
            LeftLeg  = []
            RightLeg = []
    
        elif robotName == "naoT2":
    
            Head     = [HeadYawAngle, HeadPitchAngle]
    
            LeftArm  = []
            RightArm = []
    
            LeftLeg  = []
            RightLeg = []
    
        else:
            print "ERROR : Your robot is unknown"
            print "This test is not available for your Robot"
            print "---------------------"
            exit(1)
    
        # Gather the joints together
        pTargetAngles = Head + LeftArm + LeftLeg + RightLeg + RightArm
    
        # Convert to radians
        pTargetAngles = [ x * almath.TO_RAD for x in pTargetAngles]

        # We use the "Body" name to signify the collection of all joints
        pNames = "Body"
        # We set the fraction of max speed
        pMaxSpeedFraction = 0.35
        # Ask motion to do this with a blocking call    
        motionProxy.angleInterpolationWithSpeed(pNames, pTargetAngles, pMaxSpeedFraction)

class Robot:
    def __init__(self, rt, ia, am, space):
            self.d_mvt = {}
            self.reference_time = rt
            self.isAbsolute = ia
            self.axisMask = am
            self.space = space
            self.tempo_time = 0

    def mvt(self, where, path):
            reference_time = 0
            if self.tempo_time != 0:
                reference_time = self.tempo_time
                self.tempo_time = 0
            else:
                reference_time = self.reference_time    
            if not self.d_mvt.has_key(where):
                self.d_mvt[where] = path
            else:
                old_path = self.d_mvt[where]
                saved_path = [el1 + el2 for el1, el2 in zip(path, old_path)]
                self.d_mvt[where] = saved_path
            motionProxy.positionInterpolation(where, self.space, path, self.axisMask, reference_time, self.isAbsolute)
                    
            time.sleep(1.0)



#==============================================================================
# Audio
#==============================================================================
def TestTts(texte):
    tts.say(texte)
    
#==============================================================================
# """Vision"""
#==============================================================================


def Test_Image():

    ####
    # Create proxy on ALVideoDevice

    print "Creating ALVideoDevice proxy to ", robotIP

    camProxy = ALProxy("ALVideoDevice", robotIP, port)

    ####
    # Register a Generic Video Module

    resolution = vision_definitions.kQVGA
    colorSpace = vision_definitions.kYUVColorSpace
    fps = 30

    nameId = camProxy.subscribe("python_GVM", resolution, colorSpace, fps)
    print nameId

    print 'getting images in local'
    for i in range(0, 20):
      camProxy.getImageLocal(nameId)
      camProxy.releaseImage(nameId)

    resolution = vision_definitions.kQQVGA
    camProxy.setResolution(nameId, resolution)

    print 'getting images in remote'
    for i in range(0, 20):
      camProxy.getImageRemote(nameId)

    camProxy.unsubscribe(nameId)

    print 'end of gvm_getImageLocal python script'

def showNaoImage():
    videoRecorderProxy = ALProxy("ALVideoRecorder", robotIP, port)
    
    # This records a 320*240 MJPG video at 10 fps.
    # Note MJPG can't be recorded with a framerate lower than 3 fps.
    videoRecorderProxy.setResolution(1)
    videoRecorderProxy.setFrameRate(10)
    videoRecorderProxy.setVideoFormat("MJPG")
    videoRecorderProxy.startRecording("./", "test")

    time.sleep(5)
    # Video file is saved on the robot in the
    # /home/nao/recordings/cameras/ folder.
    videoInfo = videoRecorderProxy.stopRecording()
    #print type video
    print "Video was saved on the robot: ", videoInfo[1]
    print "Num frames: ", videoInfo[0]
    video = memoryProxy.getData("./test.avi")


#==============================================================================
# """Sensors"""
#==============================================================================
def TrySensors():

    Left = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    Right = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value") 
    print 'Left :', Left
    print 'Right:', Right
    

def Accelero():
    X = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccelerometerX/Sensor/Value")
    Y = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccelerometerY/Sensor/Value") 
    Z = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccelerometerZ/Sensor/Value")
#    print "X = ", X
#    print "Y = ", Y
#    print "Z = ", Z
    
    AngleX = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AngleX/Sensor/Value")
    AngleY = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AngleX/Sensor/Value")
    return AngleX, AngleY

    
#==============================================================================
# """Motion"""
#==============================================================================
def dorun(t):
    motionProxy.setWalkTargetVelocity(1, 0, 0, 1)
    t0 = time.time()
    AngX, AngY = [], []
    while time.time()< (t0 + t):
        accelero = Accelero()
        AngX.append(accelero[0])
        AngY.append(accelero[1])
        FSRPIED()
        if memoryProxy.getData("footContact") == 0:
            print 'Foot contact lost'
        else : 
            print 'Foot contact ok'
        time.sleep(0.05)
#    motionProxy.moveTo (0.6, 0, 0)
#    time.sleep(t)
#    maxAngX, maxAngY = max(AngX), max(AngY)
#    print "maxAngX, maxAngY = ", maxAngX, ", ", maxAngY
    motionProxy.setWalkTargetVelocity(0.0, 0, 0, 1)
    print"running"
    

def doback():
    
     motionProxy.moveTo (-0.6, 0, 0)
     
     time.sleep(t)
     print"back"
    
def doleft(angle):
    
    initRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(False))
    
    theta= angle
#    motionProxy.setWalkTargetVelocity(0, 0, 0.5, 0.01)
    motionProxy.moveTo (0, 0, theta)
    #####################
    ## get robot position after move
    #####################
    endRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(False))

    #####################
    ## compute and print the robot motion
    #####################
    robotMove = almath.pose2DInverse(initRobotPosition)*endRobotPosition
    print "virage gauche :", robotMove




#    time.sleep(t)
#    print"turning left"

def doright(angle):
    
    initRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(False))
    
    theta= -angle
    motionProxy.moveTo (0, 0, theta)
#    motionProxy.setWalkTargetVelocity(0, 0, -0.5, 0.01)
    #####################
    ## get robot position after move
    #####################
    endRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(False))

    #####################
    ## compute and print the robot motion
    #####################
    robotMove = almath.pose2DInverse(initRobotPosition)*endRobotPosition
    print "virage droite :", robotMove


    time.sleep(t)
    print"turning right"
    
def doStandUp():
    
    motionProxy.wakeUp()
    motionProxy.setStiffnesses("Body", 1.0)
    time.sleep(t)
    print"standing up"
    
def doStop():
    
    motionProxy.setWalkTargetVelocity(0, 0, 0, Frequency)
    postureProxy.goToPosture("Crouch", 0.3)
    Accelero()
    motionProxy.setStiffnesses("Body", 0.0)
    motionProxy.rest()
    time.sleep(t)
    print"Stopping"


def target_velocity():
    #TARGET VELOCITY
    X = 0.4
    Y = 0.0
    Theta = 0.0
    Frequency =1.0 # max speed
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

    time.sleep(4.0)
    print "Straight Forward"
    print "walk Speed X :",motionProxy.getRobotVelocity()[0]," m/s"
    
    X = -0.4  #backward
    Y = 0.0
    Theta = 0.0
    Frequency =0.0 # low speed
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
    time.sleep(4.0)
    print "Straight Backward"
    print "walk Speed X :",motionProxy.getRobotVelocity()[0]," m/s"

def position_robot():
    
    initRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(False))

    X = 0.3
    Y = 0.1
    Theta = np.pi/2.0
    motionProxy.post.moveTo(X, Y, Theta)
    # wait is useful because with post moveTo is not blocking function
    motionProxy.waitUntilMoveIsFinished()

    #####################
    ## get robot position after move
    #####################
    endRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(False))

    #####################
    ## compute and print the robot motion
    #####################
    robotMove = almath.pose2DInverse(initRobotPosition)*endRobotPosition
    print "Robot Move :", robotMove

def Test_Square_Left_Right():
    print ">>>>>>>>>>> Test du carre"
    print ">>> carre gauche"
    time.sleep(2)
    for i in range(4):
        dorun(6)
        BatteryMemory()
        doleft(np.pi/2)
    time.sleep(2)
    print ">>> carre droite"
    for j in range(4):
        dorun(6)
        BatteryMemory()
        doright(np.pi/2)
    print "fin de test du carre"
    BatteryMemory()

#==============================================================================
# Battery
#==============================================================================
def BatteryMemory():
    percentage = memoryProxy.getData("Device/SubDeviceList/Battery/Current/Sensor/Value") 
    c = memoryProxy.getData ("Device/SubDeviceList/Battery/Charge/Sensor/Value")
    b = memoryProxy.getData ("Device/SubDeviceList/Battery/Charge/Sensor/Status")
    s = []
    t0 = time.time()
    while time.time() - t0 < 2:
        s.append(c)
        c = memoryProxy.getData ("Device/SubDeviceList/Battery/Charge/Sensor/Value")
    #print "Percentage = ", percentage    
    print "Pourcentage de la batterie :", np.mean(s) * 100, "%"
    #print "status =", b
    return np.mean(s) * 100
    
def sumList(a, b):
    result = []
    for i in range(len(a)):
        result.append(a[i] + b[i])
    return result

def close():
    myWidget.close()
    boutton.close()
#    app.exit()
    
def Test_Articulations():
    StiffnessOn(motionProxy)


    # Send NAO to Pose Init
    postureProxy.goToPosture("StandZero", 2.0)
    # Get the Robot Configuration    
    listValStandInit = [memoryProxy.getData("Device/SubDeviceList/HeadYaw/Position/Actuator/Value"),
                        memoryProxy.getData("Device/SubDeviceList/HeadPitch/Position/Actuator/Value"),
                        memoryProxy.getData("Device/SubDeviceList/LShoulderPitch/Position/Actuator/Value"),
                        memoryProxy.getData("Device/SubDeviceList/LShoulderRoll/Position/Actuator/Value"),
                        memoryProxy.getData("Device/SubDeviceList/LElbowYaw/Position/Actuator/Value"),
                        memoryProxy.getData("Device/SubDeviceList/LElbowRoll/Position/Actuator/Value"),
                        memoryProxy.getData("Device/SubDeviceList/LWristYaw/Position/Actuator/Value"),
                        memoryProxy.getData("Device/SubDeviceList/LHand/Position/Actuator/Value"),
                        memoryProxy.getData("Device/SubDeviceList/LKneePitch/Position/Actuator/Value"),
                        0,
                        0]
    
    tab = [[[0,0,0,0,0,0,0,0,120,0,0],[0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0]],
           [[130,0,0,0,0,0,0,0,0,0,0],[-260,0,0,0,0,0,0,0,0,0,0], [130,0,0,0,0,0,0,0,0,0,0]],
           [[0,30,0,0,0,0,0,0,0,0,0],[0,-70,0,0,0,0,0,0,0,0,0], [0,40,0,0,0,0,0,0,0,0,0]],
           [[0,0,120,0,0,0,0,0,0,0,0],[0,0,-240,0,0,0,0,0,0,0,0], [0,0,120,0,0,0,0,0,0,0,0]],
           [[0,0,0,-18,0,0,0,0,0,0,0],[0,0,0,95,0,0,0,0,0,0,0], [0,0,0,-75,0,0,0,0,0,0,0]],
           [[0,0,0,0,120,0,0,0,0,0,0],[0,0,0,0,-240,0,0,0,0,0,0], [0,0,0,0,120,0,0,0,0,0,0]],
           [[0,0,0,0,0,0,-2,0,0,0,0,0],[0,0,0,0,0,90,0,0,0,0,0], [0,0,0,0,0,0,-88,0,0,0,0]],
           [[0,0,0,0,0,0,105,0,0,0,0],[0,0,0,0,0,0,-210,0,0,0,0], [0,0,0,0,0,0,105,0,0,0,0]]]
    
    for i in range(len(tab)):
        for j in range(3):
            listValStandInit = sumList(listValStandInit, tab[i][j])
            configRob(listValStandInit[0], listValStandInit[1], listValStandInit[2], listValStandInit[3], listValStandInit[4], listValStandInit[5], listValStandInit[6], listValStandInit[7], listValStandInit[8], listValStandInit[9], listValStandInit[10])
    time.sleep(2)
    
    postureProxy.goToPosture("Crouch", 2.0)

def FSRPIED():
    print "Pied Gauche" , [memoryProxy.getData("Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value"),
           memoryProxy.getData("Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value"),
           memoryProxy.getData("Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value"),
           memoryProxy.getData("Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value")]
        
    print "Pied Droit" , [memoryProxy.getData("Device/SubDeviceList/RFoot/FSR/FrontLeft/Sensor/Value"),
           memoryProxy.getData("Device/SubDeviceList/RFoot/FSR/FrontRight/Sensor/Value"),
           memoryProxy.getData("Device/SubDeviceList/RFoot/FSR/RearLeft/Sensor/Value"),
           memoryProxy.getData("Device/SubDeviceList/RFoot/FSR/RearRight/Sensor/Value")]
#    print "RFoot Contact :" , memoryProxy.getData("rightFootContact")
#    print "LFoot Contact :" ,memoryProxy.getData ("leftFootContact")
#    print "Foot Contact :", memoryProxy.getData ("footContact")
    
    
class HumanGreeterModule(ALModule):
    """ A simple module able to react
    to facedetection events

    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")

        # Subscribe to the FaceDetected event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("FaceDetected",
            "HumanGreeter",
            "onFaceDetected")
        memory.subscribeToEvent("footContactChanged",
                                "HumanGreeter",
                                "Footcontact")
        
        memory.subscribeToEvent("HandLeftBackTouched",
                                "HumanGreeter",
                                "Maingauche")
        memory.subscribeToEvent("HandRightBackTouched",
                                "HumanGreeter",
                                "MainDroite")
#        memory.subscribeToEvent("BatteryChargeChanged",
#                               "HumanGreeter",
#                               "Battery")
        
    def Battery(self,eventName, percentage,subscriberIdentifier):
        memory.unsubscribeToEvent("BatteryChargeChanged",
                                "HumanGreeter")
        self.tts.say("batterie perdu.")
        self.tts.say(str(percentage)+"%")
        memory.subscribeToEvent("BatteryChargeChanged",
                                "HumanGreeter",
                                "Battery")
        
    def Maingauche(self,*_args):
        memory.unsubscribeToEvent("HandLeftBackTouched",
                                "HumanGreeter")
        self.tts.say('me touche pas lbras gauche')
        memory.subscribeToEvent("HandLeftBackTouched",
                                "HumanGreeter",
                                "Maingauche")
    def MainDroite(self,*_args):
        memory.unsubscribeToEvent("HandRightBackTouched",
                                "HumanGreeter")
        self.tts.say('me touche pas lbras droit')
        memory.subscribeToEvent("HandRightBackTouched",
                                "HumanGreeter",
                                "MainDroite")
    def Footcontact(self,*_args):
        memory.unsubscribeToEvent("footContactChanged",
                                "HumanGreeter")
        
        self.tts.say("j'ai plus les pied sur terre.")
        memory.subscribeToEvent("footContactChanged",
                                "HumanGreeter",
                                "Footcontact")
        
        
    def onFaceDetected(self, *_args):
        """ This will be called each time a face is
        detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("FaceDetected",
            "HumanGreeter")

        self.tts.say("Bonjour")

        # Subscribe again to the event
        memory.subscribeToEvent("FaceDetected",
            "HumanGreeter",
            "onFaceDetected")
        

if __name__== "__main__":
#    doInitialisation()
    #test de la vision du NAO
    try:
        """ Main entry point
    
        """
        parser = OptionParser()
        parser.add_option("--pip",
            help="Parent broker port. The IP address or your robot",
            dest="pip")
        parser.add_option("--pport",
            help="Parent broker port. The port NAOqi is listening to",
            dest="pport",
            type="int")
        parser.set_defaults(
            pip=robotIP,
            pport=9559)
    
        (opts, args_) = parser.parse_args()
        pip   = opts.pip
        pport = opts.pport
        
    #    print pip,pport
        # We need this broker to be able to construct
        # NAOqi modules and subscribe to other modules
        # The broker must stay alive until the program exists
        myBroker = ALBroker("myBroker",
           "0.0.0.0",   # listen to anyone
           0,           # find a free port and use it
           pip,         # parent broker IP
           pport)       # parent broker port
    
    
        # Warning: HumanGreeter must be a global variable
        # The name given to the constructor must be the name of the
        # variable
        global HumanGreeter
        HumanGreeter = HumanGreeterModule("HumanGreeter")
    
    
        audioProxy.post.playFile("/home/nao/music/a.mp3")
        tts.say('''Aubret, fait pas le chaud
                Je te prend en RC tranquille 
                Allé a plus, vas réviser tes partiels gros vier
                on se voit a la soirée a fontenay
        
''') 
        time.sleep(3)
        audioProxy.post.stopAll()      

     
#        dorun(7)  
#     
#        doback()
#        
#        time.sleep(2)
#        FSRPIED()
#        print 'b0 :'
#        b0 = BatteryMemory()
#        #test de capteurs
#        print "Test des capteurs frontaux du robot" 
#        TrySensors()
#        print "Fin capteurs..." 
#
#        print "Test de calcul de vitesse et position"
#        target_velocity()
#        position_robot()
#        print "Fin vitesse / position ..." 
#        
#        print "Test de la fonction de parole du nao"
#        TestTts("Test Micro")
#        time.sleep(1.0)https://www.youtube.com/watch?v=RxabLA7UQ9k
#        print "Fin parole..."
#        
#        print "Test de deplacement du robot"
#        print "trajectoire: carre gauche puis carre droite"
#        Test_Square_Left_Right()
#        print "Fin deplacement..."
#
#        print "Test des articulations Tete / Bras"
#        Test_Articulations()
#        print "Fin articulations..."
#        
#        print "b1 :"
#        b1 = BatteryMemory()
#        print "Fin Batterie..."
#        print "différence",(b0-b1)
#        
#        print "Test d'affichage en temps réel de la vision du robot"
#        doStop()
#        app = QApplication(sys.argv)
#        myWidget = vis.ImageWidget(robotIP, port, CameraID)
#        myWidget.show()
#        boutton= QPushButton()
#        boutton.show()
#        boutton.clicked.connect(close)
#
#        sys.exit(app.exec_())
#        
        print "Fin video..."
        doStop()
        myBroker.shutdown()

        
    except Exception, e:
        print'erreur: ', e
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)
       
#    doStop()
