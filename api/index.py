import os

from flask import Flask, request, render_template, send_from_directory

from converter import convert

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# for checking if server is up
@app.route("/sanity", methods=["GET", "POST"])
def index_post():
    return "Hi mom!"


@app.route("/api", methods=["POST"])
def api():
    try:
        data = bytes.decode(request.data)
        data = data.replace("\r\n", "\n")
        data = convert(data)
        return data
    except Exception as e:
        return str(e)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'hash_5.png', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
