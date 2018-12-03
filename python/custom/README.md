# rgbcontroller
### RGB strip controller for Raspberry Pi

Features various strip effects and an HTTP API for remote access.

Forked from [jgarff/rpi_ws281x](https://github.com/jgarff/rpi_ws281x) because this project relies on the Python NeoPixel library.

## Usage:
- Copy the whole project (not just this custom module) to the Pi
- Install the neopixel library
- Install this module's requirements
- Run [webserver.sh](https://github.com/paluskapter/rpi_ws281x/blob/master/python/custom/webserver.sh)

Callable endpoints are in [app.py](https://github.com/paluskapter/rpi_ws281x/blob/master/python/custom/app.py)

### Android UI for this project:
https://github.com/paluskapter/rgbapp
