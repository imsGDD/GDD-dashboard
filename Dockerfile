# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # psycopg2 dependencies
    && apt-get install -y libpq-dev \
    # Translations dependencies
    && apt-get install -y gettext \
    && apt-get install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info \
    && apt-get install -y python3-psycopg2 \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in Docker
WORKDIR /app

# Install pip3
RUN apt-get update \
    && apt-get install -y python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install any dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /app/
RUN mkdir -p /app/logs

## Add binaries to path
#ENV PATH="/app/tools/binaries:${PATH}"
#RUN chmod +x /app/tools/binaries/*

# Install Gunicorn
RUN pip install gunicorn

# Run the application
EXPOSE 80
CMD ["sh", "./runserver.sh"]

