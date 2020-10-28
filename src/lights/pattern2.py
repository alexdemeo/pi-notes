from time import sleep

from src.lights.lights import Lights, rgb_from_hex

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


class Pattern2(Lights):
    def __init__(self, rate, factor):
        super().__init__(rate,)
        self.factor = factor
        self.color_index = 0

    def tick(self, i):
        if self.color_index == len(color_arr) - 1:
            self.color_index = 0
        else:
            self.color_index += 1

        if self.color_index == 0:
            self.set_rate(self.get_rate() * self.factor)
        elif self.color_index == len(color_arr) // 2:
            self.set_rate(self.get_rate() / self.factor)

        color_hex = color_arr[self.color_index]
        return rgb_from_hex(color_hex)


if __name__ == '__main__':
    lights = Pattern2(0.04, 7.5)
    lights.start()
    sleep(5)
    lights.stop()
    print('end')
