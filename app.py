from flask import Flask, render_template
import os
import pathlib
import json

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'static'))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
