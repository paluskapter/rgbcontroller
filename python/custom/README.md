# rgbcontroller
### RGB strip controller for Raspberry Pi

Features various strip effects and an HTTP API for local access.

Also can check for inputs in an SQS queue for secure remote access.

Forked from [jgarff/rpi_ws281x](https://github.com/jgarff/rpi_ws281x) because this project relies on the Python NeoPixel library.

## Usage:
- Copy the whole project (not just this custom module) to the Pi
- Install the neopixel library
- Install this module's requirements
- If you want SQS functionality:
  - Leave SQS env var in [webserver.sh](https://github.com/paluskapter/rgbcontroller/blob/master/python/custom/webserver.sh)
  - Set SQS_URL env var
  - Create ~/.aws/config and fill it with your region, access and secret key
- Otherwise remove the SQS env var
- Run [webserver.sh](https://github.com/paluskapter/rgbcontroller/blob/master/python/custom/webserver.sh)

Callable endpoints are in [app.py](https://github.com/paluskapter/rgbcontroller/blob/master/python/custom/app.py)

### Android UI for this project:
https://github.com/paluskapter/rgbapp
