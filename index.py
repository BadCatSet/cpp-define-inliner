from flask import Flask, request

from converter import convert

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello from Flask!'


@app.route('/api', methods=['POST'])
def api():
    try:
        data = str(request.data)
        data = convert(data)
        return data
    except Exception as e:
        return str(e)

