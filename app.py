from flask import Flask, render_template, request, jsonify
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__, template_folder='templates.html')


model_1 = load_model('model_1.h5')  
model_2 = load_model('model_2.h5')  
scaler = MinMaxScaler(feature_range=(0, 1))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    selected_year = int(request.form['select_year'])
    
    # Get the last 60 days' closing price values for the selected year
    last_60_days = data[f'{selected_year}-01-01':f'{selected_year}-12-31']['Close'].values
    
    # Use the function to predict the next day's price for both models
    next_day_price_model_1 = predict_next_day_price(model_1, scaler, last_60_days)
    next_day_price_model_2 = predict_next_day_price(model_2, scaler, last_60_days)

    # Other code...

    return render_template('index.html', 
                           prediction_model_1=next_day_price_model_1,
                           prediction_model_2=next_day_price_model_2,
                           selected_year=selected_year)


if __name__ == '__main__':
    app.run(debug=True)
