import wave

from pyaudio import PyAudio


def ding(file):
    from src import DIR
    wf = wave.open(DIR + "resources/audio/" + file + ".wav", "rb")
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
