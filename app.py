import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from main import main, live_results  # Import the main function and live_results from main.py
import live_analysis
from multiprocessing import Process

app = Flask(__name__)

# Folder for uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for uploads
ALLOWED_EXTENSIONS = {'pcap'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        interface = request.form.get('interface')
        print("Interface received:", interface)
        print("Type of interface:", type(interface))

        if interface:
            print("Now App.py Is Calling live_analysis.py and its funstion live_packet_analysis")
            p = Process(target=live_analysis.live_packet_analysis, args=(interface,))
            p.start()
            print(f"Starting live packet analysis on interface: {interface}")
            return redirect(url_for('live_view'))
    interfaces = live_analysis.get_available_interfaces()
    return render_template('index.html', interface_names=interfaces)

@app.route('/live-view')
def live_view():
    # Fetch live packet results
    results = live_results
    return render_template('live.html', live_results=results)  # Pass live_results to the template

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Call the main function from main.py for static analysis
        main(filename=file_path, live=False)
        
        return redirect(url_for('results'))  # Redirect to results page
    return redirect(url_for('index'))

@app.route('/results')
def results():
    # This would normally load and pass analysis results
    # For now, we just show the results page
    return render_template('results.html')

@app.route('/data-feed')
def data_feed():
    if live_results:
        return jsonify(live_results)  # Return live_results if available
    else:
        return jsonify({})  # Return an empty object if live_results is not available


# Main entry point
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
