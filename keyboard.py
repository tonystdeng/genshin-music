import time

import pynput
keymap = [
    {'c': 'z', 'd': 'x', 'e': 'c', 'f': 'v', 'g': 'b', 'a': 'n', 'b': 'm'},
    {'c': 'a', 'd': 's', 'e': 'd', 'f': 'f', 'g': 'g', 'a': 'h', 'b': 'j'},
    {'c': 'q', 'd': 'w', 'e': 'e', 'f': 'r', 'g': 't', 'a': 'y', 'b': 'u'}
]

noteNames = ["c","c#","d","d#","e","f","f#","g","g#","a","a#","b"]

async def playNotes(note, keyboard:pynput.keyboard.Controller, shift, roundDown = True, tolerateOctive = True):
    # decode notes into western triditional notation
    octave = note // 12 -1 + shift
    if octave > 5 or octave < 3:
        if tolerateOctive:
            if octave > 5: 
                octave = 5
                noteIndex = 11
            else: 
                octave = 3
                noteIndex = 0
        else:
            print(f"\nOctive too stretched, program exited.")
            return 1
    else:
        noteIndex = note % 12
    octave-=3
    if len(noteNames[noteIndex]) == 2:
        noteIndex -= 1 if roundDown else -1

    # press!
    key = keymap[octave][noteNames[noteIndex]]
    keyboard.press(key)
    keyboard.release(key)

# all this >>>>>>>>>>>>>>>>>>>>>>>>>
keys={
    "esc": pynput.keyboard.Key.esc,
    "f4": pynput.keyboard.Key.f4
}

def key_check(keyName):
    def key_checker(key):
        try:
            if key == keys[keyName]: 
                print(f"Detected \"{keyName}\"")
                return False
        except AttributeError: 
            return
    return key_checker
# i jsut copied from hackclub cheat >>>>>>>>>>>>>>

def encounterPause(p_listener, esc_listener):
    if not p_listener.running:
        print("paused, press f4 again to resume")
        p_listener=pynput.keyboard.Listener(on_press=key_check("f4"))
        p_listener.start()

        # pausing while encountering quit
        esc=False
        while p_listener.running:
            if not esc_listener.running:
                esc=True
                break

        # unpausing
        if esc:
            return 2
        else:
            print("resumed")
            return 1