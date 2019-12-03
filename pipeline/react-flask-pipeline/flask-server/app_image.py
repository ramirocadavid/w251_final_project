from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from importlib import import_module
import os
from flask import Flask, render_template, Response

import cv2
import tensorflow as tf
from im_transf_net import create_net
import numpy as np
import argparse
import utils

import base64
from PIL import Image
import skimage
from io import BytesIO


def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

def tob64(image) -> str:
    with BytesIO() as output_bytes:
        PIL_image = Image.fromarray(skimage.img_as_ubyte(image / 255))
        PIL_image.save(output_bytes, 'JPEG') # Note JPG is not a vaild type here
        bytes_data = output_bytes.getvalue()

    return bytes_data

app = Flask(__name__)


@app.route("/image", methods=['POST'])
def image():
    print('Starting prediction...', flush=True)
    
    img = readb64(request.json['file'])

    # Read + preprocess input image.
    #img = utils.imread(input_img_path)
    #img = utils.imresize(img, content_target_resize)
    img_4d = img[np.newaxis, :]

    # Create the graph.
    with tf.variable_scope('img_t_net'):
        X = tf.placeholder(tf.float32, shape=img_4d.shape, name='input')
        Y = create_net(X, 'resize') # upsample_method, default 'resize'

    # Saver used to restore the model to the session.
    saver = tf.train.Saver()

    # Filter the input image.
    with tf.Session() as sess:
        print('Loading up model...', flush=True)
        saver.restore(sess, './models_fast/starrynight_final.ckpt') # model path
        print('Evaluating...', flush=True)
        img_out = sess.run(Y, feed_dict={X: img_4d})
        print(img_out[:2], flush=True)

    # Postprocess + save the output image.
    print('Saving image.', flush=True)
    img_out = np.squeeze(img_out)    

    # Perform post-processing. As an example, returning the original submitted file
    resp = jsonify(tob64(img_out))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.after_request
def after_request(r):
    print(r.mimetype)
    r.direct_passthrough = False
    print(r.get_data()[:200], flush=True)
    return r

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
