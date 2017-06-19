# -*- coding: utf-8 -*-
import time
import sys
from naoqi import ALProxy
import motion
import select
import vision_definitions
import numpy as np



robotIP = "172.20.28.103"
port = 9559
Frequency = 0.0 #low speed
t=1

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
    audio.setOutputVolume(100)
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
           
#stiffness for real NAO Robot
def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def doInitialisation():
    print(">>>>>> Initialisation")
    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)


#==============================================================================
# Audio
#==============================================================================
def TestTts():
    tts.say("Test Micro")
	
#==============================================================================
# """Vision"""
#==============================================================================

def Test_Detection():

    # Create a proxy to ALFaceDetection
    try:
        faceProxy = ALProxy("ALFaceDetection", robotIP, port)
    except Exception, e:
        print "Error when creating face detection proxy:"
        print str(e)
        exit(1) 


    period = 500
    faceProxy.subscribe("Test_Face", period, 0.0 )
    
    memValue = "FaceDetected"
    # A simple loop that reads the memValue and checks whether faces are detected.
    for i in range(0, 20):
        time.sleep(0.5)
        val = memoryProxy.getData(memValue)

        print ""
        print "*****"
        print ""

        # Check whether we got a valid output.
        if(val and isinstance(val, list) and len(val) >= 2):

            # We detected faces !
            # For each face, we can read its shape info and ID.

            # First Field = TimeStamp.
            timeStamp = val[0]

            # Second Field = array of face_Info's.
            faceInfoArray = val[1]

            try:
                # Browse the faceInfoArray to get info on each detected face.
                for j in range( len(faceInfoArray)-1 ):
                    faceInfo = faceInfoArray[j]
                    # First Field = Shape info.
                    faceShapeInfo = faceInfo[0]

                    # Second Field = Extra info (empty for now).
                    faceExtraInfo = faceInfo[1]

                print "  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
                print "  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])
 
            except Exception, e:
                print "faces detected, but it seems getData is invalid. ALValue ="
                print val
                print "Error msg %s" % (str(e))
        else:
              print "No face detected"

        # Unsubscribe the module.
        faceProxy.unsubscribe("Test_Face")

        print "Detection finished"

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


#==============================================================================
# """Sensors"""
#==============================================================================
def TrySensors():
 
    
    Left = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    Right = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value") 
    print 'Left :', Left
    print 'Right:', Right
    

#==============================================================================
# """Motion"""
#==============================================================================
def dorun():
    
    motionProxy.moveTo (0.4, 0, 0)
    time.sleep(t)
    print"running"
    

def doback():
    
     motionProxy.moveTo (-0.4, 0, 0)
     time.sleep(t)
     print"back"
    
def doleft():
    
    theta= -(np.pi/6)
    motionProxy.moveTo (0, 0, theta)
    time.sleep(t)
    print"turning left"

def doright():
    
    theta= (np.pi/6)
    motionProxy.moveTo (0, 0, theta)
    time.sleep(t)
    print"turning right"
    
def doStandUp():
    
    motionProxy.wakeUp()
    motionProxy.setStiffnesses("Body", 1.0)
    time.sleep(t)
    print"standing up"
    
def doStop():
    

    postureProxy.goToPosture("Crouch", 0.3)
    motionProxy.setStiffnesses("Body", 0.0)
    motionProxy.rest()
    time.sleep(t)
    print"stoping"

def target_velocity():
    #TARGET VELOCITY
    X = 0.8
    Y = 0.0
    Theta = 0.0
    Frequency =1.0 # max speed
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

    time.sleep(4.0)
    print "walk Speed X :",motionProxy.getRobotVelocity()[0]," m/s"
    
    X = -0.5  #backward
    Y = 0.0
    Theta = 0.0
    Frequency =0.0 # low speed
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
    time.sleep(4.0)
    print "walk Speed X :",motionProxy.getRobotVelocity()[0]," m/s"

def position_robot():
    
    initRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))

    X = 0.3
    Y = 0.1
    Theta = np.pi/2.0
    motionProxy.post.moveTo(X, Y, Theta)
    # wait is useful because with post moveTo is not blocking function
    motionProxy.waitUntilMoveIsFinished()

    #####################
    ## get robot position after move
    #####################
    endRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))

    #####################
    ## compute and print the robot motion
    #####################
    robotMove = m.pose2DInverse(initRobotPosition)*endRobotPosition
    print "Robot Move :", robotMove
#
#def shoot():
#    
#     # Activate Whole Body Balancer
#    isEnabled  = True
#    proxy.wbEnable(isEnabled)
#
#    # Legs are constrained fixed
#    stateName  = "Fixed"
#    supportLeg = "Legs"
#    proxy.wbFootState(stateName, supportLeg)
#
#    # Constraint Balance Motion
#    isEnable   = True
#    supportLeg = "Legs"
#    proxy.wbEnableBalanceConstraint(isEnable, supportLeg)
#
#    # Com go to LLeg
#    supportLeg = "LLeg"
#    duration   = 2.0
#    proxy.wbGoToBalance(supportLeg, duration)
#
#    # RLeg is free
#    stateName  = "Free"
#    supportLeg = "RLeg"
#    proxy.wbFootState(stateName, supportLeg)
#
#    # RLeg is optimized
#    effectorName = "RLeg"
#    axisMask     = 63
#    space        = motion.FRAME_ROBOT
#
#
#    # Motion of the RLeg
#    dx      = 0.05                 # translation axis X (meters)
#    dz      = 0.05                 # translation axis Z (meters)
#    dwy     = 5.0*math.pi/180.0    # rotation axis Y (radian)
#
#
#    times   = [2.0, 2.7, 4.5]
#    isAbsolute = False
#
#    targetList = [
#      [-dx, 0.0, dz, 0.0, +dwy, 0.0],
#      [+dx, 0.0, dz, 0.0, 0.0, 0.0],
#      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
#
#    proxy.positionInterpolation(effectorName, space, targetList,
#                                 axisMask, times, isAbsolute)
#
#
#    # Example showing how to Enable Effector Control as an Optimization
#    isActive     = False
#    proxy.wbEnableEffectorOptimization(effectorName, isActive)
#
#    # Com go to LLeg
#    supportLeg = "RLeg"
#    duration   = 2.0
#    proxy.wbGoToBalance(supportLeg, duration)
#
#    # RLeg is free
#    stateName  = "Free"
#    supportLeg = "LLeg"
#    proxy.wbFootState(stateName, supportLeg)
#
#    effectorName = "LLeg"
#    proxy.positionInterpolation(effectorName, space, targetList,
#                                axisMask, times, isAbsolute)
#
#    time.sleep(1.0)
#
#    
if __name__== "__main__":
    doInitialisation()
    #test de la vision du NAO
    try:
        Test_Detection()
        Test_Image()
        #test de capteurs 
        TrySensors()
    

        TestTts()
    #    #test de déplacements
    #    dorun()
    #    doback()
    #    doleft()
    #    doright()
    #    doStandUp()
    except Exception, e:
        print'erreur: ', e
    doStop()