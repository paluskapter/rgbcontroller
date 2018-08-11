import multiprocessing as mp

from flask import Flask

from control import RGBController

app = Flask(__name__)
rgb = RGBController()
proc = None


@app.route('/')
def index():
    return 'Hello world, I am PI'


@app.route('/instant_color/<red>/<green>/<blue>')
def instant_color(red, green, blue):
    rgb.instant_color(color=None, r=int(red), g=int(green), b=int(blue))
    return '(' + red + ',' + green + ',' + blue + ')'


@app.route('/instant_color_name/<name>')
def instant_color_name(name):
    rgb.instant_color_name(name)
    return name


@app.route('/rainbow')
def rainbow():
    start_process(rgb.rainbow)
    return 'rainbow'


@app.route('/rainbow_color_wipe')
def rainbow_color_wipe():
    start_process(rgb.rainbow_color_wipe)
    return 'rainbow_color_wipe'


@app.route('/clear')
def clear():
    rgb.clear()
    return 'clear'


def start_process(func, args=()):
    global proc
    proc = mp.Process(target=func, args=args)
    proc.start()


@app.before_request
def stop_process():
    global proc
    if proc is not None:
        proc.terminate()
        proc.join()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
