# Use the official Python runtime image
FROM python:3.13-slim

# Create the Liine directory
RUN mkdir /Liine

# Set the working directory inside the container
WORKDIR /Liine

# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1

#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# Copy the Django project  and install dependencies
COPY requirements.txt  /Liine/

# run this command to install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project to the container
COPY . /Liine/

# Copy the CSV file into the container
COPY data/restaurants.csv /tmp/restaurants.csv

# Update package list and install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Run a Python script that processes the CSV
# CMD ["python", "process_csv.py"]

# Expose the Django port
EXPOSE 8000

# Run Django’s development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]