from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
app = Flask(__name__)
model = joblib.load('soc_model.pkl')  # Load the pre-trained model
def preprocess_data(df):
    # Step 1: Drop unnecessary columns and keep the selected ones
    columns_to_keep = ['Time [s]', 'Velocity [km/h]', 'Elevation [m]', 'Throttle [%]',
                       'Motor Torque [Nm]', 'Longitudinal Acceleration [m/s^2]',
                       'Battery Voltage [V]', 'Battery Current [A]', 'Battery Temperature [°C]',
                       'Heating Power CAN [kW]', 'Requested Heating Power [W]', 'AirCon Power [kW]',
                       'Ambient Temperature [°C]', 'Heat Exchanger Temperature [°C]',
                       'Cabin Temperature Sensor [°C]', 'Heater Signal', 'Requested Coolant Temperature [°C]', 'SoC [%]']
    df = df[columns_to_keep]
    
    # Step 2: Apply Min-Max scaling to the specified columns
    min_max_columns = ['Time [s]', 'Velocity [km/h]', 'Elevation [m]', 'Throttle [%]',
                       'AirCon Power [kW]', 'Cabin Temperature Sensor [°C]', 'Battery Temperature [°C]',
                       'Heating Power CAN [kW]', 'Heat Exchanger Temperature [°C]',
                       'Ambient Temperature [°C]', 'Requested Heating Power [W]']
    scaler_min_max = MinMaxScaler()
    df.loc[:, min_max_columns] = scaler_min_max.fit_transform(df[min_max_columns])
    
    # Step 3: Apply Standard scaling to the specified columns
    standard_columns = ['Motor Torque [Nm]', 'Longitudinal Acceleration [m/s^2]',
                        'Battery Voltage [V]', 'Battery Current [A]']
    scaler_standard = StandardScaler()
    df.loc[:, standard_columns] = scaler_standard.fit_transform(df[standard_columns])
    
    # Step 4: Apply One-Hot Encoding to 'Heater Signal' and 'Requested Coolant Temperature [°C]'
    heater_signal_encoded = pd.get_dummies(df['Heater Signal'], prefix='Heater_Signal')
    coolant_temp_encoded = pd.get_dummies(df['Requested Coolant Temperature [°C]'], prefix='Coolant_Temperature')
    df = pd.concat([df, heater_signal_encoded, coolant_temp_encoded], axis=1)
    
    # Step 5: Drop the original categorical columns
    df = df.drop(['Heater Signal', 'Requested Coolant Temperature [°C]'], axis=1)
    
    # Step 6: Convert the one-hot encoded columns to integers
    df[heater_signal_encoded.columns] = df[heater_signal_encoded.columns].astype(int)
    df[coolant_temp_encoded.columns] = df[coolant_temp_encoded.columns].astype(int)
    
    return df

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Parse the incoming JSON request
    input_data = pd.DataFrame(data)  # Convert the input data into DataFrame
    
    # Preprocess the input data before prediction (same preprocessing steps as before)
    input_data = preprocess_data(input_data)  # Ensure to use the same preprocessing function
    prediction = model.predict(input_data)  # Predict the target (SoC)
    
    return jsonify({'predicted_soc': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
