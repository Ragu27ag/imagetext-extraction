# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Set working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 5000 for the Flask application
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
