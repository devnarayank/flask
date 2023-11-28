from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
CORS(app, origins=" http://localhost:3000")

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
        excel_file = request.files['excel_file']
        print(f"Received excel_file: {excel_file.filename}")
        api_key = request.form.get('api_key')
        print(f"received api-key: {api_key}")
        
        content_prompt = request.form.get('content_prompt', 'default_content_prompt')
        print(f"recieved prompt for content generation: {content_prompt}")


        # Save the uploaded Excel file
        excel_filename = secure_filename(excel_file.filename)
        excel_path = os.path.join(app.config['UPLOADS_FOLDER'], excel_filename)
        excel_file.save(excel_path)

        # Run generate.py with wp_url and excel_path
        command = f"python3 1new-article-working-without-image.py --wp_url {wp_url} --excel_path {excel_path}"

        os.system(f"{command} 2>&1 | tee -a {app.config['LOG_FILE']}")

        result = process(wp_url, api_key, content_prompt, excel_path)
        
        # if(result.status == 200):
        #     print("article generated successfully", result)
        
        return redirect(url_for('index'))
    
    except KeyError as e:
          return jsonify({'error': f"Missing required form field: {e}"}), 400


    

#@app.route('/run_script', methods=['POST'])
#def run_script(api_key, content_prompt, wp_url, excel_path):

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
    app.run(debug=True)

