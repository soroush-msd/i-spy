#!/usr/bin/env python

from time import sleep
import rospy
import smach
import smach_ros
import sys
import roslaunch
import actionlib
import darknet_ros_msgs.msg
import darknet_ros_msgs
from cv_bridge import CvBridge
import cv2
import random
from sensor_msgs.msg import Image
import pyttsx3
import speech_recognition as sr


# Make an instance of recognizer for speech recognition
r = sr.Recognizer()

# Make an instance of cvbridge to convert image formats
bridge = CvBridge()
counter = 0

# convert text to speech
def speakText(command):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', 145)     # setting up new voice rate

    if(sys.argv[1] == "f"):
        engine.setProperty('voice', 'english_rp+f3') # change to female voice

    engine.say(command)
    engine.runAndWait()
    data.writelines(command+"\n")

# listen to users' voice, and convert to text
def recog(command):
    with sr.Microphone() as source2:
        print("silence...")
        speakText(command)
        r.adjust_for_ambient_noise(source2,duration=1) # stop for a second to cope with noise
        print("speak...")
        try:
            # wait for user to start speaking for 60 seconds, speak up to 15 seconds
            audio2 = r.listen(source2,timeout=60,phrase_time_limit=15)
            result = r.recognize_google(audio2)
            result = result.lower()
            return result
        except Exception as e:
            speakText("sorry i did not understand that.")
            speakText("i'm going to sleep now.")
            return None

# greet users when they first encounter the agent
def intro():

    speakText("hello hello!")

    # say the agent's name based on requested voice
    if(sys.argv[1] == "m"):
        speakText("my name is James!")
    elif(sys.argv[1] == "f"):
        speakText("my name is Alice!")

    speakText("what is your name?")

    # many different names, sr cannot recognise all of them. so just wait 10 seconds for users to say their name.
    rospy.sleep(10)
    speakText("very nice to meet you!")

    i = 0
    while i == 0:
        guess = recog("would you like to play a game with me?")
        if(("yes" in guess) or ("yeah" in guess) or ("yea" in guess) or ("yep" in guess) or ("correct" in guess) or ("right" in guess) or ("sure" in guess) or ("absolutely" in guess) or ("of course" in guess) or ("definitely" in guess) or ("i'd" in guess) or ("i would" in guess) or ("id" in guess) or ("i" in guess) or ("would" in guess) or ("why" in guess)):
            speakText("yay! ")
            speakText("lets play i spy!")
            i = 1
        else:
            continue

# hard-coded optimisations for sr to improve reliability within the game context
def sr_optimise(guess):
    if(guess == "cop" or guess == "cops"):
        guess = "cup"
    if(guess == "caesars" or guess == "caesarstone"):
        guess = "scissors"
    if(guess == "fort" or guess == "pork" or guess == "fork" or guess == "talk" or guess == "torch" or guess == "fuk" or guess == "foot" or guess == "thought" or guess == "porch" or guess == "fox"):
        guess = "fork"
    if(guess == "butter" or guess == "battle" or guess == "butthole"):
        guess = "bottle"
    if(guess == "spawn" or guess == "spine" or guess == "spain" or guess == "spawned in"):
        guess = "spoon"
    if(guess == "so farm" or guess == "southpine"):
        guess == "cell phone"
    if(guess == "boot" or guess == "boots"):
        guess = "book"
    if(guess == "moss" or guess == "lumos" or guess == "mis" or guess == "mills" or guess == "emmaus" or guess == "maps" or guess == "mounts"):
        guess == "mouse"

    return guess

