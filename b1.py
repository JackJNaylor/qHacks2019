# system imports
import os
import sys
import subprocess as sp
import threading
import random
import queue
import time

# local imports
import video
import audioStream

# 3rd party imports
from flask import Flask, Response, render_template, request, jsonify
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

# wpm_queue = queue.Queue(maxsize=0)
# transcript_queue = queue.Queue(maxsize=0)
# crutch_queue = queue.Queue(maxsize=0)
wpm = 0
transcript = ''
crutch = {}


def audio_thread():

    time.sleep(10)
    # wpm_queue.put(-1)
    # transcript_queue.put(-1)
    # crutch_queue.put(-1)
    ag = audioStream.AudioGenerator()  # slow background task Thread
    ag.start_stream()
    global wpm
    global transcript
    global crutch
    while ag.is_alive():  # background task still running?
        wpm = ag.get_wpm()
        # wpm_queue.put(ag.get_wpm())
        # crutch_queue.put(ag.get_crutch())
        crutch = ag.get_crutch()
        transcript = ag.get_transcript()
        # transcript_queue.put(ag.get_transcript())
        time.sleep(0.2)


@app.route('/api/wpm')
def get_wpm():
    # wpm = wpm_queue.get()
    global wpm
    # try:
    #     wpm = wpm_queue.get()
    # except queue.Empty:
    #     wpm = -1
    print(wpm)
    return jsonify({'wpm':wpm})


@app.route('/api/transcript')
def get_transcript():
    global transcript
    return jsonify({'transcript': transcript})


@app.route('/api/crutch')
def get_crutch():
    global crutch
    return jsonify({'crutch': crutch})


@app.route('/api/movement')
def get_movement():
    movement = 3
    return jsonify({'movement':movement})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/init', methods=['POST'])
def init():
    # launch threads
    at = threading.Thread(target=audio_thread)
    at.daemon = True 
    if not at.isAlive():
        at.start()
        print("Startng at")

    print("Launching threads")
    # audioStream.ain()
    return "Launched Threads"


@app.route('/start', methods=['POST'])
def start():
    # tell threads to start sending new data
    # OK for main to exit even if thread is still running

    print("STARTTING")
    return "Started"


@app.route('/stop', methods=['POST'])
def stop():
    # tell threads to stop sending data
    at.stop()
    print("Stopping processing")
    # AudioGenerator.stop()
    return "Stopped processing"


@app.route('/video_stream')
def video_stream():
    # Create video stream 
    return Response(video.main(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    init()
    app.run(debug=True)
    # 
    # while True:
    #     print (wpm_queue.get())
    #     time.sleep(0.2)





