#!/bin/bash

##############################################################################
# Budget Lunch Web App - Management Script
# Quick commands to manage the application
##############################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/app.pid"
LOG_FILE="$SCRIPT_DIR/app.log"

# Function to check if app is running
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0
        fi
    fi
    return 1
}

# Function to get status
status() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Application Status${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    if is_running; then
        PID=$(cat "$PID_FILE")
        echo -e "${GREEN}✓ Application is RUNNING${NC}"
        echo -e "  PID: $PID"
        
        # Get port info
        PORT=$(lsof -Pan -p "$PID" -i 2>/dev/null | grep LISTEN | awk '{print $9}' | cut -d: -f2 | head -1)
        if [ ! -z "$PORT" ]; then
            echo -e "  Port: $PORT"
        fi
        
        # Get uptime
        START_TIME=$(ps -p "$PID" -o lstart= 2>/dev/null)
        if [ ! -z "$START_TIME" ]; then
            echo -e "  Started: $START_TIME"
        fi
        
        # Memory usage
        MEM=$(ps -p "$PID" -o rss= 2>/dev/null)
        if [ ! -z "$MEM" ]; then
            MEM_MB=$((MEM / 1024))
            echo -e "  Memory: ${MEM_MB}MB"
        fi
    else
        echo -e "${RED}✗ Application is NOT running${NC}"
    fi
    
    if [ -f "$LOG_FILE" ]; then
        echo -e "\nLog file: $LOG_FILE"
        LOG_SIZE=$(du -h "$LOG_FILE" | cut -f1)
        echo -e "Log size: $LOG_SIZE"
    fi
    echo ""
}

# Function to stop app
stop() {
    echo -e "${YELLOW}Stopping application...${NC}"
    
    if is_running; then
        PID=$(cat "$PID_FILE")
        echo -e "Killing process $PID..."
        kill "$PID" 2>/dev/null || kill -9 "$PID" 2>/dev/null
        sleep 2
        
        if is_running; then
            echo -e "${RED}✗ Failed to stop application${NC}"
            return 1
        else
            rm -f "$PID_FILE"
            echo -e "${GREEN}✓ Application stopped${NC}"
            return 0
        fi
    else
        echo -e "${YELLOW}Application is not running${NC}"
        rm -f "$PID_FILE"
        return 0
    fi
}

# Function to show logs
logs() {
    if [ -f "$LOG_FILE" ]; then
        if [ "$1" == "-f" ] || [ "$1" == "--follow" ]; then
            tail -f "$LOG_FILE"
        else
            tail -n 50 "$LOG_FILE"
        fi
    else
        echo -e "${RED}Log file not found: $LOG_FILE${NC}"
    fi
}

# Function to restart app
restart() {
    echo -e "${YELLOW}Restarting application...${NC}"
    stop
    sleep 2
    echo -e "${YELLOW}Starting deployment script...${NC}"
    bash "$SCRIPT_DIR/deploy.sh"
}

# Main script
case "$1" in
    status)
        status
        ;;
    stop)
        stop
        ;;
    logs)
        logs "$2"
        ;;
    restart)
        restart
        ;;
    *)
        echo -e "${BLUE}Budget Lunch Management Script${NC}"
        echo ""
        echo "Usage: $0 {status|stop|logs|restart}"
        echo ""
        echo "Commands:"
        echo "  status   - Show application status"
        echo "  stop     - Stop the application"
        echo "  logs     - Show last 50 lines of logs"
        echo "  logs -f  - Follow logs in real-time"
        echo "  restart  - Restart the application (runs deploy.sh)"
        echo ""
        echo "Examples:"
        echo "  $0 status"
        echo "  $0 logs -f"
        echo "  $0 restart"
        echo ""
        exit 1
        ;;
esac

