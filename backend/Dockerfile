# ---- Base Python image ----
FROM python:3.11-slim

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# ---- Install system dependencies ----
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg ca-certificates \
    libglib2.0-0 libnss3 libxss1 libasound2 libxtst6 \
    libgtk-3-0 libx11-xcb1 libxcomposite1 libxcursor1 libxi6 libxrandr2 libxdamage1 libxext6 libxfixes3 \
    fonts-liberation xdg-utils xvfb \
    && rm -rf /var/lib/apt/lists/*

# ---- Install Google Chrome ----
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
      > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# ---- Environment variables for Chrome / Selenium ----
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# ---- Working directory ----
WORKDIR /app

# ---- Install Python dependencies ----
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r /app/requirements.txt

# ---- Copy project files ----
COPY backend/app /app/app
COPY src /app/src
COPY data /app/data

# ---- Expose FastAPI port ----
EXPOSE 8000

# ---- Run the FastAPI server ----
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]