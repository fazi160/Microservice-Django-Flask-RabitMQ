# Use the official Python image as the base
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app runs on
EXPOSE 5000

# Set the default command to run the app
# CMD ["python", "main.py"]
