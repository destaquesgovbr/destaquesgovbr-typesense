# Typesense with HuggingFace GovBR News Dataset
FROM typesense/typesense:27.1

# Install Python, pip, and build dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment for Python dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create app directory
WORKDIR /app

# Copy package files and install
COPY pyproject.toml /app/
COPY src/ /app/src/
COPY scripts/ /app/scripts/
COPY requirements.txt /app/

# Install dependencies and the package
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

# Copy entrypoint script
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh

# Set environment variables for Typesense
ENV TYPESENSE_API_KEY=govbrnews_api_key_change_in_production
ENV TYPESENSE_DATA_DIR=/data
ENV PYTHONPATH=/app/src

# Create data directory
RUN mkdir -p /data

# Expose Typesense port
EXPOSE 8108

# Use custom entrypoint
ENTRYPOINT ["/opt/entrypoint.sh"]
