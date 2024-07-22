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
            self.pixels[item] = colour

    def show(self):
        self.pixels.show()
        
    def fill(self, colour):
        for pixs in self.groups:
            for pix in pixs:
                self.pixels[pix] = colour

segments_body = [[0],[9],[10],[22],[23],[34]]

segments_rhs = [[1,2,3],[4,5],[6],[7,8],[11,12],[13,16],[14,15],
               [17,19],[18],[20,21,26],[24,25,31],[27],[28],[29,37],
               [30],[32,33],[35,36]]
               
segments_lhs = [[0,1,2],[3,4],[5],[6,7],[8,9],[10,13],[11,12],
               [14,16],[15],[17,18,21],[19,20,26],[22],[23],[24,31],[25],[27,28],[29,30]]

bright_div = 100
numpix = 17  # number of segments
string_len = 38
pixpin = board.GP0
# Pin where NeoPixels are connected
pixels = neopixel.NeoPixel(pixpin, string_len, brightness=0.7, auto_write=False)

#soft
'''
colors = [
    [232, 100, 255],  # Purple
    [200, 200, 20],  # Yellow
    [30, 200, 200],  # Blue
    [100,200,50], #pink?
    [200,100,100], # turquoise
    [200,100,50], #light green?
    
]
'''


'''
#hard
colors = [
[255,0,0],
[0,255,0],
[0,0,255],
[255,255,0],
[255,0,255],
[0,255,255]

]
'''

#shades of red
colors = [
[20,255,0],
[70,255,0],
[50,255,0],
[50,255,50],
[0,255,40]
]

pixels_left = neopixel.NeoPixel(board.GP20,32, brightness=0.7, auto_write=False)

strip = segmented_neopixels(pixels,segments_rhs)
body = segmented_neopixels(pixels, segments_body)
strip_left = segmented_neopixels(pixels_left, segments_lhs)



'''
strip.fill((20,20,20))
strip.show()
time.sleep(1000)
'''

max_len=25
min_len = 10
#pixelnum, posn in flash, flash_len, direction
flashing = []

num_flashes = 10

for i in range(num_flashes):
    pix = random.randint(0, numpix - 1)
    col = random.randint(1, len(colors) - 1)
    flash_len = random.randint(min_len, max_len)
    flashing.append([pix, colors[col], flash_len, 0, 1])

strip.fill((0,0,0))
strip_left.fill((0,0,0))

body.fill((0,100,0))

while True:
    strip.show()
    strip_left.show()
    for i in range(num_flashes):
        pix = flashing[i][0]
        brightness = (flashing[i][3]/flashing[i][2])
        colr = (int(flashing[i][1][0]*brightness),
                int(flashing[i][1][1]*brightness),
                int(flashing[i][1][2]*brightness))
        strip[pix] = colr
        strip_left[pix] = colr
        if flashing[i][2] == flashing[i][3]:
            flashing[i][4] = -1
        if flashing[i][3] == 0 and flashing[i][4] == -1:
            current_pix = []
            for j in range(num_flashes):
                current_pix.append(flashing[j][0])
            pix = random.randint(0, numpix - 1)
            while (pix in current_pix):
                pix = random.randint(0, numpix - 1)
            
            col = random.randint(0, len(colors) - 1)
            flash_len = random.randint(min_len, max_len)
            flashing[i] = [pix, colors[col], flash_len, 0, 1]
        flashing[i][3] = flashing[i][3] + flashing[i][4]
    time.sleep(0.1)

