import time

import board
import neopixel

try:
    import urandom as random
except ImportError:
    import random
    
class segmented_neopixels:
    def __init__(self, pixels, groups):
        self.pixels = pixels
        self.groups = groups

    def __setitem__(self, pixel, colour):
        for item in self.groups[pixel]:
            pixels[item] = colour

    def show(self):
        self.pixels.show()
        
    def fill(self, colour):
        for pix in range(len(pixels)):
            self.pixels[pix] = colour

segments_body = [[0],[9],[10],[22],[23],[34]]

segments_rhs = [[1,2,3],[4,5],[6],[7,8],[11,12],[14,15],[13,16],
               [17,19],[18],[20,21,26],[24,25,31],[27],[28],[29,37],
               [30],[32,33],[35,36]]

bright_div = 20
numpix = 17  # number of segments
string_len = 38
pixpin = board.GP0
# Pin where NeoPixels are connected
pixels = neopixel.NeoPixel(pixpin, string_len, brightness=1, auto_write=False)
colors = [
    [232, 100, 255],  # Purple
    [200, 200, 20],  # Yellow
    [30, 200, 200],  # Blue
]

strip = segmented_neopixels(pixels,segments_rhs)

'''
strip.fill((20,20,20))
strip.show()
time.sleep(1000)
'''

max_len=5
min_len = 2
#pixelnum, posn in flash, flash_len, direction
flashing = []

num_flashes = 5

for i in range(num_flashes):
    pix = random.randint(0, numpix - 1)
    col = random.randint(1, len(colors) - 1)
    flash_len = random.randint(min_len, max_len)
    flashing.append([pix, colors[col], flash_len, 0, 1])

strip.fill((0,0,0))

while True:
    strip.show()
    for i in range(num_flashes):
        print(flashing[i])
        pix = flashing[i][0]
        brightness = (flashing[i][3]/flashing[i][2])
        colr = (int(flashing[i][1][0]*brightness),
                int(flashing[i][1][1]*brightness),
                int(flashing[i][1][2]*brightness))
        strip[pix] = colr
        if flashing[i][2] == flashing[i][3]:
            flashing[i][4] = -1
        if flashing[i][3] == 0 and flashing[i][4] == -1:
            pix = random.randint(0, numpix - 1)
            col = random.randint(0, len(colors) - 1)
            flash_len = random.randint(min_len, max_len)
            flashing[i] = [pix, colors[col], flash_len, 0, 1]
        flashing[i][3] = flashing[i][3] + flashing[i][4]
    time.sleep(0.1)

