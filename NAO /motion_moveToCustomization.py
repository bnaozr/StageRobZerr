# -*- encoding: UTF-8 -*- 

'''Move To: Small example to make Nao Move To an Objective '''
'''         With customization '''

import sys
from naoqi import ALProxy


def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def main(robotIP, proxy):
    x     = 0.2
    y     = 0.0
    theta = 0.0

    # This example show customization for the both foot
    # with all the possible gait parameters
    proxy.moveTo(-3*x, y, theta,
        [ ["MaxStepX", 0.10],         # step of 2 cm in front
          ["MaxStepY", 0.16],         # default value
          ["MaxStepTheta", 0.4],      # default value
          ["MaxStepFrequency", 1.0],  # low frequency
          ["StepHeight", 0.01],       # step height of 1 cm
          ["TorsoWx", 0.0],           # default value
          ["TorsoWy", 0.1] ])         # torso bend 0.1 rad in front

    # This example show customization for the both foot
    # with just one gait parameter, in this case, the other
    # parameters are set to the default value
#    motionProxy.moveTo(x, y, theta,
#        [ ["MaxStepX", 0.35],         # step of 2 cm in front
#          ["MaxStepY", 0.16],         # default value
#          ["MaxStepTheta", 0.4],      # default value
#          ["MaxStepFrequency", 0.5],  # low frequency
#          ["StepHeight", 0.001],       # step height of 1 cm
#          ["TorsoWx", 0.0],           # default value
#          ["TorsoWy", 0.1] ])         # torso bend 0.1 rad in front
    
    
    proxy.moveTo(3*x, y, theta,
        [ ["MaxStepX", 0.5],         # step of 2 cm in front
          ["MaxStepY", 0.16],         # default value
          ["MaxStepTheta", 0.4],      # default value
          ["MaxStepFrequency",1],  # low frequency
          ["StepHeight", 0.002],       # step height of 1 cm
          ["TorsoWx", 0.0],           # default value
          ["TorsoWy", 0.1] ])         # torso bend 0.1 rad in front


if __name__ == "__main__":
    robotIp = "172.20.27.244"
    main(robotIp)
