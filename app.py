from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
CORS(app)

@app.route('/favicon.ico')
def favicon():
    return ''


# @app.route('/')
# def index():
#      wp_urls = get_wp_urls()
#      return render_template('index.html', wp_urls=wp_urls)

@app.route('/process', methods=['POST'])
def process():
    try:
        wp_url = request.form.get('wp_url')
        print(f"Received wp_url: {wp_url}")

        api_key = request.form.get('api_key')
        print(f"Received api-key: {api_key}")

        content_prompt = request.form.get('content_prompt', 'default_content_prompt')
        print(f"Received prompt for content generation: {content_prompt}")

        # Check if the request contains an Excel file
        if 'excel_file' not in request.files:
            return jsonify({'error': 'No Excel file provided'}), 400

        excel_file = request.files['excel_file']
        print(f"Received excel_file: {excel_file.filename}")

        # Save the uploaded Excel file
        excel_filename = secure_filename(excel_file.filename)
        excel_path = os.path.join(app.config['UPLOADS_FOLDER'], excel_filename)
        excel_file.save(excel_path)

        

        # Run generate.py with wp_url and excel_path
        command = (
            f"python3 1new-article-working-without-image.py "
            f"--wp_url {wp_url} "
            f"--excel_path {excel_file} "
            f"--content_prompt {content_prompt} "
            f"--api_key {api_key}"
        )

        result = os.system(f"{command} 2>&1 | tee -a {app.config['LOG_FILE']}")

        return jsonify({'result': result}), 200
    
    except KeyError as e:
        return jsonify({'error': f"Missing required form field: {e}"}), 400

    

#@app.route('/run_script', methods=['POST'])
#def run_script(api_key, content_prompt, wp_url, excel_path):
# @app.route('/api/upload_excel', methods=['POST'])
def upload_excel():
    try:
        # Check if the request contains an Excel file
        if 'excel_file' not in request.files:
            return jsonify({'error': 'No Excel file provided'}), 400

        excel_file = request.files['excel_file']
        print(f"Received excel_file: {excel_file.filename}")

        # Save the uploaded Excel file
        excel_filename = secure_filename(excel_file.filename)
        excel_path = os.path.join(app.config['UPLOADS_FOLDER'], excel_filename)
        excel_file.save(excel_path)

        return jsonify({'message': 'Excel file uploaded successfully'}), 200

    except Exception as e:
        return jsonify({'error': f"Error uploading Excel file: {str(e)}"}), 500


@app.route('/api/log_file', methods=['GET'])
def get_log_file():
    log_file_path = app.config['LOG_FILE']
    return send_file(log_file_path, as_attachment=True)



@app.route('/get_wp_urls', methods=['GET'])
def get_wp_urls():
    return jsonify({'wp_urls': read_uploads_json()})

def read_uploads_json():
    try:
        with open("uploads.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []



if __name__ == '__main__':
    app.config['UPLOADS_FOLDER'] = '/home/admin123/Desktop/flask2/UPLOADS_FOLDER'
    app.config['LOG_FILE'] = 'output.log'
    app.run(host="127.0.0.1", port="3000", debug=True)