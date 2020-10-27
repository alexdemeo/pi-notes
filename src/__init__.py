import threading

import deepspeech
import numpy

from src.audio.listener import VADAudio
from src.lights.lights import Lights
from src.notes.note import record
from src.audio.play import ding
from fuzzywuzzy import fuzz

AGGRESSIVENESS = 0
MIC_INDEX = 4
INPUT_RATE = 44100
TRIGGER_MSG = "excuse me sir"
TERMINATE_MSG = "shut the fuck up"
DIR = "/home/pi/tmp/talkynotes/"


def matches(s1, s2, score):
    return fuzz.ratio(s1, s2) >= score


if __name__ == '__main__':
    quot = "\""
    print("START =", quot + TRIGGER_MSG + quot, ", END =", quot + TERMINATE_MSG + quot)
    model = deepspeech.Model(DIR + "resources/models/deepspeech-0.8.2-models.tflite")
    model.enableExternalScorer(DIR + "resources/models/deepspeech-0.8.2-models.scorer")
    vad_audio = VADAudio(AGGRESSIVENESS, MIC_INDEX, INPUT_RATE)
    frames = vad_audio.vad_collector()
    stream_context = model.createStream()
    lights = Lights()
    standby = True
    for frame in frames:
        if frame is not None:
            stream_context.feedAudioContent(numpy.frombuffer(frame, numpy.int16))
        else:
            if standby:
                text = stream_context.finishStream()
                print(text)
                if matches(text, TRIGGER_MSG, 75):
                    ding("note")
                    lights.start()
                    print("Recording...")
                    standby = False
                stream_context = model.createStream()
            else:
                text = stream_context.intermediateDecode()
                print(text)
                last_bit = text[-len(TERMINATE_MSG):]
                if matches(last_bit, TERMINATE_MSG, 75):
                    lights.stop()
                    text = stream_context.finishStream()
                    ding("cello")
                    record(text.replace(TERMINATE_MSG, ''))
                    standby = True
                    stream_context = model.createStream()
    print("exit")
