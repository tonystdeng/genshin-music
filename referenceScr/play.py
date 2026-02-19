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
        "lastEventTick": 0, # last tick where something happened
        "tempo": 500000, # micro second per quarter
        "currentNotes": dict() # absolutenote: velocity
    } for _ in mid.tracks]

    # main loop
    lastUpdateTime = time.time()
    while True:
        for i in range(len(mid.tracks)):
            updateTrack(mid.tracks[i], tracksInfo[i], time.time() - lastUpdateTime, tpqn)
        lastUpdateTime = time.time()

def updateTrack(track, trackInfo, deltaT, tpqn):
    # go through events until reached unreached
    while True:
        msg = track[0]
        if msg.time >= trackInfo["lastEventTick"]:
            trackInfo["lastEventTick"] = trackInfo["lastEventTick"] - msg.time
            track.pop(0)
            checkEvent(msg, trackInfo)
        else:
            break
    
    #update ticks
    trackInfo["lastEventTick"] += deltaT / trackInfo["tempo"] * tpqn

def checkEvent(event, trackInfo):
    if event.type=='set_tempo':
        trackInfo["tempo"] = event.tempo
    elif event.type=="note_on":
        if event.velocity==0 and event.note in trackInfo["currentNotes"]:
            # just another way to note_off acording to gpt ^
            trackInfo["currentNotes"].pop(event.note)
        else:# a new note is playing, record its info and will be sotred when stoped
            trackInfo["currentNotes"][event.note] = event.velocity

    elif event.type=="note_off":
        if not len(trackInfo["currentNotes"]):
            print("Your MIDI file tried to stop a note that is never played, please fix it somehow.")
            return 1
        trackInfo["currentNotes"].clear()