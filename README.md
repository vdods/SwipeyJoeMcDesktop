# Swipey Joe McDesktop

A service which recognizes sequences of hand gestures tracked by the Leap Motion Controller and triggers keyboard events based on a customizable configuration file.

#### Required Python modules

Swipey Joe is written in Python using `PyUserInput` and is ostensibly cross platform, though I haven't tested it on anything but Linux.

- `Leap` -- make sure that the files `Leap.py`, `LeapPython.so`, and `libLeap.so` (where `.so` would be `.dylib` or `.dll` on Mac and Windows respectively) are in your Python path.
- `PyUserInput` -- in particular `pykeyboard` -- and its particular dependencies.

## Usage Instructions

Swipey Joe reads the contents of the JSON-formatted configuration file `SwipeyJoeMcDesktop.config`, which defines a set of gesture sequence bindings.
Each binding is a sequence of hand gestures followed by an action string.  Upon recognition of a particular gesture sequence, the keyboard events (or
otherwise) corresponding to the associated action are emitted.  Thus, one has easily customizable gesture-based commands.

Swipey Joe recognizes the following Leap-based hand gestures:
- Hand swipe (a quick, linear motion with the fingers extended) in any of the 8 compass directions E, NE, N, NW, W, SW, S, SE (think of the compass hanging vertically on a wall), distinguishing between left and right hands.
- Key tap (With hand extended, palm down, using a single finger to quickly tap in mid-air, as if there were a keyboard directly under the finger) with any of the 5 fingers.

Here is an example configuration.  The brief_description and detailed_description key/value pairs are not currently used past self-documentation, but will be once the visualization component is implemented.

    {
        "description":"Victor Dods' configuration file for use with Linux/KDE.",
        "bindings":[
            {
                "sequence"              :["N"],
                "action"                :"control+f10",
                "brief_description"     :"Show all windows",
                "detailed_description"  :"Swipe north (either hand) to show all windows"
            },
            {
                "sequence"              :["W"],
                "action"                :"control+alt+right",
                "brief_description"     :"Switch one desktop right.",
                "detailed_description"  :"Swipe west (either hand) to switch one desktop right."
            },
            {
                "sequence"              :["E"],
                "action"                :"control+alt+left",
                "brief_description"     :"Switch one desktop left.",
                "detailed_description"  :"Swipe east (either hand) to switch one desktop left."
            },
            {
                "sequence"              :["S"],
                "action"                :"control+alt+a",
                "brief_description"     :"Switch to application demanding attention.",
                "detailed_description"  :"Swipe south (either hand) to switch to the application currently demanding attention (such as a newly opened web link, or a chat window with newly received message)."
            },
            {
                "sequence"              :["SW"],
                "action"                :"control+alt+shift+a",
                "brief_description"     :"Switch to code editor window.",
                "detailed_description"  :"Swipe south-west (either hand) to switch to the code editor window (which has been manually configured in KDE to use the control+alt+shift+a keyboard shortcut)."
            },
            {
                "sequence"              :["SE"],
                "action"                :"control+alt+shift+b",
                "brief_description"     :"Switch to web browser window.",
                "detailed_description"  :"Swipe south-east (either hand) to switch to the main web browser window (which has been manually configured in KDE to use the control+alt+shift+b keyboard shortcut)."
            },
            {
                "sequence"              :["righthand:T-index"],
                "action"                :"alt:hold+shift:release+tab",
                "brief_description"     :"Walk forward through windows.",
                "detailed_description"  :"Tap with right index finger to walk forward through windows.  Hold the hand out to keep the window visualization, withdraw to complete the window selection."
            },
            {
                "sequence"              :["righthand:T-middle"],
                "action"                :"alt:hold+shift:hold+tab",
                "brief_description"     :"Walk backward through windows.",
                "detailed_description"  :"Tap with right middle finger to walk backward through windows.  Hold the hand out to keep the window visualization, withdraw to complete the window selection."
            },
            {
                "sequence"              :["lefthand:T-index"],
                "action"                :"control:hold+shift:release+tab",
                "brief_description"     :"Walk forward through application tabs.",
                "detailed_description"  :"Tap with left index finger to walk forward through application tabs.  Withdraw the hand to complete the tab selection."
            },
            {
                "sequence"              :["lefthand:T-middle"],
                "action"                :"control:hold+shift:hold+tab",
                "brief_description"     :"Walk backward through application tabs.",
                "detailed_description"  :"Tap with left middle finger to walk backward through application tabs.  Withdraw the hand to complete the tab selection."
            },
            {
                "sequence"              :["T-thumb","T-thumb","T-thumb"],
                "action"                :"control+alt+l",
                "brief_description"     :"Lock the desktop.",
                "detailed_description"  :"Tap with the thumb (on either hand) three times to lock the desktop."
            }
        ]
    }

A gesture string, as used in the configuration file, must be one of the following.

- `"lefthand:<gesturename>"` - Recognizes the gesture given by `<gesturename>` only for the left hand.
- `"righthand:<gesturename>"` - Recognizes the gesture given by `<gesturename>` only for the right hand.
- `"<gesturename>"` - Recognizes the gesture given by `<gesturename>` for either hand.

The value of `<gesturename>` must be one of the following.

- `E`, `NE`, `N`, `NW`, `W`, `SW`, `S`, `SE` - A hand swipe in the east, north-east, north, west, south-west, south, or south-east directions respectively.
- `T-thumb`, `T-index`, `T-middle`, `T-ring`, `T-pinky` - A key tap with the thumb, index, middle, ring, or pinky finger respectively.

An action string must be one of the following.

- `<keycommand>[+<keycommand>]...[+<keycommand>]` - A combination of the specified keys.

The value of `<keycommand>` must be one of the following.  The `hold` and `release` modifiers are used to create persistent actions (e.g. using `alt+tab` and `alt+shift+tab` to walk through windows with a visualization).

- `<keyname>` - Press and release the named key.
- `<keyname>:hold` - Press the named key and leave it held down.
- `<keyname>:release` - Release the named key (before any other keys in the action are pressed).

The value of `<keyname>` must be a named key, such as `x`, `space`, `control`, etc., including platform-specific names, some of which are quite strange.  The available keys (as well as unsupported keys) 
are printed to console upon Swipey Joe startup.

## Author

Victor Dods at Leap Motion (vdods@leapmotion.com or victor.dods@gmail.com)

## History

- `2015.06.09` -- Initial publication.
