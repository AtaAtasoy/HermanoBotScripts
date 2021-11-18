from flask import Flask
import os
from volleyball import volleyball_module
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.register_blueprint(volleyball_module, url_prefix = '/volleyball')

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
