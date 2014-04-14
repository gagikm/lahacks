################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import lightblue
from lightblue import *
s = socket()
debug = True
# Best monkey patching ever
if debug:
    s.send = lambda x: x
    s.connect = lambda x: x
s.connect(("00:13:12:25:49:79",1))

 

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"
        self.clamp = 0

    def on_connect(self, controller):
        print "Connected"
        # Enable gestures
#        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
 #       controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
  #      controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
   #     controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        start = time.time()
        frame = controller.frame()
        if(len(frame.hands)!=0 and len(frame.hands)!=2):
            # Get the most recent frame and report some basic information
            #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
            #      frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

            if not frame.hands.is_empty:
                # Get the first hand
                hand = frame.hands[0]

                MIN_SPEED=20.0
                MAX_SPEED=80.0
                
                #IMPORTANT: Face green light toward you.
                left_right_velocity = hand.palm_velocity[0] #right:+ #left:- #
                if abs(left_right_velocity) < MIN_SPEED or abs(left_right_velocity) > 500:
                    adjusted_lrv = 0.0
                elif(left_right_velocity >= MAX_SPEED):
                    adjusted_lrv = 1.0
                elif (left_right_velocity <= -MAX_SPEED):
                    adjusted_lrv = -1.0
                else:
                    adjusted_lrv = left_right_velocity / MAX_SPEED #adjusted lrv 
                if adjusted_lrv != 0:
                    motor4="4%f\n" % (adjusted_lrv)
                    s.send(motor4)  #//////////////////////////////////////////////////////////////////////// LEFT-RIGHT
                    print motor4

                # up is harder than down
                # moving up + down should have higher min speed?
                up_down_velocity = hand.palm_velocity[1] #up:+ #down:-
                if abs(up_down_velocity) < MIN_SPEED or abs(up_down_velocity) > 500:
                    adjusted_udv = 0.0
                elif(up_down_velocity >= MAX_SPEED):
                    adjusted_udv = 1.0
                elif(up_down_velocity <= -MAX_SPEED):
                    adjusted_udv = -1.0
                else:
                    adjusted_udv = up_down_velocity / MAX_SPEED     #adjusted udv
                if adjusted_udv != 0:
                    #motor2="2%f\n" % (adjusted_udv * (-1/4.0)) #might be positive !~!~!~!~!~!~!~!~~!~!~!~!~!
                    motor2="2%f\n" % (adjusted_udv * (3/4.0))
                    s.send(motor2)  #//////////////////////////////////////////////////////////////////////// UP-DOWN
                    print motor2

                forward_back_velocity = -hand.palm_velocity[2] #back:- #frwd:+
                #print "forward back: %f" % forward_back_velocity
                if abs(forward_back_velocity) < MIN_SPEED or abs(forward_back_velocity) > 500:
                    adjusted_fbv = 0.0
                elif(forward_back_velocity >= MAX_SPEED):
                    adjusted_fbv = 1.0;
                elif(forward_back_velocity <= -MAX_SPEED):
                    adjusted_fbv = -1.0;
                else:
                    adjusted_fbv = forward_back_velocity / MAX_SPEED #adjusted fbv
                if adjusted_fbv != 0:
                    #motor2="2%f\n" % (adjusted_fbv * (1.0/4.0)) #may not work! probably will ~!~!~!~!~!~~~!!~
                    motor3="3%f\n" % (adjusted_fbv * (3.0/4.0))
                    s.send(motor3)  #//////////////////////////////////////////////////////////////////////// FRWD-BACK
                    print motor3



                # Check if the hand has any fingers
                fingers = hand.fingers
                CLAMP_TIME = 30
                if (len(fingers))>1:
                    # Calculate the hand's average finger tip position
                    self.clamp=max(0, self.clamp - 1)
                    motor0 = "0%f\n" % (-0.5) #////////////////////////////////////////////////////////// OPEN
                    if self.clamp > 0:
                        s.send(motor0)
                        print motor0
                else:
                    self.clamp=min(CLAMP_TIME, self.clamp + 1)
                    motor0="0%f\n" % (0.5) #////////////////////////////////////////////////////////// CLOSE
                    if(self.clamp < CLAMP_TIME):
                        s.send(motor0)
                        print motor0



                # Get the hand's sphere radius and palm position
                print "Hand sphere radius: %f mm, palm position: %s" % (
                      hand.sphere_radius, hand.palm_position)

                # Get the hand's normal vector and direction
                normal = hand.palm_normal
                direction = hand.direction

                # Calculate the hand's pitch
                print "Hand pitch: %f degrees" % (direction.pitch * Leap.RAD_TO_DEG) #-20 to 20, ignore -10 to 10
                hand_pitch = direction.pitch * Leap.RAD_TO_DEG
                if (hand_pitch > 10) and (hand_pitch) < 25:
                    motor1 = "1%f\n" % (0.4) #////////////////////////////////////////////////////////// WRIST UP
                    s.send(motor1)
                elif(hand_pitch > -20) and (hand_pitch < -10):
                    motor1 = "1%f\n" % (-0.4) #///////////////////////////////////////////////////////// WRIST DOWN
                    s.send(motor1)
                """
                # Gestures
                for gesture in frame.gestures():
                    if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                        circle = CircleGesture(gesture)

                        # Determine clock direction using the angle between the pointable and the circle normal
                        if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
                            clockwiseness = "clockwise"
                        else:
                            clockwiseness = "counterclockwise"

                        # Calculate the angle swept since the last frame
                        swept_angle = 0
                        if circle.state != Leap.Gesture.STATE_START:
                            previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                            swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                        print "Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                                gesture.id, self.state_string(gesture.state),
                                circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

                    if gesture.type == Leap.Gesture.TYPE_SWIPE:
                        swipe = SwipeGesture(gesture)
                        print "Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                                gesture.id, self.state_string(gesture.state),
                                swipe.position, swipe.direction, swipe.speed)

                    if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                        keytap = KeyTapGesture(gesture)
                        print "Key Tap id: %d, %s, position: %s, direction: %s" % (
                                gesture.id, self.state_string(gesture.state),
                                keytap.position, keytap.direction )

                    if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                        screentap = ScreenTapGesture(gesture)
                        print "Screen Tap id: %d, %s, position: %s, direction: %s" % (
                                gesture.id, self.state_string(gesture.state),
                                screentap.position, screentap.direction )
                """
            # print "%f seconds" % (time.time() - start)

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():

    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    #print "here"
    #sys.exit() 
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
