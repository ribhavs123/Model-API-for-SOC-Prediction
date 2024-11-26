# Model-API-for-SOC-Prediction

This repository provides a Flask-based API to serve a pre-trained machine learning model for predicting the State of Charge (SOC). The model is wrapped inside a Docker container, making it easy to deploy and interact with.

Requirements
Before running the API, ensure you have the following dependencies installed:

Docker (for containerization)
Python 3.9+
Necessary Python packages listed in requirements.txt



Steps to Get Started
1. Clone the Repository
      - First, clone this repository to your local machine.

2. Install Dependencies
      - Make sure to install the necessary Python packages. You can do this by running the following command:
        pip install -r requirements.txt

3. Build the Docker image:

      - In your project directory, run the following command:
    
        docker build -t soc_model_api .
        Run the Docker container:
    
      - After building the image, you can run the Docker container with the following command:
        
        docker run -p 5000:5000 soc_model_api
        This will start the Flask API on port 5000, which you can access via http://localhost:5000.
    
4.Running the Application
      - Once the model is properly loaded, you can run the Flask application by simply running:
    
        python app.py

5. API Endpoints
      - curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"input_data": [your_data_here]}'
        
6. Stopping the Docker Container
      - If you're running the application in Docker, you can stop the container using:
          docker stop <container_id>

