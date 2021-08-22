from flask import Flask
import os

app = Flask(__name__)
if __name__ == "main":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"