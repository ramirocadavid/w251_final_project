import json, argparse, time, base64, cv2
from collections import defaultdict
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with tf.gfile.GFile(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def, name='')

    return graph

app = Flask(__name__)
cors = CORS(app)
graph = load_graph('frozen_inference_graph.pb')

##################################################
# API part
##################################################
@app.route("/predict", methods=['POST'])
def predict():
    print('Starting prediction...', flush=True)

    sess = tf.Session(graph=graph)

    # Define input and output tensors (i.e. data) for the object detection classifier
    # Input tensor is the image
    image_tensor = graph.get_tensor_by_name('image_tensor:0')

    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image where a particular object was detected
    detection_boxes = graph.get_tensor_by_name('detection_boxes:0')

    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image, together with the class label.
    detection_scores = graph.get_tensor_by_name('detection_scores:0')
    detection_classes = graph.get_tensor_by_name('detection_classes:0')

    # Number of objects detected
    num_detections = graph.get_tensor_by_name('num_detections:0')

    imageFile = readb64(request.json['file'])

    # Load image using OpenCV and
    # expand image dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value
    # image = cv2.imread(imageFile)
    image_expanded = np.expand_dims(imageFile, axis=0)

    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})

    # Perform post-processing. As an example, returning the original submitted file
    return jsonify(request.json['file'])


##################################################
# END API part
##################################################

if __name__ == "__main__":
    print('Starting the API')
    app.run()