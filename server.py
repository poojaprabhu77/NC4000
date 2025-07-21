
from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import logging
import os
import json

#app = Flask(__name__, static_folder=os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, static_folder="static")
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


@app.route('/submit', methods=['POST'])
def submit():
    param = request.json.get('param')
    app.logger.info(f"Received param: {param}")
    if not param:
        return jsonify({'error': 'Missing parameter'}), 400
    # Store only the link string in link.json
    with open(os.path.join(BASE_DIR, 'link.json'), 'w') as fl:
        fl.write(param)
    print(param)
    return jsonify({'received': param}), 200

@app.route('/data', methods=['GET'])
def get_data(): 
    try:
        with open(os.path.join(BASE_DIR, 'link.json'), 'r') as f:
            link = f.read().strip()
        return jsonify({'link': link}), 200
    except FileNotFoundError:
        return jsonify({'error': 'Data file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5000, debug=False)
