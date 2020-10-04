import deepspeech
import numpy

from src.listener import VADAudio
from src.note import record
from src.play import ding
from fuzzywuzzy import fuzz

AGGRESSIVENESS = 0
MIC_INDEX = 0
INPUT_RATE = 44100
TRIGGER_MSG = "hear me"
TERMINATE_MSG = "okay done"
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
    standby = True
    for frame in frames:
        if standby:
            if frame is not None:
                stream_context.feedAudioContent(numpy.frombuffer(frame, numpy.int16))
            else:
                text = stream_context.finishStream()
                print(text)
                if matches(text, TRIGGER_MSG, 75):
                    ding("note")
                    print("Recording...")
                    standby = False
                stream_context = model.createStream()
        else:
            if frame is not None:
                stream_context.feedAudioContent(numpy.frombuffer(frame, numpy.int16))
            else:
                text = stream_context.intermediateDecode()
                print(text)
                last_bit = text[-len(TERMINATE_MSG):]
                if matches(last_bit, TERMINATE_MSG, 75):
                    text = stream_context.finishStream()
                    ding("cello")
                    record(text.replace(TERMINATE_MSG, ''))
                    standby = True
                    stream_context = model.createStream()
    print("exit")
