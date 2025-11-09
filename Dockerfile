# Use official Python image
FROM python:3.12-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Create the app directory
RUN mkdir /app

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the code
COPY . /app/

# Run Django dev server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
