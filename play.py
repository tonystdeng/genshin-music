import time
import sys

import pynput
keymap = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

from mido import MidiFile

def play(fileName):
    try:
        mid=MidiFile(fileName)
    except FileNotFoundError:
        print(f"\nCan't find {fileName}, program exited.")
        return 1
    tpqn = mid.ticks_per_beat # Ticks Per Quarter Note

    tracksInfo = [{
        "tick": 0, # tick number
        "tempo": 500000, # micro second per quarter
        "currentNotes": [] # [absolutenote, velocity]
    } for _ in mid.tracks]

    # main loop
    startTime = time.time()

    print(type(mid.tracks), "\n")
    sys.exit()
    while True:
        for track in mid.tracks:
            pass