# state Human: where users interact and play with the robot
class Human(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                            outcomes=['robot_turn', 'exit_success', 'exit_fail'],
                            input_keys=['human_letter', 'robot_guesses', 'asks', 'object_names'],
                            output_keys=['human_letter', 'asks'])

    def execute(self, userdata):
        rospy.loginfo('Executing state HUMAN')

        # if state human is executing for the first time
        if(userdata.asks == ""):
            if(sys.argv[2] == "h"):
                turn = "human"
            elif(sys.argv[2] == "r"):
                turn = "robot"
            elif(sys.argv[2] == "g"):
                turn = ""

            # determine who plays/guesses first
            # if turn is empty, greet and let the robot play first
            if turn == "human":
                speakText("hello welcome back!")
                speakText("now it is my turn to make a guess.")
            elif turn == "robot":
                speakText("hello i am very happy to see you again!")
                speakText("now it is your turn to make a guess.")
            else:
                intro()
                turn = "robot"
                if turn == "robot":
                    speakText("now it is your turn to make a guess.")
            
            # if turn is human, ask user for the first letter of the object
            if turn == "human":
                result = recog("what is the first letter of the object? ")
                if(result == "let her be"):
                    result = "letter b"
                    userdata.human_letter = result[7]
                elif("letter" in result):
                    userdata.human_letter = result[7]
                else:
                    a,b = result.split(' ',1)
                    userdata.human_letter = b

                # if letter is empty, ask them again
                x = 1
                while x == 1:
                    if(userdata.human_letter == ""):
                        result = recog("sorry! could you repeat that again?")
                        userdata.human_letter = result[7]
                    else:
                        x = 0

                # transition to state robot
                speakText("you said: " + userdata.human_letter)
                speakText("please wait while i'm looking around")
                userdata.asks = "h"
                return 'robot_turn'

            # if turn is robot, transition to state robot
            elif turn == "robot":
                userdata.asks = "r"
                speakText("please wait while i'm looking around")
                return 'robot_turn'

            # else exit
            else:
                sys.exit("usage: $ rosrun i-spy stateMachine.py [f]emale/[m]ale [h]uman/[r]obot/[g]reeting")

        # if it is not the first time state human is executing
        else:

            # if turn is human, robot guesses the objects starting with the matching letter given by user
            if(userdata.asks == "h"):

                # if robot could not find an object that matches the desired letter
                if(len(userdata.robot_guesses) == 0):
                    speakText("i'm sorry, i could not find an object that starts with " + userdata.human_letter)
                    correct_object = recog("what is the object?")
                    speakText("oh right! " + correct_object)
                    speakText(" how did i miss that.")
                    return 'exit_fail'

                # if objects were found
                random.shuffle(userdata.robot_guesses)
                for i in range(len(userdata.robot_guesses)):

                    # if the object is one word e.g. keyboard
                    if(userdata.robot_guesses[i][0] == userdata.human_letter):
                        speakText("i am guessing: " + userdata.robot_guesses[i])

                    # if object is 2 words e.g. wine glass
                    else:
                        words = userdata.robot_guesses[i].split()
                        word = words[1]
                        speakText("i am guessing: " + word)
                        speakText("or to be more precise, i am guessing: " + userdata.robot_guesses[i])

                    # ask users if the guess was right
                    guess = recog("did i guess right?")
                    if( ("yes" in guess) or ("yeah" in guess) or ("yea" in guess) or ("yep" in guess) or ("correct" in guess) or ("right" in guess) or ("sure" in guess) or ("absolutely" in guess) or ("of course" in guess) or ("definitely" in guess) or (guess == "you did") or (guess == "udit")):
                        speakText("yay!")
                        speakText("i guessed right!")
                        speakText("thank you for playing with me! i hope to see you again.")
                        return 'exit_success'

                    else:
                        continue

                # if robot fails to guess the correct object after exhausting all possible guesses
                speakText("oh no!")
                speakText("it seems I have run out of guesses")  
                correct_object = recog("i am curious, what is the correct object?")
                speakText("oh right! " + correct_object)
                speakText(" how did i miss that.")
                speakText("i hope i guess right next time we play.")
                return 'exit_fail'

            # if turn is robot, say the chosen letter by robot to user
            elif(userdata.asks == "r"):
                speakText("i choose: " + userdata.robot_guesses[0])
                guess = recog("what is the object that starts with " + userdata.robot_guesses[0] + " ?")

                # if user guesses correctly, exit success
                human_guess = sr_optimise(guess)
                if(human_guess == userdata.object_names[0] and human_guess[0] == userdata.robot_guesses[0]):
                    speakText("good job! The Object is " + userdata.object_names[0])
                    return 'exit_success'
                elif(userdata.object_names[0] in human_guess):
                    speakText("good job! The Object is " + userdata.object_names[0])
                    return 'exit_success'
                    
                # if not, ask them again for the correct object. if success, exit success. else exit fail
                speakText("Oh No! you guessed wrong. ")
                speakText("you guessed " + human_guess)
                speakText("you have one more try")
                guess = recog("what is the object that starts with " + userdata.robot_guesses[0] + " ?")
                human_guess = sr_optimise(guess)

                if(human_guess == userdata.object_names[0] and human_guess[0] == userdata.robot_guesses[0]):
                    speakText("good job! The Object is " + userdata.object_names[0])
                    return 'exit_success'
                elif(userdata.object_names[0] in human_guess):
                    speakText("good job! The Object is " + userdata.object_names[0])
                    return 'exit_success'
                
                speakText("Oh No! you guessed wrong again. ")
                speakText("you guessed " + human_guess)
                speakText("the correct object is " +  userdata.object_names[0])
                return 'exit_fail'
                        

