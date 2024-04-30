# app.py

import os
from flask import Flask, render_template, request
import main  # Import the main module

app = Flask(__name__)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = os.path.join('uploads', file.filename)
            file.save(filename)
            images = main.main(filename)  # Assume main returns list of image paths
            return render_template('result.html', images=images)
    return render_template('index.html')

# Main entry point
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
