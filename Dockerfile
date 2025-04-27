# Use an official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHON_VERSION=3.11

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

RUN python manage.py collectstatic --noinput

# Expose port 8000 for Django
EXPOSE 8000

# Start server
CMD ["gunicorn", "libraryproject.wsgi:application", "--bind", "0.0.0.0:8000"]
