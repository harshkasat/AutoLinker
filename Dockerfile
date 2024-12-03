# # Base image with Python 3.11
# FROM python:3.11-slim

# # Set environment variables to avoid interactive prompts
# ENV DEBIAN_FRONTEND=noninteractive
# ENV DISPLAY=:99

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     wget \
#     curl \
#     unzip \
#     xvfb \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Install Chromium manually
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
#     apt-get install -y ./google-chrome-stable_current_amd64.deb && \
#     rm google-chrome-stable_current_amd64.deb

# # Install ChromeDriver
# RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
#     DRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION%.*}) && \
#     wget -q https://chromedriver.storage.googleapis.com/$DRIVER_VERSION/chromedriver_linux64.zip && \
#     unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
#     rm chromedriver_linux64.zip

# # Set the working directory in the container
# WORKDIR /app

# # Copy Python dependencies configuration file
# COPY requirements.txt /app/

# # Install Python dependencies
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt

# # Copy the script and other project files into the container
# COPY . /app/

# # Command to start Xvfb and run the Selenium script
# CMD ["sh", "-c", "Xvfb :99 & python main.py"]

# Use Selenium's official standalone-chrome image
FROM selenium/standalone-chrome:129.0

# Set the working directory in the container
WORKDIR /app

# Copy Python dependencies configuration file
COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the script and other project files into the container
COPY . /app/

# Define the entry point for the container
CMD ["python3", "main.py"]
