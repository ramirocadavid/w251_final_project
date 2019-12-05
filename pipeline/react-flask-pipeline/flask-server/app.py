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
    # convert image to bytes
    with BytesIO() as output_bytes:
        PIL_image = Image.fromarray(skimage.img_as_ubyte(image / 255))
        PIL_image.save(output_bytes, 'JPEG') # Note JPG is not a vaild type here
        bytes_data = output_bytes.getvalue()

    # encode bytes to base64 string
    base64_str = str(base64.b64encode(bytes_data), 'utf-8')
    return 'data:image/jpeg;base64,' + base64_str

    return base64_str

app = Flask(__name__)
cors = CORS(app)


@app.route("/image", methods=['POST'])
def image():
    print('Starting prediction...', flush=True)
    
    img = readb64(request.json['file'])
    model = request.headers['Type']

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
        saver.restore(sess, './models_fast/' + model + '.ckpt') # model path
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
    # return jsonify(tob64(img_out))


@app.route('/video', methods=['POST'])
def video():
    # Load video
    data = request.files['file'].read()
    model = request.headers['Type']
    print(model, flush=True)

    with open('video.mp4', 'wb') as out_file:
        out_file.write(data)

    video_stream = cv2.VideoCapture('video.mp4')

    # Command-line argument parsing.
    model_path = './models_fast/' + model + '.ckpt'
    upsample_method = 'resize'
    resolution = None

    # # Instantiate video capture object.
    # cap = cv2.VideoCapture(0)

    # Set resolution
    if resolution is not None:
        x_length, y_length = resolution
        video_stream.set(3, x_length)  # 3 and 4 are OpenCV property IDs.
        video_stream.set(4, y_length)
    x_new = int(video_stream.get(3))
    y_new = int(video_stream.get(4))
    print ('Resolution is: {0} by {1}'.format(x_new, y_new), flush=True)

    # Create the graph.
    shape = [1, y_new, x_new, 3]
    with tf.variable_scope('img_t_net'):
        X = tf.placeholder(tf.float32, shape=shape, name='input')
        Y = create_net(X, upsample_method)
    print ("step1", flush=True)
    # Saver used to restore the model to the session.
    saver = tf.train.Saver()

    with tf.Session() as sess:
        print ("Loading up model...", flush=True)
        saver.restore(sess, model_path)
        print ('Begin filtering...')
        
        """Video streaming generator function."""
        currentFrame = 0
        # Get current width of frame
        width = video_stream.get(3)   # float
        # Get current height of frame
        height = video_stream.get(4) # float

        # Define the codec and create VideoWriter object
        #fourcc = cv2.VideoWriter_fourcc(*'X264')
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        FILE_OUTPUT = 'video_stylized.mp4'
        out = cv2.VideoWriter(FILE_OUTPUT, fourcc, 20.0, (int(width), int(height)))
        #out = cv2.VideoWriter(FILE_OUTPUT, fourcc, 20.0, (x_new, y_new))
        while video_stream.isOpened():
            ret, frame = video_stream.read()

            if ret:
                # Make frame 4-D
                img_4d = frame[np.newaxis, :]

                # Our operations on the frame come here
                img_out = sess.run(Y, feed_dict={X: img_4d})
                img_out = np.squeeze(img_out).astype(np.uint8)
                img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)

                out.write(img_out)
            else:
                break

        print("\nCHECKPOINT\n", flush=True)
        video_stream.release()
        out.release()
            
    # resp = send_file(FILE_OUTPUT, mimetype='video/mp4', attachment_filename='video.mp4')
    resp = send_file(FILE_OUTPUT)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.after_request
def after_request(r):
    print(r.mimetype)
    r.direct_passthrough = False
    print(r.get_data()[:200], flush=True)
    return r

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
