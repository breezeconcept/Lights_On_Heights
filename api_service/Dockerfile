# Use official Python image
FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Copy the application
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Run using Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
