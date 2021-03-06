// Generated for ALMotion version 1.14

#ifndef ALMOTIONPROXYPOSTHANDLER_H_
#define ALMOTIONPROXYPOSTHANDLER_H_
#include <boost/shared_ptr.hpp>
#include <alvalue/alvalue.h>
#include <string>
#include <vector>

namespace AL
{
class ALProxy;
class ALMotionProxy;

/// <summary>
/// ALMotion provides methods that help make Nao move. It contains commands for manipulating joint angles, joint stiffness, and a higher level API for controling walks.
/// ALMotionPostHandler gives acces to all bound methods of the module, using a thread around each call.
/// Long running tasks can be stopped by calling stop(id) with the id returned by the post.
/// </summary>
/// \ingroup ALProxies
class ALMotionProxyPostHandler
{
  friend class ALMotionProxy;

  protected:
  boost::shared_ptr<ALProxy> fParent;

  private:
  void setParent(boost::shared_ptr<ALProxy> pParent);

  public:
  /// <summary>
  /// ALMotion provides methods that help make Nao move. It contains commands for manipulating joint angles, joint stiffness, and a higher level API for controling walks.
  /// ALMotionPostHandler gives acces to all bound methods of the module, using a thread around each call.
  /// Long running tasks can be stopped by calling stop(id) with the id returned by the post.
  /// </summary>
  ALMotionProxyPostHandler();

