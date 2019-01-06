import sys
from app.app import get_joke
# load Flask 
import flask

app = flask.Flask(__name__)
@app.route("/joke", methods=["GET"])
def joke():
    return flask.jsonify(get_joke())

def main(args=None):
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    main()
