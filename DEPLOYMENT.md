# Budget Lunch Web App - Deployment Guide

## Overview

This guide covers deploying the Budget Lunch Web App to an EC2 instance using the automated deployment scripts.

## Files

- **`deploy.sh`** - Main deployment script that automates the entire deployment process
- **`manage.sh`** - Management script for checking status, viewing logs, and controlling the app
- **`app.log`** - Application log file (generated after deployment)
- **`app.pid`** - Process ID file (generated after deployment)

## Initial Setup on EC2

### 1. Connect to Your EC2 Instance

```bash
ssh -i your-key.pem ec2-user@your-ec2-ip
```

### 2. Install Required System Packages

```bash
# For Amazon Linux 2 / RHEL
sudo yum update -y
sudo yum install -y git python3 python3-pip

# For Ubuntu/Debian
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv
```

### 3. Clone the Repository

```bash
cd ~
git clone https://github.com/csupomona-cs480/budget-lunch-web-app-2.git
cd budget-lunch-web-app-2
```

### 4. Make Scripts Executable

```bash
chmod +x deploy.sh manage.sh
```

### 5. Configure EC2 Security Group

Make sure your EC2 security group allows inbound traffic on the application ports:
- Port 5002 (budget_lunch_local_db.py)
- Port 5001 (budget_lunch.py)

## Deployment

### First Time Deployment

```bash
./deploy.sh
```

This will:
1. ✓ Pull latest changes from GitHub
2. ✓ Create/activate virtual environment
3. ✓ Install all dependencies from requirements.txt
4. ✓ Stop any existing application processes
5. ✓ Start the application in background with nohup

### Deploying Specific App File

By default, `deploy.sh` runs `budget_lunch_local_db.py`. To deploy a different file:

```bash
./deploy.sh budget_lunch.py
```

### Subsequent Deployments

After making changes locally:

1. **Push changes to GitHub** (from your local machine):
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

2. **Deploy on EC2** (from SSH session):
   ```bash
   cd ~/budget-lunch-web-app-2
   ./deploy.sh
   ```

## Management Commands

### Check Application Status

```bash
./manage.sh status
```

Output shows:
- Running status (✓ or ✗)
- Process ID (PID)
- Port number
- Start time
- Memory usage
- Log file location and size

### View Logs

**Last 50 lines:**
```bash
./manage.sh logs
```

**Follow logs in real-time:**
```bash
./manage.sh logs -f
# Press Ctrl+C to exit
```

**Alternative (direct command):**
```bash
tail -f app.log
```

### Stop Application

```bash
./manage.sh stop
```

### Restart Application

```bash
./manage.sh restart
```

This will stop the app and run the full deployment script.

## Manual Operations

### Start Application Manually

```bash
source venv/bin/activate
nohup python3 budget_lunch_local_db.py > app.log 2>&1 &
echo $! > app.pid
```

### Kill Process Manually

```bash
# Using PID file
kill $(cat app.pid)

# Or find and kill by name
pkill -f budget_lunch_local_db.py

# Force kill if needed
kill -9 $(cat app.pid)
```

### Check Running Python Processes

```bash
ps aux | grep python
```

### Check Port Usage

```bash
# Check if port 5002 is in use
sudo netstat -tulpn | grep 5002

# Or using lsof
sudo lsof -i :5002
```

## Troubleshooting

### Application Won't Start

1. **Check the logs:**
   ```bash
   ./manage.sh logs
   ```

2. **Check if port is already in use:**
   ```bash
   sudo lsof -i :5002
   ```

3. **Check virtual environment:**
   ```bash
   source venv/bin/activate
   python3 -c "import flask; print('Flask is installed')"
   ```

4. **Manually install dependencies:**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Can't Pull from GitHub

**If authentication fails:**
```bash
# Use HTTPS with personal access token
git remote set-url origin https://YOUR_TOKEN@github.com/csupomona-cs480/budget-lunch-web-app-2.git

# Or use SSH (if you've set up SSH keys)
git remote set-url origin git@github.com:csupomona-cs480/budget-lunch-web-app-2.git
```

**If there are local changes:**
```bash
# Stash local changes
git stash

# Pull changes
git pull origin main

# Reapply stashed changes if needed
git stash pop
```

### Permission Denied

```bash
# Make scripts executable
chmod +x deploy.sh manage.sh

# Check file ownership
ls -la deploy.sh manage.sh

# If needed, take ownership
sudo chown $USER:$USER deploy.sh manage.sh
```

### Virtual Environment Issues

```bash
# Remove and recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Access Your Application

Once deployed, access your application at:

```
http://your-ec2-public-ip:5002
```

Or for budget_lunch.py:
```
http://your-ec2-public-ip:5001
```

## Setting Up a Domain Name (Optional)

### Using Nginx as Reverse Proxy

1. **Install Nginx:**
   ```bash
   sudo yum install -y nginx  # Amazon Linux
   # or
   sudo apt install -y nginx  # Ubuntu
   ```

2. **Configure Nginx:**
   ```bash
   sudo nano /etc/nginx/conf.d/budget-lunch.conf
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:5002;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

3. **Start Nginx:**
   ```bash
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```

## Automated Deployment with Webhooks (Advanced)

To automatically deploy when you push to GitHub:

1. Set up a webhook endpoint in your Flask app
2. Configure GitHub webhook to call your endpoint
3. The endpoint should call `deploy.sh` when triggered

## Logs and Monitoring

### Application Logs
- **Location:** `app.log` in project directory
- **View:** `./manage.sh logs -f`

### System Logs
```bash
# Check system logs
sudo journalctl -u nginx -f  # If using Nginx

# Check EC2 instance logs
sudo tail -f /var/log/messages  # Amazon Linux
sudo tail -f /var/log/syslog    # Ubuntu
```

### Log Rotation (Recommended)

Create `/etc/logrotate.d/budget-lunch`:

```
/home/ec2-user/budget-lunch-web-app-2/app.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

## Best Practices

1. **Always test locally before deploying to EC2**
2. **Use meaningful commit messages**
3. **Check logs after deployment** to ensure everything started correctly
4. **Monitor disk space** - logs can grow large
5. **Set up CloudWatch** for EC2 monitoring
6. **Use Elastic IP** to avoid changing IP addresses
7. **Regular backups** of your database/data files
8. **Keep dependencies updated** but test changes first

## Quick Reference

```bash
# Deploy
./deploy.sh

# Check status
./manage.sh status

# View logs
./manage.sh logs -f

# Restart
./manage.sh restart

# Stop
./manage.sh stop
```

## Support

For issues or questions:
- Check application logs: `./manage.sh logs`
- Review deployment script: `cat deploy.sh`
- Check GitHub repository for updates

---

**Last Updated:** 2025-10-09