  /// <summary>
  /// Interpolates one or multiple joints to a target angle or along timed trajectories. This is a blocking call.
  /// </summary>
  /// <param name="names"> Name or names of joints, chains, \"Body\", \"JointActuators\", \"Joints\" or \"Actuators\". </param>
  /// <param name="angleLists"> An angle, list of angles or list of list of angles in radians </param>
  /// <param name="timeLists"> A time, list of times or list of list of times in seconds </param>
  /// <param name="isAbsolute"> If true, the movement is described in absolute angles, else the angles are relative to the current angle. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int angleInterpolation(const AL::ALValue& names, const AL::ALValue& angleLists, const AL::ALValue& timeLists, const bool& isAbsolute);
  /// <summary>
  /// Interpolates a sequence of timed angles for several motors using bezier control points. This is a blocking call.
  /// </summary>
  /// <param name="jointNames"> A vector of joint names </param>
  /// <param name="times"> An ragged ALValue matrix of floats. Each line corresponding to a motor, and column element to a control point. </param>
  /// <param name="controlPoints"> An ALValue array of arrays each containing [float angle, Handle1, Handle2], where Handle is [int InterpolationType, float dAngle, float dTime] descibing the handle offsets relative to the angle and time of the point. The first bezier param describes the handle that controls the curve preceeding the point, the second describes the curve following the point. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int angleInterpolationBezier(const std::vector<std::string>& jointNames, const AL::ALValue& times, const AL::ALValue& controlPoints);
  /// <summary>
  /// Interpolates one or multiple joints to a target angle, using a fraction of max speed. Only one target angle is allowed for each joint. This is a blocking call.
  /// </summary>
  /// <param name="names"> Name or names of joints, chains, \"Body\", \"JointActuators\", \"Joints\" or \"Actuators\". </param>
  /// <param name="targetAngles"> An angle, or list of angles in radians </param>
  /// <param name="maxSpeedFraction"> A fraction. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int angleInterpolationWithSpeed(const AL::ALValue& names, const AL::ALValue& targetAngles, const float& maxSpeedFraction);
  /// <summary>
  /// Changes Angles. This is a non-blocking call.
  /// </summary>
  /// <param name="names"> The name or names of joints, chains, \"Body\", \"JointActuators\", \"Joints\" or \"Actuators\". </param>
  /// <param name="changes"> One or more changes in radians </param>
  /// <param name="fractionMaxSpeed"> The fraction of maximum speed to use </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int changeAngles(const AL::ALValue& names, const AL::ALValue& changes, const float& fractionMaxSpeed);
  /// <summary>
  /// Creates a move of an end effector in cartesian space. This is a non-blocking call.
  /// </summary>
  /// <param name="effectorName"> Name of the effector. </param>
  /// <param name="space"> Task space {FRAME_TORSO = 0, FRAME_WORLD = 1, FRAME_ROBOT = 2}. </param>
  /// <param name="positionChange"> 6D position change array (xd, yd, zd, wxd, wyd, wzd) in meters and radians </param>
  /// <param name="fractionMaxSpeed"> The fraction of maximum speed to use </param>
  /// <param name="axisMask"> Axis mask. True for axes that you wish to control. e.g. 7 for position only, 56 for rotation only and 63 for both </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int changePosition(const std::string& effectorName, const int& space, const std::vector<float>& positionChange, const float& fractionMaxSpeed, const int& axisMask);
  /// <summary>
  /// Moves an end-effector to the given position and orientation transform. This is a non-blocking call.
  /// </summary>
  /// <param name="chainName"> Name of the chain. Could be: \"Head\", \"LArm\",\"RArm\", \"LLeg\", \"RLeg\", \"Torso\" </param>
  /// <param name="space"> Task space {FRAME_TORSO = 0, FRAME_WORLD = 1, FRAME_ROBOT = 2}. </param>
  /// <param name="transform"> Transform arrays </param>
  /// <param name="fractionMaxSpeed"> The fraction of maximum speed to use </param>
  /// <param name="axisMask"> Axis mask. True for axes that you wish to control. e.g. 7 for position only, 56 for rotation only and 63 for both </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int changeTransform(const std::string& chainName, const int& space, const std::vector<float>& transform, const float& fractionMaxSpeed, const int& axisMask);
  /// <summary>
  /// NAO stiffens the motors of desired hand. Then, he closes the hand, then cuts motor current to conserve energy. This is a blocking call.
  /// </summary>
  /// <param name="handName"> The name of the hand. Could be: \"RHand\" or \"LHand\" </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int closeHand(const std::string& handName);
  /// <summary>
  /// Exits and unregisters the module.
  /// </summary>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int exit();
  /// <summary>
  /// Kills all tasks.
  /// </summary>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int killAll();
  /// <summary>
  /// Emergency Stop on Move task: This method will end the move task brutally, without attempting to return to a balanced state. The robot could easily fall.
  /// </summary>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int killMove();
  /// <summary>
  /// Kills all tasks that use any of the resources given. Only motion API's' blocking call takes resources and can be killed. Use getBodyNames(\"Body\") to have the list of the available joint for your robot.
  /// </summary>
  /// <param name="resourceNames"> A vector of resource joint names </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int killTasksUsingResources(const std::vector<std::string>& resourceNames);
  /// <summary>
  /// DEPRECATED. Use killMove function instead.
  /// </summary>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int killWalk();
  /// <summary>
  /// Makes the robot move at the given velocity. This is a non-blocking call.
  /// </summary>
  /// <param name="x"> The velocity along x axis [m.s-1]. </param>
  /// <param name="y"> The velocity along y axis [m.s-1]. </param>
  /// <param name="theta"> The velocity around z axis [rd.s-1]. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int move(const float& x, const float& y, const float& theta);
  /// <summary>
  /// Makes the robot move at the given velocity. This is a non-blocking call.
  /// </summary>
  /// <param name="x"> The velocity along x axis [m.s-1]. </param>
  /// <param name="y"> The velocity along y axis [m.s-1]. </param>
  /// <param name="theta"> The velocity around z axis [rd.s-1]. </param>
  /// <param name="moveConfig"> An ALValue with custom move configuration. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int move(const float& x, const float& y, const float& theta, const AL::ALValue& moveConfig);
  /// <summary>
  /// Initialize the move process. Check the robot pose and take a right posture. This is blocking called.
  /// </summary>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int moveInit();
  /// <summary>
  /// Makes the robot move at the given position. This is a non-blocking call.
  /// </summary>
  /// <param name="x"> The position along x axis [m.s-1]. </param>
  /// <param name="y"> The position along y axis [m.s-1]. </param>
  /// <param name="theta"> The position around z axis [rd.s-1]. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int moveTo(const float& x, const float& y, const float& theta);
  /// <summary>
  /// Makes the robot move at the given position. This is a non-blocking call.
  /// </summary>
  /// <param name="x"> The position along x axis [m.s-1]. </param>
  /// <param name="y"> The position along y axis [m.s-1]. </param>
  /// <param name="theta"> The position around z axis [rd.s-1]. </param>
  /// <param name="moveConfig"> An ALValue with custom move configuration. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int moveTo(const float& x, const float& y, const float& theta, const AL::ALValue& moveConfig);
  /// <summary>
  /// Makes Nao move to the given relative Position. This is a blocking call.
  /// </summary>
  /// <param name="controlPoint"> An ALValue with all the control point in NAO SPACE[[x1,y1,theta1], ..., [xN,yN,thetaN] </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int moveTo(const AL::ALValue& controlPoint);
  /// <summary>
  /// Makes Nao move to the given relative Position. This is a blocking call.
  /// </summary>
  /// <param name="controlPoint"> An ALValue with all the control point in NAO SPACE[[x1,y1,theta1], ..., [xN,yN,thetaN] </param>
  /// <param name="feetGaitConfig"> An ALValue with the custom gait configuration for both feet </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int moveTo(const AL::ALValue& controlPoint, const AL::ALValue& feetGaitConfig);
  /// <summary>
  /// Makes the robot move at the given normalized velocity. This is a non-blocking call.
  /// </summary>
  /// <param name="x"> The normalized velocity along x axis (between -1 and 1). </param>
  /// <param name="y"> The normalized velocity along y axis (between -1 and 1). </param>
  /// <param name="theta"> The normalized velocity around z axis (between -1 and 1). </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int moveToward(const float& x, const float& y, const float& theta);
  /// <summary>
  /// Makes the robot move at the given normalized velocity. This is a non-blocking call.
  /// </summary>
  /// <param name="x"> The normalized velocity along x axis (between -1 and 1). </param>
  /// <param name="y"> The normalized velocity along y axis (between -1 and 1). </param>
  /// <param name="theta"> The normalized velocity around z axis (between -1 and 1). </param>
  /// <param name="moveConfig"> An ALValue with custom move configuration. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int moveToward(const float& x, const float& y, const float& theta, const AL::ALValue& moveConfig);
  /// <summary>
  /// NAO stiffens the motors of desired hand. Then, he opens the hand, then cuts motor current to conserve energy. This is a blocking call.
  /// </summary>
  /// <param name="handName"> The name of the hand. Could be: \"RHand or \"LHand\" </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int openHand(const std::string& handName);
  /// <summary>
  /// Moves an end-effector to the given position and orientation over time. This is a blocking call.
  /// </summary>
  /// <param name="chainName"> Name of the chain. Could be: \"Head\", \"LArm\", \"RArm\", \"LLeg\", \"RLeg\", \"Torso\" </param>
  /// <param name="space"> Task space {FRAME_TORSO = 0, FRAME_WORLD = 1, FRAME_ROBOT = 2}. </param>
  /// <param name="path"> Vector of 6D position arrays (x,y,z,wx,wy,wz) in meters and radians </param>
  /// <param name="axisMask"> Axis mask. True for axes that you wish to control. e.g. 7 for position only, 56 for rotation only and 63 for both </param>
  /// <param name="durations"> Vector of times in seconds corresponding to the path points </param>
  /// <param name="isAbsolute"> If true, the movement is absolute else relative </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int positionInterpolation(const std::string& chainName, const int& space, const AL::ALValue& path, const int& axisMask, const AL::ALValue& durations, const bool& isAbsolute);
  /// <summary>
  /// Moves end-effectors to the given positions and orientations over time. This is a blocking call.
  /// </summary>
  /// <param name="effectorNames"> Vector of chain names. Could be: \"Head\", \"LArm\", \"RArm\", \"LLeg\", \"RLeg\", \"Torso\" </param>
  /// <param name="taskSpaceForAllPaths"> Task space {FRAME_TORSO = 0, FRAME_WORLD = 1, FRAME_ROBOT = 2}. </param>
  /// <param name="paths"> Vector of 6D position arrays (x,y,z,wx,wy,wz) in meters and radians </param>
  /// <param name="axisMasks"> Vector of Axis Masks. True for axes that you wish to control. e.g. 7 for position only, 56 for rotation only and 63 for both </param>
  /// <param name="relativeTimes"> Vector of times in seconds corresponding to the path points </param>
  /// <param name="isAbsolute"> If true, the movement is absolute else relative </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int positionInterpolations(const std::vector<std::string>& effectorNames, const int& taskSpaceForAllPaths, const AL::ALValue& paths, const AL::ALValue& axisMasks, const AL::ALValue& relativeTimes, const bool& isAbsolute);
  /// <summary>
  /// The robot will rest: go to a relax and safe position and set Motor OFF
  /// </summary>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int rest();
  /// <summary>
  /// Sets angles. This is a non-blocking call.
  /// </summary>
  /// <param name="names"> The name or names of joints, chains, \"Body\", \"JointActuators\", \"Joints\" or \"Actuators\". </param>
  /// <param name="angles"> One or more angles in radians </param>
  /// <param name="fractionMaxSpeed"> The fraction of maximum speed to use </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int setAngles(const AL::ALValue& names, const AL::ALValue& angles, const float& fractionMaxSpeed);
  /// <summary>
  /// Enable The fall manager protection for the robot. When a fall is detected the robot adopt a joint configuration to protect himself and cut the stiffness.
    ///
    /// . An memory event called \"robotHasFallen\" is generated when the fallManager have been activated.
  /// </summary>
  /// <param name="pEnable"> Activate or disactivate the smart stiffness. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int setFallManagerEnabled(const bool& pEnable);
  /// <summary>
  /// Makes Nao do foot step planner. This is a non-blocking call.
  /// </summary>
  /// <param name="legName"> name of the leg to move('LLeg'or 'RLeg') </param>
  /// <param name="footSteps"> [x, y, theta], [Position along X/Y, Orientation round Z axis] of the leg relative to the other Leg in [meters, meters, radians]. Must be less than [MaxStepX, MaxStepY, MaxStepTheta] </param>
  /// <param name="timeList"> time list of each foot step </param>
  /// <param name="clearExisting"> Clear existing foot steps. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int setFootSteps(const std::vector<std::string>& legName, const AL::ALValue& footSteps, const std::vector<float>& timeList, const bool& clearExisting);
  /// <summary>
  /// Makes Nao do foot step planner with speed. This is a blocking call.
  /// </summary>
  /// <param name="legName"> name of the leg to move('LLeg'or 'RLeg') </param>
  /// <param name="footSteps"> [x, y, theta], [Position along X/Y, Orientation round Z axis] of the leg relative to the other Leg in [meters, meters, radians]. Must be less than [MaxStepX, MaxStepY, MaxStepTheta] </param>
  /// <param name="fractionMaxSpeed"> speed of each foot step. Must be between 0 and 1. </param>
  /// <param name="clearExisting"> Clear existing foot steps. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int setFootStepsWithSpeed(const std::vector<std::string>& legName, const AL::ALValue& footSteps, const std::vector<float>& fractionMaxSpeed, const bool& clearExisting);
  /// <summary>
  /// Internal Use.
  /// </summary>
  /// <param name="config"> Internal: An array of ALValues [i][0]: name, [i][1]: value </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int setMotionConfig(const AL::ALValue& config);
  /// <summary>
  /// Moves an end-effector to the given position and orientation. This is a non-blocking call.
  /// </summary>
  /// <param name="chainName"> Name of the chain. Could be: \"Head\", \"LArm\",\"RArm\", \"LLeg\", \"RLeg\", \"Torso\" </param>
  /// <param name="space"> Task space {FRAME_TORSO = 0, FRAME_WORLD = 1, FRAME_ROBOT = 2}. </param>
  /// <param name="position"> 6D position array (x,y,z,wx,wy,wz) in meters and radians </param>
  /// <param name="fractionMaxSpeed"> The fraction of maximum speed to use </param>
  /// <param name="axisMask"> Axis mask. True for axes that you wish to control. e.g. 7 for position only, 56 for rotation only and 63 for both </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int setPosition(const std::string& chainName, const int& space, const std::vector<float>& position, const float& fractionMaxSpeed, const int& axisMask);
  /// <summary>
  /// Enable Smart Stiffness for all the joints (True by default), the update take one motion cycle for updating. The smart Stiffness is a gestion of joint maximum torque. More description is available on the red documentation of ALMotion module.
  /// </summary>
  /// <param name="pEnable"> Activate or disactivate the smart stiffness. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int setSmartStiffnessEnabled(const bool& pEnable);
  /// <summary>
  /// Sets the stiffness of one or more joints. This is a non-blocking call.
  /// </summary>
  /// <param name="names"> Names of joints, chains, \"Body\", \"JointActuators\", \"Joints\" or \"Actuators\". </param>
  /// <param name="stiffnesses"> One or more stiffnesses between zero and one. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int setStiffnesses(const AL::ALValue& names, const AL::ALValue& stiffnesses);
  /// <summary>
  /// Moves an end-effector to the given position and orientation transform. This is a non-blocking call.
  /// </summary>
  /// <param name="chainName"> Name of the chain. Could be: \"Head\", \"LArm\",\"RArm\", \"LLeg\", \"RLeg\", \"Torso\" </param>
  /// <param name="space"> Task space {FRAME_TORSO = 0, FRAME_WORLD = 1, FRAME_ROBOT = 2}. </param>
  /// <param name="transform"> Transform arrays </param>
  /// <param name="fractionMaxSpeed"> The fraction of maximum speed to use </param>
  /// <param name="axisMask"> Axis mask. True for axes that you wish to control. e.g. 7 for position only, 56 for rotation only and 63 for both </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int setTransform(const std::string& chainName, const int& space, const std::vector<float>& transform, const float& fractionMaxSpeed, const int& axisMask);
  /// <summary>
  /// DEPRECATED Function. PLease use setWalkArmsEnabled().
  /// </summary>
  /// <param name="leftArmEnable"> if true Left Arm motions are controlled by the Walk Task </param>
  /// <param name="rightArmEnable"> if true Right Arm mMotions are controlled by the Walk Task </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int setWalkArmsEnable(const bool& leftArmEnable, const bool& rightArmEnable);
  /// <summary>
  /// Sets if Arms Motions are enabled during the Walk Process.
  /// </summary>
  /// <param name="leftArmEnabled"> if true Left Arm motions are controlled by the Walk Task </param>
  /// <param name="rightArmEnabled"> if true Right Arm mMotions are controlled by the Walk Task </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int setWalkArmsEnabled(const bool& leftArmEnabled, const bool& rightArmEnabled);
  /// <summary>
  /// Makes Nao walk at the given velocity. This is a non-blocking call.
  /// </summary>
  /// <param name="x"> Fraction of MaxStepX. Use negative for backwards. [-1.0 to 1.0] </param>
  /// <param name="y"> Fraction of MaxStepY. Use negative for right. [-1.0 to 1.0] </param>
  /// <param name="theta"> Fraction of MaxStepTheta. Use negative for clockwise [-1.0 to 1.0] </param>
  /// <param name="frequency"> Fraction of MaxStepFrequency [0.0 to 1.0] </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int setWalkTargetVelocity(const float& x, const float& y, const float& theta, const float& frequency);
  /// <summary>
  /// Makes Nao walk at the given velocity. This is a non-blocking call.
  /// </summary>
  /// <param name="x"> Fraction of MaxStepX. Use negative for backwards. [-1.0 to 1.0] </param>
  /// <param name="y"> Fraction of MaxStepY. Use negative for right. [-1.0 to 1.0] </param>
  /// <param name="theta"> Fraction of MaxStepTheta. Use negative for clockwise [-1.0 to 1.0] </param>
  /// <param name="frequency"> Fraction of MaxStepFrequency [0.0 to 1.0] </param>
  /// <param name="feetGaitConfig"> An ALValue with the custom gait configuration for both feet </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int setWalkTargetVelocity(const float& x, const float& y, const float& theta, const float& frequency, const AL::ALValue& feetGaitConfig);
  /// <summary>
  /// Makes Nao walk at the given velocity. This is a non-blocking call.
  /// </summary>
  /// <param name="x"> Fraction of MaxStepX. Use negative for backwards. [-1.0 to 1.0] </param>
  /// <param name="y"> Fraction of MaxStepY. Use negative for right. [-1.0 to 1.0] </param>
  /// <param name="theta"> Fraction of MaxStepTheta. Use negative for clockwise [-1.0 to 1.0] </param>
  /// <param name="frequency"> Fraction of MaxStepFrequency [0.0 to 1.0] </param>
  /// <param name="leftFootMoveConfig"> An ALValue with custom move configuration for the left foot </param>
  /// <param name="rightFootMoveConfig"> An ALValue with custom move configuration for the right foot </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int setWalkTargetVelocity(const float& x, const float& y, const float& theta, const float& frequency, const AL::ALValue& leftFootMoveConfig, const AL::ALValue& rightFootMoveConfig);
  /// <summary>
  /// Interpolates one or multiple joints to a target stiffness or along timed trajectories of stiffness. This is a blocking call.
  /// </summary>
  /// <param name="names"> Name or names of joints, chains, \"Body\", \"JointActuators\", \"Joints\" or \"Actuators\". </param>
  /// <param name="stiffnessLists"> An stiffness, list of stiffnesses or list of list of stiffnesses </param>
  /// <param name="timeLists"> A time, list of times or list of list of times. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int stiffnessInterpolation(const AL::ALValue& names, const AL::ALValue& stiffnessLists, const AL::ALValue& timeLists);
  /// <summary>
  /// returns true if the method is currently running
  /// </summary>
  /// <param name="id"> the ID of the method to wait for </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int stop(const int& id);
  /// <summary>
  /// Stop Move task safely as fast as possible. The move task is ended less brutally than killMove but more quickly than move(0.0, 0.0, 0.0).
    ///
    /// This is a blocking call.
  /// </summary>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int stopMove();
  /// <summary>
  /// DEPRECATED. Use stopMove function instead.
  /// </summary>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int stopWalk();
  /// <summary>
  /// Moves an end-effector to the given position and orientation over time using homogenous transforms to describe the positions or changes. This is a blocking call.
  /// </summary>
  /// <param name="chainName"> Name of the chain. Could be: \"Head\", \"LArm\",\"RArm\", \"LLeg\", \"RLeg\", \"Torso\" </param>
  /// <param name="space"> Task space {FRAME_TORSO = 0, FRAME_WORLD = 1, FRAME_ROBOT = 2}. </param>
  /// <param name="path"> Vector of Transform arrays </param>
  /// <param name="axisMask"> Axis mask. True for axes that you wish to control. e.g. 7 for position only, 56 for rotation only and 63 for both </param>
  /// <param name="duration"> Vector of times in seconds corresponding to the path points </param>
  /// <param name="isAbsolute"> If true, the movement is absolute else relative </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int transformInterpolation(const std::string& chainName, const int& space, const AL::ALValue& path, const int& axisMask, const AL::ALValue& duration, const bool& isAbsolute);
  /// <summary>
  /// Moves end-effector to the given transforms over time. This is a blocking call.
  /// </summary>
  /// <param name="effectorNames"> Vector of chain names. Could be: \"Head\", \"LArm\", \"RArm\", \"LLeg\", \"RLeg\", \"Torso\" </param>
  /// <param name="taskSpaceForAllPaths"> Task space {FRAME_TORSO = 0, FRAME_WORLD = 1, FRAME_ROBOT = 2}. </param>
  /// <param name="paths"> Vector of transforms arrays. </param>
  /// <param name="axisMasks"> Vector of Axis Masks. True for axes that you wish to control. e.g. 7 for position only, 56 for rotation only and 63 for both </param>
  /// <param name="relativeTimes"> Vector of times in seconds corresponding to the path points </param>
  /// <param name="isAbsolute"> If true, the movement is absolute else relative </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int transformInterpolations(const std::vector<std::string>& effectorNames, const int& taskSpaceForAllPaths, const AL::ALValue& paths, const AL::ALValue& axisMasks, const AL::ALValue& relativeTimes, const bool& isAbsolute);
  /// <summary>
  /// Update the target to follow by the head of NAO.
    ///
    /// This function is mainly use by the tracker modules.
  /// </summary>
  /// <param name="pTargetPositionWy"> The target position wy in FRAME_ROBOT </param>
  /// <param name="pTargetPositionWz"> The target position wz in  FRAME_ROBOT </param>
  /// <param name="pTimeSinceDetectionMs"> The time in Ms since the target was detected </param>
  /// <param name="pUseOfWholeBody"> If true, the target is follow in cartesian space by the Head with whole Body constraints. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int updateTrackerTarget(const float& pTargetPositionWy, const float& pTargetPositionWz, const int& pTimeSinceDetectionMs, const bool& pUseOfWholeBody);
  /// <summary>
  /// Waits until the move process is finished: This method can be used to block your script/code execution until the move task is totally finished.
  /// </summary>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int waitUntilMoveIsFinished();
  /// <summary>
  /// DEPRECATED. Use waitUntilMoveIsFinished function instead.
  /// </summary>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int waitUntilWalkIsFinished();
  /// <summary>
  /// The robot will wake up: set Motor ON and go to initial position if needed
  /// </summary>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int wakeUp();
  /// <summary>
  /// DEPRECATED. Use moveInit function instead.
  /// </summary>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int walkInit();
  /// <summary>
  /// DEPRECATED. Use moveTo() function instead.
  /// </summary>
  /// <param name="x"> Distance along the X axis in meters. </param>
  /// <param name="y"> Distance along the Y axis in meters. </param>
  /// <param name="theta"> Rotation around the Z axis in radians [-3.1415 to 3.1415]. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int walkTo(const float& x, const float& y, const float& theta);
  /// <summary>
  /// DEPRECATED. Use moveTo() function instead.
  /// </summary>
  /// <param name="x"> Distance along the X axis in meters. </param>
  /// <param name="y"> Distance along the Y axis in meters. </param>
  /// <param name="theta"> Rotation around the Z axis in radians [-3.1415 to 3.1415]. </param>
  /// <param name="feetGaitConfig"> An ALValue with the custom gait configuration for both feet. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int walkTo(const float& x, const float& y, const float& theta, const AL::ALValue& feetGaitConfig);
  /// <summary>
  /// DEPRECATED. Use moveTo() function instead.
  /// </summary>
  /// <param name="controlPoint"> An ALValue with all the control point in NAO SPACE[[x1,y1,theta1], ..., [xN,yN,thetaN] </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int walkTo(const AL::ALValue& controlPoint);
  /// <summary>
  /// DEPRECATED. Use moveTo() function instead.
  /// </summary>
  /// <param name="controlPoint"> An ALValue with all the control point in NAO SPACE[[x1,y1,theta1], ..., [xN,yN,thetaN] </param>
  /// <param name="feetGaitConfig"> An ALValue with the custom gait configuration for both feet </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int walkTo(const AL::ALValue& controlPoint, const AL::ALValue& feetGaitConfig);
  /// <summary>
  /// UserFriendly Whole Body API: enable Whole Body Balancer. It's a Generalized Inverse Kinematics which deals with cartesian control, balance, redundancy and task priority. The main goal is to generate and stabilized consistent motions without precomputed trajectories and adapt nao's behaviour to the situation. The generalized inverse kinematic problem takes in account equality constraints (keep foot fix), inequality constraints (joint limits, balance, ...) and quadratic minimization (cartesian / articular desired trajectories). We solve each step a quadratic programming on the robot.
  /// </summary>
  /// <param name="isEnabled"> Active / Disactive Whole Body Balancer. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int wbEnable(const bool& isEnabled);
  /// <summary>
  /// UserFriendly Whole Body API: enable to keep balance in support polygon.
  /// </summary>
  /// <param name="isEnable"> Enable Nao to keep balance. </param>
  /// <param name="supportLeg"> Name of the support leg: \"Legs\", \"LLeg\", \"RLeg\". </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int wbEnableBalanceConstraint(const bool& isEnable, const std::string& supportLeg);
  /// <summary>
  /// UserFriendly Whole Body API: enable whole body cartesian control of an effector.
  /// </summary>
  /// <param name="effectorName"> Name of the effector : \"Head\", \"LArm\" or \"RArm\". Nao goes to posture init. He manages his balance and keep foot fix. \"Head\" is controlled in rotation. \"LArm\" and \"RArm\" are controlled in position. </param>
  /// <param name="isEnabled"> Active / Disactive Effector Control. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int wbEnableEffectorControl(const std::string& effectorName, const bool& isEnabled);
  /// <summary>
  /// Advanced Whole Body API: enable to control an effector as an optimization.
  /// </summary>
  /// <param name="effectorName"> Name of the effector : \"All\", \"Arms\", \"Legs\", \"Head\", \"LArm\", \"RArm\", \"LLeg\", \"RLeg\", \"Torso\", \"Com\". </param>
  /// <param name="isActive"> if true, the effector control is taken in acount in the optimization criteria. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int wbEnableEffectorOptimization(const std::string& effectorName, const bool& isActive);
  /// <summary>
  /// UserFriendly Whole Body API: set the foot state: fixed foot, constrained in a plane or free.
  /// </summary>
  /// <param name="stateName"> Name of the foot state. \"Fixed\" set the foot fixed. \"Plane\" constrained the Foot in the plane. \"Free\" set the foot free. </param>
  /// <param name="supportLeg"> Name of the foot. \"LLeg\", \"RLeg\" or \"Legs\". </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int wbFootState(const std::string& stateName, const std::string& supportLeg);
  /// <summary>
  /// Advanced Whole Body API: \"Com\" go to a desired support polygon. This is a blocking call.
  /// </summary>
  /// <param name="supportLeg"> Name of the support leg: \"Legs\", \"LLeg\", \"RLeg\". </param>
  /// <param name="duration"> Time in seconds. Must be upper 0.5 s. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int wbGoToBalance(const std::string& supportLeg, const float& duration);
  /// <summary>
  /// UserFriendly Whole Body API: set new target for controlled effector. This is a non-blocking call.
  /// </summary>
  /// <param name="effectorName"> Name of the effector : \"Head\", \"LArm\" or \"RArm\". Nao goes to posture init. He manages his balance and keep foot fix. \"Head\" is controlled in rotation. \"LArm\" and \"RArm\" are controlled in position. </param>
  /// <param name="targetCoordinate"> \"Head\" is controlled in rotation (WX, WY, WZ). \"LArm\" and \"RArm\" are controlled in position (X, Y, Z). TargetCoordinate must be absolute and expressed in FRAME_ROBOT. If the desired position/orientation is unfeasible, target is resize to the nearest feasible motion. </param>
  /// <returns> brokerTaskID : The ID of the task assigned to it by the broker.</returns>
  int wbSetEffectorControl(const std::string& effectorName, const AL::ALValue& targetCoordinate);
};

}
#endif // ALMOTIONPROXYPOSTHANDLER_H_

