FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    g++ \
    libpq-dev \
    python3-dev \
    python3-pip

# Copy application code to the container image
WORKDIR /
COPY . .

# Install production dependencies
RUN pipenv install

# Run the web service on container startup
CMD ["python", "web/app.py"]
