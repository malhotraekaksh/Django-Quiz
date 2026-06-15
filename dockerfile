# Use Python base image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy project into container
COPY . /app

# Install Django dependencies
RUN pip install django

# Open port for Django
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
