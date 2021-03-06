import logging
import sys
import time
import rtmidi
import numpy as np
import threading
n_pulses = 100000


def main():
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()

    if available_ports:
        midiout.open_port(2)
    else:
        midiout.open_virtual_port("My virtual output")    
    def send_pulse():
        midiout.send_message([248])
    def send_start():
        midiout.send_message([250])

    def send_midi_clock_primitive(tempo):
        start_time = time.time() # maybe change to absolute time later
        period = (60.0/tempo)/24.0
        epsilon = 0.001
    
        while True:
            next_pulse_time = start_time + (np.floor((time.time()-start_time)/period) + 1) * period
            if next_pulse_time - time.time() < epsilon:
                midiout.send_message([248])
                time.sleep(epsilon*2)
            else:
                time.sleep(0.001)
    def send_midi_clock(tempo):
        period = (60.0/tempo)/24.0
        start_time = time.time() # maybe change to absolute time later
        lookahead = 0.002
    
        while True:
            now = time.time()
            next_pulse_time = start_time + (np.floor((now-start_time)/period) + 1) * period
            if next_pulse_time - now < lookahead:
                threading.Timer(next_pulse_time - time.time(), send_pulse, ()).start()
                time.sleep(lookahead*2)
            else:
                time.sleep(0.001)

    def start_on_beat(tempo):
        threshold = 0.001
        period = (60.0/tempo)
        now = time.time()
        next_quarter_note_time = (np.floor(now/period) + 1) * period
        while next_quarter_note_time - time.time() > threshold:
            time.sleep(0.001)
        send_midi_clock(tempo)
    
    def start_on_measure(tempo):
        threshold = 0.001
        period = (60.0/tempo) * 4
        now = time.time()
        next_measure_time = (np.floor(now/period) + 1) * period
        while next_measure_time - time.time() > threshold:
            time.sleep(0.001)
#        midiout.send_message([250])
        send_midi_clock_primitive(tempo)

    start_on_measure(120)

if __name__=="__main__":
    main()

