import itertools
from random import randint

from webcolors import name_to_rgb

from neopixel import Adafruit_NeoPixel
from util import *


class RGBController:
    strip = None

    def __init__(self):
        LED_COUNT = 300
        LED_PIN = 18
        LED_FREQ_HZ = 800000
        LED_DMA = 10
        LED_BRIGHTNESS = 255
        LED_INVERT = False
        LED_CHANNEL = 0
        STRIP_TYPE = 0x00081000  # GRB

        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                                       LED_BRIGHTNESS, LED_CHANNEL, STRIP_TYPE)
        self.strip.begin()

    def clear(self, state):
        """Clears the strip one by one."""
        static_color_array(self.strip, state[0]['colors'])
        self.color_wipe(state, Color(0, 0, 0))

    def fire(self, state):
        """Fire effect."""
        while True:
            for i in range(40) + range(self.strip.numPixels() - 25, self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(randint(180, 255), 0, 0))

            for i in range(40, self.strip.numPixels() - 25):
                self.strip.setPixelColor(i, Color(
                    randint(180, 255),
                    randint(10, 50) if random() > 0.7 else 0,
                    0))

            self.strip.show()
            self.save_state(state, save_pixels(self.strip))
            sleep(randint(100, 200) / 1000.0)

    def rainbow(self, state, wait_ms=0):
        """Whole rainbow moves across the strip."""
        while True:
            for j in range(256):
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, rainbow_wheel((i + j) & 255))
                self.strip.show()
                self.save_state(state, save_pixels(self.strip))
                sleep(wait_ms / 1000.0)

    def rainbow_color_wipe(self, state):
        """Wipe 12 colors across display a pixel at a time."""
        for color in itertools.cycle(RAINBOW):
            self.color_wipe(state, color, 10)

    def rainbow_fade(self, state, brightness=255):
        """Fades between all the colors in the rainbow."""
        color_generator = rainbow_color_generator(brightness)
        wait = int((-1 / 5.0 * brightness) + 50) if brightness <= 200 else 10

        while True:
            c = color_generator.next()
            self.static_color(c[0], c[1], c[2], wait)
            self.save_state(state, save_pixels(self.strip))

    def random_fade(self, state):
        """Randomly fades between colors."""
        old_r, old_g, old_b = random_color()
        self.static_color(old_r, old_g, old_b)

        while True:
            new_r, new_g, new_b = random_color()

            dist_r = old_r - new_r
            dist_g = old_g - new_g
            dist_b = old_b - new_b

            steps = max(abs(dist_r), abs(dist_g), abs(dist_b))

            step_r = (steps / float(abs(dist_r))) if dist_r != 0 else 999
            step_g = (steps / float(abs(dist_g))) if dist_g != 0 else 999
            step_b = (steps / float(abs(dist_b))) if dist_b != 0 else 999

            for i in range(1, steps + 1):
                if i % step_r < 1:
                    old_r = (old_r - 1) if dist_r > 0 else old_r + 1
                if i % step_g < 1:
                    old_g = (old_g - 1) if dist_g > 0 else old_g + 1
                if i % step_b < 1:
                    old_b = (old_b - 1) if dist_b > 0 else old_b + 1
                self.static_color(old_r, old_g, old_b, 10)
                self.save_state(state, save_pixels(self.strip))

    def snake(self, state, method="color"):
        """
        Snake implementation for all 3 methods:
        color: Snake with changing color.
        fade: Snake with continuously changing color.
        rainbow: Snake with the whole rainbow.
        """
        start = 0
        length = 48
        direction = False
        count = itertools.count()
        normal_color = None
        fade_color_gen = rainbow_color_generator()
        while True:
            r, g, b = fade_color_gen.next()
            fade_color = Color(r, g, b)

            if start == self.strip.numPixels() - length or start == 0:
                direction = not direction
                normal_color = RAINBOW[count.next() % 12]

            for i in range(start) + range(start + length, self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(0, 0, 0))

            for i in range(start, start + length):
                color = normal_color if method == "color" else fade_color if method == "fade" else RAINBOW[
                    (i - start) / 4]
                self.strip.setPixelColor(i, color)

            if direction:
                start += 1
            else:
                start -= 1

            self.strip.show()
            self.save_state(state, save_pixels(self.strip))
            sleep(0.01)

    def static_color(self, r, g, b, wait_ms=0):
        """Switches color of the whole strip."""
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            static_color_array(self.strip, [Color(r, g, b)] * self.strip.numPixels(), wait_ms)
        else:
            self.show_error()

    def static_color_name(self, name, wait_ms=0):
        """Switches color of the whole strip by name."""
        try:
            rgb = name_to_rgb(name)
            self.static_color(rgb.red, rgb.green, rgb.blue, wait_ms)
        except ValueError:
            self.show_error()

    def static_gradient(self, c1, c2):
        """Gradient between 2 colors."""
        if all([0 <= i <= 255 and 0 <= j <= 255 for i in c1 for j in c2]):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, gradient_color(i, c1, c2, self.strip.numPixels()))
            self.strip.show()
        else:
            self.show_error()

    def strobe(self, state, wait_ms=300):
        """Strobe effect."""
        while True:
            r, g, b = random_color()
            self.static_color(r, g, b, wait_ms)
            self.save_state(state, save_pixels(self.strip))

    def color_wipe(self, state, color, wait_ms=0):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            self.save_state(state, save_pixels(self.strip))
            sleep(wait_ms / 1000.0)

    def save_state(self, state, colors):
        """Saves the state of the strip between processes."""
        d = state[0]
        d['colors'] = colors
        state[0] = d

    def show_error(self):
        """Flashes red twice."""
        colors = save_pixels(self.strip)
        for i in range(2):
            self.static_color(0, 0, 0)
            sleep(0.1)
            self.static_color(255, 0, 0)
            sleep(0.1)

        self.static_color(0, 0, 0)
        sleep(0.1)
        static_color_array(self.strip, colors)
