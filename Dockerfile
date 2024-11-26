# Step 1: Use a Python base image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install the dependencies from the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose the port that the Flask app will run on
EXPOSE 5000

# Step 6: Define the command to run the Flask app
CMD ["python", "app.py"]
