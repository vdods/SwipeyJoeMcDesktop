import json
import Leap
import sys
import time

from GestureSequenceController import *
from InputController import *
from LeapEventListener import *
import Log

def initialize_log ():
    """
    Creates a Log singleton in the Log module, and creates record, indent, and unindent functions
    in that module which call the respective methods on the Log singleton.  Also runs the Log
    unit test.
    """
    Log.Log.run_unit_test()
    
    Log.singleton = Log.Log(sys.stdout)
    
    def record (string):
        Log.singleton.record(string)
    def indent ():
        Log.singleton.indent()
    def unindent ():
        Log.singleton.unindent()
    
    Log.record   = record
    Log.indent   = indent
    Log.unindent = unindent

def main ():
    initialize_log()
    
    input_controller = InputController()
    
    def activate_key_combo (key_combo):
        input_controller.activate_key_combo(key_combo)
        
    gesture_sequence_controller = GestureSequenceController(json.load(open('SwipeyJoeMcDesktop.config')), activate_key_combo)

    def on_gesture (gesture_name):
        Log.record('on_gesture("{0}")\n'.format(gesture_name))
        Log.indent()
        gesture_sequence_controller.process_gesture(gesture_name)
        Log.unindent()

    def on_gesturing_hand_withdrawal ():
        Log.record('on_gesturing_hand_withdrawal()\n')
        Log.indent()
        input_controller.release_all_held_keys()
        gesture_sequence_controller.reset_active_sequences()
        Log.unindent()
        Log.record('\n\n\n')
    
    def grab_to_move_mouse_cursor (frame):
        if len(frame.hands) == 1:
            hand = frame.hands[0]
            if hand.grab_strength == 1.0:
                normalized_position = frame.interaction_box.normalize_point(hand.palm_position)
                input_controller.set_mouse_position((normalized_position[0], 1.0-normalized_position[1]))

    leap_event_listener = LeapEventListener(on_gesture, on_gesturing_hand_withdrawal, None)#grab_to_move_mouse_cursor)

    controller = Leap.Controller()
    controller.add_listener(leap_event_listener)
    try:
        while True:
            time.sleep(42)
    except KeyboardInterrupt:
        Log.record('KeyboardInterrupt -- exiting.\n')
        pass
    except:
        Log.record('Unhandled exception -- exiting.\n')
        pass

    controller.remove_listener(leap_event_listener)
    return 0

if __name__ == "__main__":
    sys.exit(main())
