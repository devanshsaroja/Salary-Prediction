from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the pickled model and scalers
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler_X.pkl', 'rb') as f:
    scaler_X = pickle.load(f)

with open('scaler_y.pkl', 'rb') as f:
    scaler_y = pickle.load(f)

print("Model and scalers loaded successfully.")

# Function to predict salary using the loaded model and scalers
def predict_salary(i_date, i_month, i_year):
    X_pred = scaler_X.transform(np.array([[i_date, i_month, i_year]]))  # Correct scaling
    y_pred_scale = model.predict(X_pred)  # Make prediction
    y_pred = scaler_y.inverse_transform(y_pred_scale.reshape(-1, 1)).flatten()  # Inverse scaling
    return y_pred[0]

# Home route to render the form and display prediction result
@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_salary = None  # Default value to None
    error_message = None  # Default error message to None
    if request.method == 'POST':
        try:
            # Get inputs from form data
            i_date = int(request.form['date'])
            i_month = int(request.form['month'])
            i_year = int(request.form['year'])

            # Server-side validation
            if i_date < 1 or i_date > 30:
                raise ValueError("Day must be between 1 and 30.")
            if i_month < 1 or i_month > 12:
                raise ValueError("Month must be between 1 and 12.")
            if i_year < 1952:
                raise ValueError("Year must be at least 1952.")

            print(f"Inputs received: Date = {i_date}, Month = {i_month}, Year = {i_year}")  # Debugging log

            # Call the prediction function
            predicted_salary = predict_salary(i_date, i_month, i_year)

        except ValueError as ve:
            error_message = f"Value error: {ve}"
            print(error_message)
        except Exception as e:
            error_message = f"An error occurred: {e}"
            print(error_message)

    return render_template('index.html', predicted_salary=predicted_salary, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
