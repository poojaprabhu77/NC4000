from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
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
        return jsonify({'error': 'No data available'}), 404
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
