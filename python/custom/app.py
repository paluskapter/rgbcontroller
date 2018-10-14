import multiprocessing as mp

from flask import Flask

from control import RGBController

app = Flask(__name__)
rgb = RGBController()
proc = None


@app.route('/')
def index():
    return 'Raspberry Pi RGB strip controller'


@app.route('/clear')
def clear():
    rgb.clear()
    return 'clear'


@app.route('/fire')
def fire():
    start_process(rgb.fire)
    return 'fire'


@app.route('/music')
def music():
    start_process(rgb.music)
    return 'music'


@app.route('/rainbow')
def rainbow():
    start_process(rgb.rainbow)
    return 'rainbow'


@app.route('/rainbow_color_wipe')
def rainbow_color_wipe():
    start_process(rgb.rainbow_color_wipe)
    return 'rainbow_color_wipe'


@app.route('/rainbow_fade')
def rainbow_fade():
    start_process(rgb.rainbow_fade)
    return 'rainbow_fade'


@app.route('/random_fade')
def random_fade():
    start_process(rgb.random_fade)
    return 'random_fade'


@app.route('/snake_color')
def snake_color():
    start_process(rgb.snake_color)
    return 'snake_color'


@app.route('/snake_fade')
def snake_fade():
    start_process(rgb.snake_fade)
    return 'snake_fade'


@app.route('/snake_rainbow')
def snake_rainbow():
    start_process(rgb.snake_rainbow)
    return 'snake_rainbow'


@app.route('/static_color/<red>/<green>/<blue>')
def static_color(red, green, blue):
    try:
        rgb.static_color(int(red), int(green), int(blue))
    except ValueError:
        rgb.show_error()
    return 'static_color'


@app.route('/static_color_name/<name>')
def static_color_name(name):
    rgb.static_color_name(name)
    return 'static_color_name'


@app.route('/static_gradient/<r1>/<g1>/<b1>/<r2>/<g2>/<b2>')
def gradient(r1, g1, b1, r2, g2, b2):
    try:
        rgb.static_gradient((int(r1), int(g1), int(b1)), (int(r2), int(g2), int(b2)))
    except ValueError:
        rgb.show_error()
    return 'static_gradient'


@app.route('/static_voltage_drop')
def static_voltage_drop():
    rgb.static_voltage_drop()
    return 'static_voltage_drop'


@app.route('/strobe/<wait>')
def strobe(wait):
    try:
        start_process(rgb.strobe, (int(wait),))
    except ValueError:
        rgb.show_error()
    return 'strobe'


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

# TODO: Voice commands
