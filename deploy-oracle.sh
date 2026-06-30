#!/bin/bash
# Oracle Cloud Free Tier deployment script for yt-dlp backend
# Run this ON your Oracle Cloud VM after SSH-ing in

set -e

echo "=== Installing Docker ==="
sudo apt-get update
sudo apt-get install -y docker.io docker-compose git
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

echo "=== Cloning backend ==="
cd /opt
sudo git clone https://github.com/sanjusajan-creator/yt-dlp.git ytdlp-backend
sudo chown -R $USER:$USER ytdlp-backend
cd ytdlp-backend

echo "=== Setting up cookies ==="
read -p "Paste your YT_COOKIES_B64 value: " COOKIES_B64
echo "YT_COOKIES_B64=$COOKIES_B64" > .env

echo "=== Building and starting ==="
docker-compose up -d --build

echo "=== Testing ==="
sleep 10
curl -s http://localhost:8000/debug/cookies

echo ""
echo "=== Done! ==="
echo "Your API is running at http://YOUR_VM_IP:8000"
echo "Test with: curl http://YOUR_VM_IP:8000/audio?video_id=dQw4w9WgXcQ"
