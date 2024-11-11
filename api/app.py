from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import joblib
from utils.modelling import prepare_model_data


app = Flask(__name__)

CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    data = prepare_model_data(data)
    
    print(data.info())
    
    preprocessor = joblib.load('api\preprocessor.pkl')
    
    X_preprocesseed = preprocessor.transform(data)
    
    model = joblib.load('api\model.pkl')
    
    prediction = model.predict(X_preprocesseed)
    
    is_fraud = prediction.tolist()[0]
    
    return jsonify({'is_fraud': is_fraud}), 200


if __name__ == '__main__':
    app.run(debug=True)