import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# Initialize the Flask app
app = Flask(__name__)

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    # Render the main page
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    try:
        # Get form inputs and ensure they are numeric
        experience = request.form['experience']
        test_score = request.form['test_score']
        interview_score = request.form['interview_score']

        # Validate and convert inputs to floats
        features = [experience, test_score, interview_score]
        int_features = [float(x) for x in features]  # Convert inputs to floats

        # Prepare features for prediction
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)

        # Format and display the prediction
        output = round(prediction[0], 2)
        return render_template('index.html', prediction_text=f'Employee Salary should be $ {output}')

    except ValueError:
        # Handle invalid input errors
        return render_template('index.html', prediction_text='Invalid input: All features must be numeric')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    '''
    For direct API calls through request
    '''
    data = request.get_json(force=True)
    try:
        # Extract features and ensure they are numeric
        prediction = model.predict([np.array(list(map(float, data.values())))])
        output = prediction[0]
        return jsonify(output)

    except ValueError:
        # Handle invalid API inputs
        return jsonify({"error": "Invalid input: All features must be numeric"})

if __name__ == "__main__":
    app.run(debug=True)