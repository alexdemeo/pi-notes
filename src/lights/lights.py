import threading

import abc
import webcolors

from gpiozero import LED
from apa102_pi.driver.apa102 import APA102
from time import sleep

N = 12

MAX_COLOR = 200
INCREMENT = 5


def rgb_from_hex(color):
    return webcolors.hex_to_rgb(color)


class Lights(metaclass=abc.ABCMeta):
    def __init__(self, rate):
        self.rate = rate
        self.power = LED(5)
        self.dev = APA102(num_led=N)
        self.running = False
        self.t = None
        self.rgb = (0, 0, 0)

    def start(self):
        self.t = threading.Thread(target=self.loop)
        self.power.on()
        self.running = True
        self.t.start()

    @abc.abstractmethod
    def tick(self, i):
        pass

    def _tick(self, i):
        self.rgb = self.tick(i)
        self.dev.set_pixel(i - 1, 0, 0, 0, 0)
        self.dev.set_pixel(i, *self.rgb)
        self.dev.show()

    def loop(self):
        while self.running:
            for i in range(1, N + 2):
                self._tick(i)
                sleep(self.rate)

    def stop(self):
        if self.running:
            self.power.off()
            self.running = False
            self.t.join()
