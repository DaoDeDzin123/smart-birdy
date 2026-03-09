# Use an official Python runtime as a parent image, using a specific version and the slim variant
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port your app runs on (change if necessary, e.g., 5000 for Flask)
EXPOSE 8000

# Define the command to run the application when the container launches
CMD ["python", "main.py"]