FROM bitnami/spark:3.3

USER root

# Install Python pip and development tools
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev build-essential

# Clean up apt cache
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install Python packages
RUN pip3 install --no-cache-dir -r /app/requirements.txt

USER 1001
