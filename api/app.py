from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from utils.modelling import prepare_model_data


app = Flask(__name__)

CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    data = prepare_model_data(data)
    print(data)
    
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)