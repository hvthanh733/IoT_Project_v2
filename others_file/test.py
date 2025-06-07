from flask import Flask, Response
import time

app = Flask(__name__)

def count_to_100():
    def generate():
        for i in range(1, 101):
            yield f"data:{i}\n\n"
            time.sleep(1)
    return Response(generate(), mimetype='text/event-stream')

