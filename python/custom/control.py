import time

import webcolors

from neopixel import Adafruit_NeoPixel, Color


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

    def color_wipe(self, color, wait_ms=0):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def rainbow_color_wipe(self):
        """Wipe 12 colors across display a pixel at a time."""
        while True:
            self.color_wipe(Color(255, 0, 0), 10)
            self.color_wipe(Color(255, 127, 0), 10)
            self.color_wipe(Color(255, 255, 0), 10)
            self.color_wipe(Color(127, 255, 0), 10)
            self.color_wipe(Color(0, 255, 0), 10)
            self.color_wipe(Color(0, 255, 127), 10)
            self.color_wipe(Color(0, 255, 255), 10)
            self.color_wipe(Color(0, 127, 255), 10)
            self.color_wipe(Color(0, 0, 255), 10)
            self.color_wipe(Color(127, 0, 255), 10)
            self.color_wipe(Color(255, 0, 255), 10)
            self.color_wipe(Color(255, 0, 127), 10)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        while True:
            for j in range(256 * iterations):
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, self.wheel((i + j) & 255))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)

    def clear(self):
        """Clears the strip one by one."""
        self.color_wipe(Color(0, 0, 0))

    def instant_color(self, color, r=None, g=None, b=None):
        """Instantly switches color."""
        if color is None:
            self.instant_color_array([Color(r, g, b)] * self.strip.numPixels())
        else:
            self.instant_color_array([color] * self.strip.numPixels())

    def instant_color_array(self, color):
        """Instantly switches color from an array of colors."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color[i])
        self.strip.show()

    def instant_color_name(self, name):
        """Instantly switches color from a color name."""
        try:
            rgb = webcolors.name_to_rgb(name)
            self.instant_color(Color(rgb.red, rgb.green, rgb.blue))
        except ValueError:
            self.show_error()

    def show_error(self):
        """Flashes red twice."""
        colors = self.save_pixels()
        for i in range(2):
            self.instant_color(Color(0, 0, 0))
            time.sleep(0.1)
            self.instant_color(Color(255, 0, 0))
            time.sleep(0.1)

            self.instant_color(Color(0, 0, 0))
        time.sleep(0.1)
        self.instant_color_array(colors)

    def save_pixels(self):
        """Saves current pixel colors"""
        return [self.strip.getPixelColor(i) for i in range(self.strip.numPixels())]

# TODO: Voltage drop effect
# TODO: Strobe
# TODO: Fade random
# TODO: Fade rainbow
