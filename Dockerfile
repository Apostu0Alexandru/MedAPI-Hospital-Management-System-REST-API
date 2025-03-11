# Use Python slim image as base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose port 8000 for the application
EXPOSE 8000

# Run migrations and collect static files during build (optional)
RUN mkdir -p /app/staticfiles && chmod 755 /app/staticfiles
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Run the application using Gunicorn
CMD ["gunicorn", "hospital_management.wsgi:application", "--bind", "0.0.0.0:8000"]
