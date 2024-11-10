#!/bin/bash

# Print ASCII art banner
echo "  _                       ____               _               _             _   _____   _____   _____ "
echo " | |_    __ _     _      / __ \\  __      __ | |__     __ _  | |_   ____   / | |___ /  |___ /  |___  |"
echo " | __|  / _\` |   (_)    / / _\` | \\ \\ /\\ / / | '_ \\   / _\` | | __| |_  /   | |   |_ \\    |_ \\     / / "
echo " | |_  | (_| |    _    | | (_| |  \\ V  V /  | | | | | (_| | | |_   / /    | |  ___) |  ___) |   / /  "
echo "  \\__|  \\__, |   (_)    \\ \\__,_|   \\_/\\_/   |_| |_|  \\__,_|  \\__| /___|   |_| |____/  |____/   /_/   "
echo "        |___/            \\____/                                                                 "

# Update package list and install required packages
echo "Updating package list..."
sudo apt update -y

# Install Python and venv
echo "Installing Python 3 and venv..."
sudo apt install python3 python3-venv python3-pip -y


# Set up a virtual environment
echo "Setting up a virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

# Install libraries (modify the list as needed)
echo "Installing required libraries..."
pip install --upgrade pip
pip install flask playwright requests logging pystyle Flask-CloudflareRemote # Add other libraries here

playwright install-deps
playwright install chromium


sudo apt update
sudo apt install screen
screen

# Provide instructions
echo "Virtual environment setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"
echo "To deactivate, simply run: deactivate"
echo "with love by @whatzwasthere"
echo "place 'certificate.crt', 'certificate.key' to enable HTTPS protocol (TLS v1_2) "


echo "  _                       ____               _               _             _   _____   _____   _____ "
echo " | |_    __ _     _      / __ \\  __      __ | |__     __ _  | |_   ____   / | |___ /  |___ /  |___  |"
echo " | __|  / _\` |   (_)    / / _\` | \\ \\ /\\ / / | '_ \\   / _\` | | __| |_  /   | |   |_ \\    |_ \\     / / "
echo " | |_  | (_| |    _    | | (_| |  \\ V  V /  | | | | | (_| | | |_   / /    | |  ___) |  ___) |   / /  "
echo "  \\__|  \\__, |   (_)    \\ \\__,_|   \\_/\\_/   |_| |_|  \\__,_|  \\__| /___|   |_| |____/  |____/   /_/   "
echo "        |___/            \\____/                                                                 "

source ./venv/bin/activate 
python main.py
