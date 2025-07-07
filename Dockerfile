# Use a stable Python
FROM python:3.10-slim

# Install build dependencies
RUN pip install --upgrade pip setuptools wheel

# Copy project files
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port (default for Streamlit)
EXPOSE 8501

# Default command to start the app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
