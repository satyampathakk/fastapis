#!/bin/bash

# Update package list and install Tor
echo "Updating package list and installing Tor..."
sudo apt-get update
sudo apt-get install -y tor

# Define the path to the torrc file
TORRC_FILE="/etc/tor/torrc"

# Backup the original torrc file
echo "Backing up the original torrc file..."
sudo cp $TORRC_FILE ${TORRC_FILE}.bak

# Uncomment or add hidden service configuration in torrc
echo "Configuring the torrc file for hidden services..."

# Add hidden service configuration if not present
{
  echo ""
  echo "# Hidden Service Configuration"
  echo "HiddenServiceDir /var/lib/tor/hidden_service/"
  echo "HiddenServicePort 80 127.0.0.1:8000"  # Change port and destination if needed
} | sudo tee -a $TORRC_FILE

# Ensure the HiddenServiceDir exists and has the correct permissions
sudo mkdir -p /var/lib/tor/hidden_service
sudo chown debian-tor:debian-tor /var/lib/tor/hidden_service

# Restart Tor service to apply changes
echo "Restarting Tor service..."
sudo systemctl restart tor

# Show the hidden service hostname
echo "Hidden service hostname:"
sudo cat /var/lib/tor/hidden_service/hostname

echo "Tor installation and configuration for hidden services completed."
