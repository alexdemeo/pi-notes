import threading
import webcolors

from gpiozero import LED
from apa102_pi.driver.apa102 import APA102
from time import sleep

from src.lights.lights import Lights, rgb_from_hex

N = 12

BASE_R = 90
BASE_G = 10
BASE_B = 8

MAX_COLOR = 200
INCREMENT = 5

color_arr = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
              '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
              '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
              '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
              '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
              '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
              '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
              '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
              '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
              '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF']


class Pattern1(Lights):
    def __init__(self, rate):
        super().__init__(rate)
        self.color_index = 0

    def tick(self, i):
        if self.color_index == len(color_arr) - 1:
            self.color_index = 0
        else:
            self.color_index += 1
        color_hex = color_arr[self.color_index]
        return rgb_from_hex(color_hex)


if __name__ == '__main__':
    lights = Pattern1(0.01)
    lights.start()
    sleep(2)
    lights.stop()
    print('end')
