#!/usr/bin/env bash
# check-and-install.sh
# Installs and starts the test-project service
# Logs to journalctl via logger

# Exit immediately if a command fails
set -e

# Get the directory where the script resides
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="test-project.service"
SCRIPT_NAME="test-project.py"
SERVICE_PATH="/etc/systemd/system"

# Function to log to both console and journalctl
log() {
    echo "$1"
    logger -t "test-project-installer" "$1"
}

log "Starting installation..."
log "Script directory: $SCRIPT_DIR"

# Ensure Python script is executable
if [ -x "${SCRIPT_DIR}/${SCRIPT_NAME}" ]; then
    log "${SCRIPT_NAME} is already executable."
else
    log "Making ${SCRIPT_NAME} executable..."
    chmod +x "${SCRIPT_DIR}/${SCRIPT_NAME}"
fi

# Update service file with correct path and copy it
log "Configuring systemd service file..."
sed "s|/path/to/test-project.py|${SCRIPT_DIR}/${SCRIPT_NAME}|g" \
    "${SCRIPT_DIR}/${SERVICE_NAME}" | \
    sudo tee "${SERVICE_PATH}/${SERVICE_NAME}" > /dev/null

# Reload systemd daemon
log "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable the service
log "Enabling service..."
sudo systemctl enable "${SERVICE_NAME}"

# Start the service
log "Starting service..."
sudo systemctl start "${SERVICE_NAME}"

log "Installation complete. Service is running."
log "View logs with: sudo journalctl -u ${SERVICE_NAME} -f"
log "View installer logs with: sudo journalctl -t test-project-installer"
