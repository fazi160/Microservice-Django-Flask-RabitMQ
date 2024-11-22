FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Install system dependencies required for mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean

# Copy and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Command to start the Django server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
