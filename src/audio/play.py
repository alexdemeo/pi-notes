import threading
import wave

from pyaudio import PyAudio


def ding(file):
    def go():
        filepath = "/home/pi/tmp/talkynotes/" + "resources/audio/" + file + ".wav"
        wf = wave.open(filepath, "rb")
        chunk = 1024
        p = PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                        rate=wf.getframerate(), output=True)
        data = wf.readframes(chunk)
        while data != b'':
            stream.write(data)
            data = wf.readframes(chunk)
        stream.close()
        p.terminate()

    t = threading.Thread(target=go)
    t.start()


if __name__ == '__main__':
    ding("beep")
    # ding("note")
    # ding("cello")
