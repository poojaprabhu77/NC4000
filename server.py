@app.route('/frontend')
def frontend_redirect():
    return redirect('/frontend.html')

@app.route('/frontend.html')
def serve_frontend():
    return send_from_directory(BASE_DIR, 'frontend.html')
from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import logging

import os
app = Flask(__name__, static_folder=os.path.dirname(os.path.abspath(__file__)))
# Use a more robust storage for production (e.g., database)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def root():
    # Redirect to index.html
    return redirect('/index.html')

@app.route('/index.html')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')

# Add /frontend redirect and serve
@app.route('/frontend')
def frontend_redirect():
    return redirect('/frontend.html')

@app.route('/frontend.html')
def serve_frontend():
    return send_from_directory(BASE_DIR, 'frontend.html')
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Use a more robust storage for production (e.g., database)
data = None

@app.route('/submit', methods=['POST'])
def submit():
    global data
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    param = request.json.get('param')
    app.logger.info(f"Received param: {param}")
    if not param:
        return jsonify({'error': 'Missing parameter'}), 400
    data = {'link': param}
    return jsonify({'received': param}), 200

@app.route('/data', methods=['GET'])
def get_data():
    global data
    if data is None:
        # Return a default link if no data has been submitted
        return jsonify({'link': 'https://your-default-tracking-link.com'}), 200
    return jsonify(data), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5000, debug=False)
