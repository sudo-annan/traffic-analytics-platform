#!/usr/bin/env bash
set -e

echo "=== System Update ==="
sudo apt update && sudo apt upgrade -y

echo "=== Install essentials ==="
sudo apt install -y build-essential git curl wget unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release

echo "=== Install Python 3.11 and pip ==="
sudo apt install -y python3.11 python3.11-venv python3.11-dev
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3

echo "=== Create Python virtual environment ==="
python3 -m venv ~/.venvs/traffic_env
source ~/.venvs/traffic_env/bin/activate
pip install --upgrade pip wheel setuptools

echo "=== Install core Python packages ==="
pip install fastapi uvicorn[standard] requests opencv-python numpy pandas selenium undetected-chromedriver pillow matplotlib

echo "=== Install Node.js (v20 LTS) via nvm ==="
if [ ! -d "$HOME/.nvm" ]; then
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
fi
nvm install 20
nvm use 20

echo "=== Install Docker CE and Compose ==="
sudo apt remove -y docker docker-engine docker.io containerd runc || true
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker

echo "=== Verify Docker ==="
docker --version
docker compose version

echo "=== Install Google Chrome and ChromeDriver ==="
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb

CHROME_VERSION=$(google-chrome --version | grep -oP '[0-9]+' | head -1)
CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE")
wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip"
unzip -q chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
rm -rf chromedriver-linux64.zip chromedriver-linux64
chromedriver --version

echo "=== Install ngrok (for local exposure) ==="
wget -q https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.tgz
tar xzf ngrok-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/
rm ngrok-stable-linux-amd64.tgz
ngrok version

echo "=== Setup complete! ==="
echo "To activate your Python env each session:"
echo "source ~/.venvs/traffic_env/bin/activate"
