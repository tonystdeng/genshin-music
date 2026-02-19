import time
import asyncio
import pynput

import keyboardUtil

from mido import MidiFile

async def play(settings):
    #pynput setup
    keyboardController = pynput.keyboard.Controller()
    esc_listener=pynput.keyboard.Listener(on_press=keyboardUtil.key_check("esc"))
    esc_listener.start()
    p_listener=pynput.keyboard.Listener(on_press=keyboardUtil.key_check("f4"))
    p_listener.start()

    # file load
    try:
        mid=MidiFile(settings["filename"])
    except FileNotFoundError:
        print(f"\nCan't find {settings["filename"]}, program exited.")
        return 1
    tpqn = mid.ticks_per_beat # Ticks Per Quarter Note

    # track exclution if noted
    if settings["track"] >= 0:
        try:
            mid.tracks = [mid.tracks[int(settings["track"])]]
        except:
            print(f"\nTrack entered invalid, program exited.")
            return 1

    # track memory
    tracksInfo = [{
        "lastEventTick": 0, # last tick where something happened
        "tempo": 500000, # micro second per quarter
    } for _ in mid.tracks]

    # main loop
    lastUpdateTime = time.time()
    deltaTime = time.time() - lastUpdateTime
    while esc_listener.running:

        # react to pauses
        pauseReaction = keyboardUtil.encounterPause(p_listener, esc_listener)
        if pauseReaction == 2:
            return 2
        elif pauseReaction == 1:
            p_listener=pynput.keyboard.Listener(on_press=keyboardUtil.key_check("f4"))
            p_listener.start()
            lastUpdateTime = time.time()
            deltaTime = time.time() - lastUpdateTime

        # main logic: take notes from each track then play
        notesPlayed = set()
        active = False
        for i in range(len(mid.tracks)):
            newNotes = updateTrack(mid.tracks[i], tracksInfo[i], deltaTime * 1000000, tpqn)
            if newNotes == -1:
                continue
            active = True
            notesPlayed.update(newNotes)
        if not active: return
        errorPlaying = await asyncio.gather(
            *(keyboardUtil.playNotes(note, keyboardController, settings["shift"]) for note in notesPlayed)
        )
        if 1 in errorPlaying: return 1
        deltaTime = time.time() - lastUpdateTime
        lastUpdateTime = time.time()

    else:
        return 2

def updateTrack(track, trackInfo, deltaT, tpqn):
    notesPlayed = set()
    # go through events until reached unreached or reach the end
    while True:
        try:
            msg = track[0]
        except IndexError:
            return -1
        if msg.time <= trackInfo["lastEventTick"]:
            trackInfo["lastEventTick"] = trackInfo["lastEventTick"] - msg.time
            track.pop(0)
            note = checkEvent(msg, trackInfo)
            if note:
                notesPlayed.add(note)
        else:
            break
    
    #update ticks
    trackInfo["lastEventTick"] += deltaT / trackInfo["tempo"] * tpqn
    return notesPlayed

def checkEvent(event, trackInfo):
    if event.type=='set_tempo':
        trackInfo["tempo"] = event.tempo
    elif event.type=="note_on":
        if event.velocity!=0:
            return event.note
    return None