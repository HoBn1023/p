from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle
import os
import joblib
import contractions
import re 
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

# Initialize Flask app
app = Flask(__name__)
# Function to clean and preprocess the text
def preprocess_text(text):
    text = contractions.fix(text)
    text = re.sub(r'[^\w\s]|\d', '', text.lower().strip())
    words = text.split()
    stop_words = set(stopwords.words('english'))
    cleaned_text = ' '.join(word for word in words if word not in stop_words)
    return cleaned_text

# Load the pre-trained model
model_path = r"C:\Users\houda\Desktop\website\backend\sentiment_modelSVM.pkl"
try:
    model = joblib.load(model_path)
    print("Model loaded successfully.")
except FileNotFoundError:
    print(f"Pickle file not found at {model_path}. Ensure the file path is correct.")
    model = None
except joblib.JoblibException:
    print("Error unpickling the file. The file might be corrupted or not a pickle file.")
    model = None
except Exception as e:
    print(f"An error occurred: {e}")
    model = None

@app.route('/')
def index():
    return render_template('index.html')

# Define the Flask route
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded. Check server logs for details."}), 500
    
    try:
        json_ = request.json
        query_df = pd.DataFrame(json_)
        query_texts = query_df['text'].apply(preprocess_text)  # Ensure you preprocess the text similarly as during training
        prediction = model.predict(query_texts)
        prediction = prediction.tolist()  # Convert prediction to list for JSON serialization
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)