# state robot: representing the robot's behaviour in the gameplay
class Robot(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                            outcomes=['perception', 'robot_responds_human', 'exit_success', 'exit_fail'],
                            input_keys=['human_letter_to_robot', 'object_names', 'robot_response', 'asks'])

    def execute(self, userdata):

        rospy.loginfo('Executing state ROBOT')
        global counter

        # if turn is human and no object is found yet, robot starts to find the correct object
        # transition to state perception
        if(userdata.asks=="h"):
            if((len(userdata.object_names) == 0)):
                if counter < 3:
                    speakText("i am looking for an object that starts with " + userdata.human_letter_to_robot)
                    counter += 1
                    return 'perception'
                else:
                    print("NO object found")
                    return 'exit_fail'
            
            # if turn is human and objects have been found, transition to state human
            elif((len(userdata.object_names) != 0)):
                print("Objects detected are:")
                for i in range(len(userdata.object_names)):
                    if(userdata.object_names[i][0] == userdata.human_letter_to_robot):
                        userdata.robot_response.append( userdata.object_names[i])
                    elif(" " in userdata.object_names[i]):
                        words = userdata.object_names[i].split()
                        word = words[1]
                        if(word[0] == userdata.human_letter_to_robot):
                            userdata.robot_response.append(userdata.object_names[i])
                return 'robot_responds_human'

        # if turn is robot and no object is found yet, transition to state peception
        elif(userdata.asks =="r"):
            if((len(userdata.object_names) == 0)):
                if counter < 3:
                    print("looking around")
                    counter += 1
                    return 'perception'
                else:
                    print("NO object found")
                    return 'exit_fail'

            # if turn is robot and objects have been found, choose a random
            # word that has not been chosen by robot in previous games. 
            # (this is to make the gameplay more interesting by avoiding robot choosing repetivie objects over and over again.)
            elif((len(userdata.object_names) != 0)):                
                file1 = open('/home/kinovagen3/Desktop/objects.txt', 'a+') 
                get_objects = file1.readlines()
                random_word = ""
                if (len(get_objects) != 0):
                    for i in range(len(userdata.object_names)):
                        if((userdata.object_names[i]+"\n") in get_objects):
                            continue
                        else:
                            random_word = userdata.object_names[i]
                            file1.writelines(random_word+"\n")
                            break
                else:
                    random_word = userdata.object_names[0]
                    file1.writelines(random_word+"\n")

                file1.close()

                # when all possible objects have been played, then just choose a random object
                if(random_word == ""):
                    random_word = random.choice(userdata.object_names)
                
                # add the random word as robot's response and transition to state human
                userdata.object_names[0] = random_word
                userdata.robot_response.append(random_word[0])
                return 'robot_responds_human'        


# state perception: to send the image captured by state vision to darknet_ros for object detection
class Perception(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                            outcomes=['objects', 'vision'],
                            input_keys=['human_letter_to_robot', 'objects_detected', 'image_received'],
                            output_keys=['image_received', 'objects_detected'])

    def execute(self, userdata):
        print("Running darknet_ros...")
        rospy.loginfo('Executing state PERCEPTION')

        # if image is not received, tranition to state vision
        if userdata.image_received == 0:
            return 'vision'

        # construct a simpleActionClient and open a connection to the desired action server '/darknet_ros/check_for_objects' from
        # the corresponding action file
        client = actionlib.SimpleActionClient('/darknet_ros/check_for_objects', darknet_ros_msgs.msg.CheckForObjectsAction)
        client.wait_for_server()

        # read the image from the stored location
        cv_message = cv2.imread('/home/kinovagen3/catkin_ws/camera_image_vision.jpeg')

        # change image format from OpenCV to ROS compatible
        image_message = bridge.cv2_to_imgmsg(cv_message, encoding="rgb8")

        # define the goal - checking for objects in the specified image
        goal = darknet_ros_msgs.msg.CheckForObjectsGoal(image=image_message)

        # send the goal to the action server, wait and store the results
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()

        # a not so good solution to make darknet_ros wait more before sending the results to client
        # but it works nevertheless
        i = 0
        while i < 1:
            client.send_goal(goal)
            client.wait_for_result()
            result = client.get_result()
            i = i + 1

        os_list = []

        # weird and unwanted results from darknet_ros - none of these were in the tested image so just ignore them
        # and append the rest of the recognised objects to a list
        for i in range(len(result.bounding_boxes.bounding_boxes)):
            if(result.bounding_boxes.bounding_boxes[i].Class != "diningtable"):
                if(result.bounding_boxes.bounding_boxes[i].Class != "chair"):
                    if(result.bounding_boxes.bounding_boxes[i].Class != "knife"):
                        if(result.bounding_boxes.bounding_boxes[i].Class != "laptop"):
                            if(result.bounding_boxes.bounding_boxes[i].Class != "tvmonitor"):
                                os_list.append(result.bounding_boxes.bounding_boxes[i].Class)

        # remove duplicates
        os_list = list(set(os_list))

        # shuffle for a better gameplay
        random.shuffle(os_list)
        for i in os_list:
            data.writelines(i+"\n")

        # add the objects to userdata and return to state robot
        userdata.objects_detected = list(os_list)
        return 'objects'


