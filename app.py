import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from multiprocessing import Process, set_start_method
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import live_analysis
import features  # Assuming 'features' is a module that handles pcap file analysis

def create_app():
    app = Flask(__name__)
    CORS(app)
    socketio = SocketIO(app)

    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = {'pcap', 'pcapng'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def clear_images_directory():
        image_dir = os.path.join(app.static_folder, 'images')
        for img_file in os.listdir(image_dir):
            os.remove(os.path.join(image_dir, img_file))
        print("Cleared all images in the directory.")

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/start', methods=['POST'])
    def start_analysis():
        interface = "\\Device\\NPF_{3958AAE7-B2D7-4302-9F76-EA8AD698D618}"
        p = Process(target=live_analysis.start_live_analysis, args=(interface,))
        p.start()
        return redirect(url_for('live_view'))

    @app.route('/live-view')
    def live_view():
        return render_template('live.html')

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            print("No file part in the request")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print("No file selected for upload")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            clear_images_directory()
            results = features.main(file_path)
            if results:
                return redirect(url_for('results'))
            else:
                print("Analysis failed. Check the file format and content.")
        else:
            print("Uploaded file not allowed or no file found")
        return redirect(url_for('index'))

    @app.route('/results')
    def results():
        image_dir = os.path.join(app.static_folder, 'images')
        image_files = {img: img for img in os.listdir(image_dir)}
        return render_template('results.html', images=image_files)

    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    def send_live_data():
        while True:
            live_data = live_analysis.get_live_results()
            if live_data:
                socketio.emit('live_data', live_data)
            socketio.sleep(1)

    live_data_thread = socketio.start_background_task(target=send_live_data)

    return app, socketio

if __name__ == '__main__':
    set_start_method('spawn')
    app, socketio = create_app()
    socketio.run(app, debug=True)
