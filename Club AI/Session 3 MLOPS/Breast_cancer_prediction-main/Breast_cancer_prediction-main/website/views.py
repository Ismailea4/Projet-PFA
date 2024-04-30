from flask import Blueprint, render_template, request
import pandas as pd

import joblib

views = Blueprint('views', __name__)

# Load the model
svm = joblib.load('svm_model.pkl')

# Load the scaler
scaler = joblib.load('scaler.pkl')

# Load the csv file and get the columns
df = pd.read_csv('breast-cancer.csv')
columns = df.columns[2:].tolist()
columns_mean = columns[:10]
columns_se = columns[10:20]
columns_worst = columns[20:] 

@views.route('/', methods=['GET', 'POST'])
def index():

    print(columns_mean)
    print(columns_worst)
    print(columns_se)

    if request.method == 'POST':

        #  Check if all the fields are filled
        for column in columns:
            if request.form[column] == '':
                return render_template('index.html', error="Please fill all the fields", columns_mean=columns_mean, columns_se=columns_se, columns_worst=columns_worst)
       
        # Get the data from the form
        input_data = []
        for column in columns:
            input_data.append(float(request.form[column]))
       
        # Scale the data
        input_data = scaler.transform([input_data])

        # Make the prediction
        prediction = svm.predict(input_data)

        # Return the result
        if prediction[0] == 1:
            result = "Malignant"
        else:
            result = "Benign"

        print(result)

        return render_template('index.html', result=result, columns_mean=columns_mean, columns_se=columns_se, columns_worst=columns_worst)
    
    return render_template('index.html', columns_mean=columns_mean, columns_se=columns_se, columns_worst=columns_worst)