# state vision: to launch the robot's camera node and topics to capture its FOV as an image
class Vision(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                            outcomes=['send_vision_to_perception'],
                            input_keys=['image_send'],
                            output_keys=['image_send'])

    def execute(self, userdata):
        rospy.loginfo('Executing state VISION')

        # launch Kinova Gen3's camera node
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/kinovagen3/catkin_ws/src/ros_kortex_vision/launch/kinova_vision.launch"])
        launch.start()

        # wait for the color image
        msg = rospy.wait_for_message("/camera/color/image_raw", Image)

        # change the image format from ROS to OpenCV compatible
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")

        # save the image somewhere and return to state perception
        cv2.imwrite('/home/kinovagen3/catkin_ws/camera_image_vision.jpeg', cv2_img)
        launch.shutdown()
        userdata.image_send = 1
        return 'send_vision_to_perception'


# main: for constructing state machines and specifiying their variables, outcomes, transitions and remappings.
def main():
    
    # initialise ispy node
    rospy.init_node('ISpy_state_machine')

    # Create a SMACH state machine with 2 main outcome based on how the game plays out
    sm = smach.StateMachine(outcomes=['failed', 'successfull'])

    # storing:
    # letter of interest
    sm.userdata.sm_letter = ""

    # list of possible guesses
    sm.userdata.guess_list = []

    # final guess
    sm.userdata.final_guess = []

    # whose turn it is
    sm.userdata.ask = ""

    # image recieved or not
    sm.userdata.image_status = 0
    
    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('HUMAN', Human(), 
                               transitions={'robot_turn' : 'ROBOT' ,
                                            'exit_success' : 'successfull',
                                            'exit_fail' : 'failed'},
                               remapping={'human_letter' : 'sm_letter',
                               "robot_guesses" : "final_guess",
                               "asks" : "ask",
                               "object_names" : "guess_list"})

        smach.StateMachine.add('ROBOT', Robot(), 
                               transitions={'perception' : 'PERCEPTION',
                               "robot_responds_human" : "HUMAN",
                               'exit_success' : 'successfull',
                               'exit_fail' : 'failed'},
                               remapping={"human_letter_to_robot" : "sm_letter",
                               "object_names" : "guess_list",
                               "robot_response" : "final_guess",
                               "asks" : "ask"})

        smach.StateMachine.add('PERCEPTION', Perception(), 
                               transitions={'objects' : 'ROBOT',
                               "vision" : "VISION"},
                               remapping={"human_letter_to_robot" : "sm_letter",
                               "objects_detected" : "guess_list",
                               "image_received" : "image_status"})
        
        smach.StateMachine.add('VISION', Vision(), 
                               transitions={'send_vision_to_perception' : 'PERCEPTION'},
                               remapping={"image_send" : "image_status"})

    # run introspection server to visualise transitions between states during each run
    image_topic = "/camera/color/image_raw"    
    sis = smach_ros.IntrospectionServer('ispy', sm, '/SM_ROOT')
    sis.start()
    outcome = sm.execute()
    sis.stop()


if __name__ == '__main__':

    # opening a file to append human-robot conversations to a file
    data = open('/home/kinovagen3/Desktop/experiment/p18/s18.txt', 'a+')

    # start darknet_ros to overlap I/O with computation (loading weight file)
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/kinovagen3/catkin_ws/src/darknet_ros/darknet_ros/launch/yolo_v3.launch"])
    launch.start()
    main()

    # shutdown darknet_ros
    launch.shutdown()
    data.writelines("**********************"+"\n")
    data.close()
