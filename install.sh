#!/bin/bash

# Create a virtual environment (optional)
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install fastapi[all] sqlalchemy psutil

# You can add other dependencies as needed
echo "All dependencies installed."

# Create a systemd service file
SERVICE_NAME="chatapi.service"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME"

# Write the service file
echo "[Unit]
Description=FastAPI Application
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/uvicorn main:app --host 0.0.0.0 --port 80 --reload
Restart=always

[Install]
WantedBy=multi-user.target" | sudo tee $SERVICE_FILE

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable $SERVICE_NAME

# Start the service
sudo systemctl start $SERVICE_NAME

echo "Service $SERVICE_NAME created and started successfully."
