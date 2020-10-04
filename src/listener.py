import collections
import queue
import wave
import numpy
import pyaudio
import webrtcvad

from scipy import signal


class Audio(object):
    FORMAT = pyaudio.paInt16
    RATE_PROCESS = 16000
    CHANNELS = 1
    BLOCKS_PER_SECOND = 50

    def callback(self, in_data):
        self.buffer_queue.put(in_data)

    def __init__(self, callback=None, device=None, input_rate=RATE_PROCESS):
        def proxy_callback(in_data, frame_count, time_info, status):
            if self.chunk is not None:
                in_data = self.wf.readframes(self.chunk)
            callback(in_data)
            return None, pyaudio.paContinue
        if callback is None:
            callback = self.callback
        self.buffer_queue = queue.Queue()
        self.device = device
        self.input_rate = input_rate
        self.sample_rate = self.RATE_PROCESS
        self.block_size = int(self.RATE_PROCESS / float(self.BLOCKS_PER_SECOND))
        self.block_size_input = int(self.input_rate / float(self.BLOCKS_PER_SECOND))
        self.pa = pyaudio.PyAudio()
        kwargs = {
            'format': self.FORMAT,
            'channels': self.CHANNELS,
            'rate': self.input_rate,
            'input': True,
            'frames_per_buffer': self.block_size_input,
            'stream_callback': proxy_callback,
        }
        self.chunk = None
        kwargs['input_device_index'] = self.device
        print("PyAudio args:", kwargs)
        self.stream = self.pa.open(**kwargs)
        self.stream.start_stream()

    def resample(self, data, input_rate):
        data16 = numpy.fromstring(string=data, dtype=numpy.int16)
        resample_size = int(len(data16) / input_rate * self.RATE_PROCESS)
        resample = signal.resample(data16, resample_size)
        resample16 = numpy.array(resample, dtype=numpy.int16)
        return resample16.tostring()

    def read_resampled(self):
        return self.resample(data=self.buffer_queue.get(), input_rate=self.input_rate)

    def read(self):
        return self.buffer_queue.get()

    def destroy(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()

    frame_duration_ms = property(lambda self: 1000 * self.block_size // self.sample_rate)

    def write_wav(self, filename, data):
        print("write wav %s", filename)
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        # wf.setsampwidth(self.pa.get_sample_size(FORMAT))
        assert self.FORMAT == pyaudio.paInt16
        wf.setsampwidth(2)
        wf.setframerate(self.sample_rate)
        wf.writeframes(data)
        wf.close()


class VADAudio(Audio):
    def __init__(self, aggressiveness=0, device=None, input_rate=None):
        super().__init__(device=device, input_rate=input_rate)
        self.vad = webrtcvad.Vad(aggressiveness)

    def frame_generator(self):
        if self.input_rate == self.RATE_PROCESS:
            while True:
                yield self.read()
        else:
            while True:
                yield self.read_resampled()

    def vad_collector(self, padding_ms=300, ratio=0.75, frames=None):
        frames = self.frame_generator()
        num_padding_frames = padding_ms // self.frame_duration_ms
        ring_buffer = collections.deque(maxlen=num_padding_frames)
        triggered = False
        for frame in frames:
            if len(frame) < 640:
                return
            is_speech = self.vad.is_speech(frame, self.sample_rate)
            if not triggered:
                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])
                if num_voiced > ratio * ring_buffer.maxlen:
                    triggered = True
                    for f, s in ring_buffer:
                        yield f
                    ring_buffer.clear()
            else:
                yield frame
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                if num_unvoiced > ratio * ring_buffer.maxlen:
                    triggered = False
                    yield None
                    ring_buffer.clear()

