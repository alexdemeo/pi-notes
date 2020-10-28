from time import sleep

from src.lights.lights import Lights, rgb_from_hex, N


def _get_hex_str(hex_):
    hex_str = hex(hex_)[2:]
    zeroes = '0' * (6 - len(hex_str))
    result = '#' + zeroes + hex_str
    if result == '#100feff':
        print(hex_str)
    return result


class Pattern3(Lights):
    def __init__(self, rate, factor):
        super().__init__(rate)
        self.factor = factor
        self.hex = 0
        self.direction = 1
        self.brightness = 5

    def tick(self, i):
        if 0 < i < 100:
            self.brightness = 100
        else:
            self.brightness = 5
        self.hex += self.direction * self.factor
        if self.hex <= 0:
            self.hex = 0
            self.direction = 1
        elif self.hex > 0xffffff:
            self.hex = 0xffffff
            self.direction = -1

        hex_str = _get_hex_str(self.hex)
        print(hex_str)
        return (*rgb_from_hex(hex_str), self.brightness)


if __name__ == '__main__':
    lights = Pattern3(0.03, int(0xffffff * 0.05))
    lights.start()
    sleep(10)
    lights.stop()
    print('end')
