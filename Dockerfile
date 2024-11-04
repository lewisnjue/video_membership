# Use the official Python image from Docker Hub
FROM python:latest

# Set the working directory in the container
WORKDIR /video_membership

# Copy only requirements.txt first for caching dependencies
COPY requirements.txt .

# Create a virtual environment and install dependencies
RUN python3 -m venv /opt/env && \
    /opt/env/bin/pip install --upgrade pip && \
    /opt/env/bin/pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application using Uvicorn
CMD ["/opt/env/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
