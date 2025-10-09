#!/bin/bash

##############################################################################
# Budget Lunch Web App - EC2 Deployment Script
# This script automates the deployment process on EC2
##############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv"
APP_FILE="${1:-budget_lunch_local_db.py}"  # Default to budget_lunch_local_db.py
LOG_FILE="$SCRIPT_DIR/app.log"
PID_FILE="$SCRIPT_DIR/app.pid"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Budget Lunch Deployment Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Step 1: Pull latest changes from GitHub
echo -e "${YELLOW}[Step 1/5]${NC} Pulling latest changes from GitHub..."
cd "$SCRIPT_DIR"
git fetch origin
git pull origin main || git pull origin master

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Successfully pulled latest changes${NC}"
else
    echo -e "${RED}✗ Failed to pull changes${NC}"
    exit 1
fi
echo ""

# Step 2: Activate virtual environment
echo -e "${YELLOW}[Step 2/5]${NC} Activating virtual environment..."
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${RED}✗ Virtual environment not found at $VENV_PATH${NC}"
    echo -e "${YELLOW}Creating new virtual environment...${NC}"
    python3 -m venv "$VENV_PATH"
fi

source "$VENV_PATH/bin/activate"
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Step 3: Install dependencies
echo -e "${YELLOW}[Step 3/5]${NC} Installing dependencies..."
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r "$SCRIPT_DIR/requirements.txt"
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠ requirements.txt not found, skipping dependency installation${NC}"
fi
echo ""

# Step 4: Kill running Python process
echo -e "${YELLOW}[Step 4/5]${NC} Stopping existing application..."

# Try to kill using PID file first
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo -e "Killing process with PID: $OLD_PID"
        kill "$OLD_PID" 2>/dev/null || kill -9 "$OLD_PID" 2>/dev/null
        sleep 2
        echo -e "${GREEN}✓ Process stopped${NC}"
    else
        echo -e "${YELLOW}⚠ PID file exists but process not running${NC}"
    fi
    rm -f "$PID_FILE"
fi

# Also kill any process running the app file (backup method)
APP_PIDS=$(pgrep -f "$APP_FILE" || true)
if [ ! -z "$APP_PIDS" ]; then
    echo -e "Found additional processes: $APP_PIDS"
    for pid in $APP_PIDS; do
        kill "$pid" 2>/dev/null || kill -9 "$pid" 2>/dev/null
    done
    sleep 2
    echo -e "${GREEN}✓ All application processes stopped${NC}"
else
    echo -e "${YELLOW}⚠ No running application processes found${NC}"
fi
echo ""

# Step 5: Start the server with nohup
echo -e "${YELLOW}[Step 5/5]${NC} Starting application in background..."
cd "$SCRIPT_DIR"

# Make sure we're in the virtual environment
source "$VENV_PATH/bin/activate"

# Start the application
nohup python3 "$APP_FILE" > "$LOG_FILE" 2>&1 &
NEW_PID=$!

# Save the PID
echo "$NEW_PID" > "$PID_FILE"

# Wait a moment and check if process is still running
sleep 3
if ps -p "$NEW_PID" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Application started successfully${NC}"
    echo -e "${GREEN}  PID: $NEW_PID${NC}"
    echo -e "${GREEN}  Log file: $LOG_FILE${NC}"
    echo -e "${GREEN}  PID file: $PID_FILE${NC}"
else
    echo -e "${RED}✗ Application failed to start${NC}"
    echo -e "${RED}Check the log file for details: $LOG_FILE${NC}"
    exit 1
fi
echo ""

# Display port information
PORT=$(grep -E "port\s*=\s*[0-9]+" "$APP_FILE" | grep -o '[0-9]\+' | head -1)
if [ ! -z "$PORT" ]; then
    echo -e "${GREEN}Application is running on port: $PORT${NC}"
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "To view logs in real-time, run:"
echo -e "  ${YELLOW}tail -f $LOG_FILE${NC}"
echo ""
echo -e "To stop the application, run:"
echo -e "  ${YELLOW}kill \$(cat $PID_FILE)${NC}"
echo ""

