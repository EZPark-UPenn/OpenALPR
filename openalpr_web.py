from flask import Flask, jsonify, request
import json
import urllib
from base64 import b64encode
import requests

from openalpr import Alpr
import openalpr

import time

import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hello world!"

@app.route('/alpr', methods = ['POST'])
def alpr():
    start_time = time.time();
    try:
        print 'recieved image, processing...'

        alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
        alpr.set_top_n(20)

        mid1_time = time.time();

        if 'image' not in request.files:
            print "image was not in files"
            return 'Image parameter not provided'

        jpeg_bytes = request.files['image'].read()

        if len(jpeg_bytes) <= 0:
            print "there are no bytes!"
            return False

        mid2_time = time.time();

        results = alpr.recognize_array(jpeg_bytes)

        print "got results!"

        end_time = time.time();

        print("total_time: " + str(end_time-start_time));
        print("alpr_time: " + str(mid1_time-start_time));
        print("jpeg_time: " + str(mid2_time-mid1_time));
        print("processing_time: " + str(end_time-mid2_time));

        return jsonify(results)
    except Exception, e:
        print e
        raise e
    

if __name__ == "__main__":
    app.run(debug = True)