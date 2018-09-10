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

    def clear(self):
        """Clears the strip one by one."""
        self.instant_color(16, 16, 16)
        color_wipe(self.strip, Color(0, 0, 0))

    def comet(self):
        """Comet effect."""
        # TODO: Implement
        pass

    def fire(self):
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
            sleep(randint(100, 200) / 1000.0)

    def gradient(self, c1, c2):
        """Gradient between 2 colors."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, gradient_color(i, c1, c2, self.strip.numPixels()))
        self.strip.show()

    def instant_color(self, r, g, b, wait_ms=0):
        """Instantly switches color."""
        instant_color_array(self.strip, [Color(r, g, b)] * self.strip.numPixels(), wait_ms)

    def instant_color_name(self, name, wait_ms=0):
        """Instantly switches color from a color name."""
        try:
            rgb = name_to_rgb(name)
            self.instant_color(rgb.red, rgb.green, rgb.blue, wait_ms)
        except ValueError:
            self.show_error()

    def music(self):
        """Lights according to music."""
        # TODO: Implement
        pass

    def rainbow(self, wait_ms=0):
        """Draw rainbow that fades across all pixels at once."""
        while True:
            for j in range(256):
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, wheel((i + j) & 255))
                self.strip.show()
                sleep(wait_ms / 1000.0)

    def rainbow_color_wipe(self):
        """Wipe 12 colors across display a pixel at a time."""
        while True:
            color_wipe(self.strip, Color(255, 0, 0), 10)
            color_wipe(self.strip, Color(255, 127, 0), 10)
            color_wipe(self.strip, Color(255, 255, 0), 10)
            color_wipe(self.strip, Color(127, 255, 0), 10)
            color_wipe(self.strip, Color(0, 255, 0), 10)
            color_wipe(self.strip, Color(0, 255, 127), 10)
            color_wipe(self.strip, Color(0, 255, 255), 10)
            color_wipe(self.strip, Color(0, 127, 255), 10)
            color_wipe(self.strip, Color(0, 0, 255), 10)
            color_wipe(self.strip, Color(127, 0, 255), 10)
            color_wipe(self.strip, Color(255, 0, 255), 10)
            color_wipe(self.strip, Color(255, 0, 127), 10)

    def rainbow_fade(self):
        """Goes through all the colors (every led is the same color)"""
        r = 255
        g = 0
        b = 0
        while True:
            for i in range(255):
                g += 1
                self.instant_color(r, g, b, 10)
            for i in range(255):
                r -= 1
                self.instant_color(r, g, b, 10)
            for i in range(255):
                b += 1
                self.instant_color(r, g, b, 10)
            for i in range(255):
                g -= 1
                self.instant_color(r, g, b, 10)
            for i in range(255):
                r += 1
                self.instant_color(r, g, b, 10)
            for i in range(255):
                b -= 1
                self.instant_color(r, g, b, 10)

    def random_fade(self):
        """Randomly fades between colors."""
        old_r, old_g, old_b = random_color()
        self.instant_color(old_r, old_g, old_b)

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
                self.instant_color(old_r, old_g, old_b, 10)

    def snake(self):
        """Snake with changing color."""
        # TODO: Implement
        pass

    def snake_rainbow(self):
        """Rainbow snake effect."""
        # TODO: Implement
        pass

    def strobe(self, wait_ms):
        """Strobe effect."""
        while True:
            r, g, b = random_color()
            self.instant_color(r, g, b, wait_ms)

    def voltage_drop(self):
        """Voltage drop effect (white to orange)"""
        self.gradient((255, 255, 255), (255, 50, 0))

    def show_error(self):
        """Flashes red twice."""
        colors = save_pixels(self.strip)
        for i in range(2):
            self.instant_color(0, 0, 0)
            sleep(0.1)
            self.instant_color(255, 0, 0)
            sleep(0.1)

            self.instant_color(0, 0, 0)
        sleep(0.1)
        instant_color_array(self.strip, colors)
