import Leap
import Log
import math
import time

class LeapEventListener (Leap.Listener):
    def __init__ (self, call_upon_gesture = None, call_upon_gesturing_hand_withdrawal = None, call_upon_frame = None):
        Leap.Listener.__init__(self)
        self.__compass_direction_name = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
        self.__compass_direction_image = ["   \n-->\n   \n", \
                                          "  7\n / \n/  \n", \
                                          " ^ \n | \n | \n", \
                                          "P  \n \\ \n  \\\n", \
                                          "   \n<--\n   ", \
                                          "  /\n / \nL  \n", \
                                          " | \n | \n V \n", \
                                          "\\  \n \\ \n  G\n"]
        def do_nothing ():
            pass
        self.__call_upon_gesture = call_upon_gesture
        self.__call_upon_gesturing_hand_withdrawal = call_upon_gesturing_hand_withdrawal
        self.__call_upon_frame = call_upon_frame
        self.__min_swipe_length = 70.0
        self.__min_swipe_velocity = 200.0
        self.__finger_names = { \
            Leap.Finger.TYPE_THUMB  :'thumb', \
            Leap.Finger.TYPE_INDEX  :'index', \
            Leap.Finger.TYPE_MIDDLE :'middle', \
            Leap.Finger.TYPE_RING   :'ring', \
            Leap.Finger.TYPE_PINKY  :'pinky' \
        }
        # NOTE: The way things are set up will probably lead to problems if one tries to gesture
        # with more than one hand at a time.
        self.__gesturing_hand_id = None
        self.__last_gesture_time = time.time()
        self.__gesture_cooldown_duration = 0.1 # seconds

    def on_connect (self, controller):
        Log.record('Connected to Leap service.\n')
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.config.set("Gesture.Swipe.MinLength", self.__min_swipe_length)
        controller.config.set("Gesture.Swipe.MinVelocity", self.__min_swipe_velocity)
        controller.config.save()

    def on_disconnect (self, controller):
        Log.record('Disconnected from Leap service.\n')

    def on_frame (self, controller):
        frame = controller.frame()
        if self.__call_upon_frame != None:
            self.__call_upon_frame(frame)
        gestures = frame.gestures()
        for gesture in gestures:
            self.__process_gesture(gesture)
        if self.__gesturing_hand_id != None and not frame.hand(self.__gesturing_hand_id).is_valid:
            if self.__call_upon_gesturing_hand_withdrawal != None:
                self.__call_upon_gesturing_hand_withdrawal()
                self.__gesturing_hand_id = None

    def on_exit (self, controller):
        pass

    def __process_gesture (self, gesture):
        current_time = time.time()
        if current_time < self.__last_gesture_time + self.__gesture_cooldown_duration:
            return
        # Swipes (including ones that are only in-progress) take precedence over taps.
        if gesture.type is Leap.Gesture.TYPE_SWIPE:
            if gesture.state is Leap.Gesture.STATE_STOP:
                swipe = Leap.SwipeGesture(gesture)
                for pointable in swipe.pointables:
                    if not pointable.is_finger:
                        continue

                    finger = Leap.Finger(pointable)
                    if finger.type is not Leap.Finger.TYPE_INDEX:
                        continue

                    swipe_offset = swipe.position - swipe.start_position
                    planar_swipe_offset_length_squared = swipe_offset.x**2 + swipe_offset.y**2
                    if planar_swipe_offset_length_squared < self.__min_swipe_length**2:
                        continue

                    assert len(gesture.hands) == 1
                    gesturing_hand = gesture.hands[0]
                    self.__gesturing_hand_id = gesturing_hand.id
                    swipe_angle = math.atan2(swipe.direction.y, swipe.direction.x)
                    tau = 2.0*math.pi
                    if (swipe_angle < 0.0):
                        swipe_angle += tau
                    assert 0.0 <= swipe_angle and swipe_angle <= tau
                    # lerp the real number range [0,tau] onto the integer range [0,8]
                    menu_index = int(round(8.0*swipe_angle/tau))
                    if menu_index == 8: # wrap 8 to 0.
                        menu_index = 0
                    handedness = "lefthand" if gesturing_hand.is_left else "righthand"
                    activated_compass_direction_name = self.__compass_direction_name[menu_index]
                    gesture_name = handedness + ":" + activated_compass_direction_name
                    #Log.record('swiped {0}\n{1}\n'.format(gesture_name, self.__compass_direction_image[menu_index]))
                    if self.__call_upon_gesture != None:
                        self.__call_upon_gesture(gesture_name)
                    self.__last_gesture_time = current_time
        elif gesture.type is Leap.Gesture.TYPE_KEY_TAP:
            key_tap = Leap.KeyTapGesture(gesture)
            if key_tap.pointable.is_finger:
                assert len(gesture.hands) == 1
                gesturing_hand = gesture.hands[0]
                self.__gesturing_hand_id = gesturing_hand.id
                finger = Leap.Finger(key_tap.pointable)
                handedness = "lefthand" if gesturing_hand.is_left else "righthand"
                tap_name = "T-" + self.__finger_names[finger.type]
                gesture_name = handedness + ":" + tap_name
                #Log.record('tapped {0}\n'.format(gesture_name))
                if self.__call_upon_gesture != None:
                    self.__call_upon_gesture(gesture_name)
                self.__last_gesture_time = current_time

