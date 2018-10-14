import multiprocessing as mp

from flask import Flask

from control import RGBController

app = Flask(__name__)
rgb = RGBController()
proc = None


@app.route('/')
def index():
    return 'Rasberry Pi RGB strip controller'


@app.route('/clear')
def clear():
    rgb.clear()
    return 'clear'


@app.route('/fire')
def fire():
    start_process(rgb.fire)
    return 'fire'


@app.route('/gradient/<r1>/<g1>/<b1>/<r2>/<g2>/<b2>')
def gradient(r1, g1, b1, r2, g2, b2):
    rgb.gradient((int(r1), int(g1), int(b1)), (int(r2), int(g2), int(b2)))
    return 'gradient'


@app.route('/instant_color/<red>/<green>/<blue>')
def instant_color(red, green, blue):
    rgb.instant_color(int(red), int(green), int(blue))
    return '(' + red + ',' + green + ',' + blue + ')'


@app.route('/instant_color_name/<name>')
def instant_color_name(name):
    rgb.instant_color_name(name)
    return name


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


@app.route('/snake')
def snake():
    start_process(rgb.snake)
    return 'snake'


@app.route('/snake_gradient')
def snake_gradient():
    start_process(rgb.snake_gradient)
    return 'snake_gradient'


@app.route('/snake_rainbow')
def snake_rainbow():
    start_process(rgb.snake_rainbow)
    return 'snake_rainbow'


@app.route('/strobe/<wait>')
def strobe(wait):
    start_process(rgb.strobe, (int(wait),))
    return 'strobe'


@app.route('/voltage_drop')
def voltage_drop():
    start_process(rgb.voltage_drop)
    return 'voltage_drop'


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

# TODO: Error handling
# TODO: Voice commands
