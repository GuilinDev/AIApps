# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the wait-for-it script
COPY wait-for-it.sh /app/wait-for-it.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run wait-for-it.sh when the container launches
CMD ["./wait-for-it.sh", "db", "--", "python", "app.py"]
