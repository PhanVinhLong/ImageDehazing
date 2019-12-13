from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import atexit
import collections
import cv2
import os
import signal
import time

import flask
import numpy as np
import scipy.misc as sic
from PIL import Image

from werkzeug.utils import secure_filename

parser = argparse.ArgumentParser()
parser.add_argument("--output_dir", default='./static/images', help="output folder [DO NOT CHANGE]")
args = parser.parse_args()

# Check the output directory to save the checkpoint
if not os.path.exists(args.output_dir):
    os.mkdir(args.output_dir)

app = flask.Flask(__name__)


def handle_exit():
    print('------------------------ Exiting ------------------------')

@app.route('/')
def index():
    return flask.render_template("index.html")


@app.route('/error')
def image_not_found():
    return None


# TODO: Take multiple images
@app.route('/dehaze', methods=['POST'])
def dehaze():
    start = time.time()
    image = flask.request.files['image']
    model = flask.request.form['model']
    image_name = None
    image_path = None

    if image:
        image_name = secure_filename(image.filename)
        image_path = os.path.join(args.output_dir, image_name)
        image.save(image_path)
    else:
        return flask.redirect(flask.url_for('image_not_found'))

    dehazed_path = image_path
    print("image_path:", image_path)
    input_im = Image.open(image_path)

    return flask.jsonify({
        "real": image_path,
        "dehazed": dehazed_path,
    })


atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

if __name__ == '__main__':
    app.run(debug=True)
