# Quick Start - EC2 Deployment

## First Time Setup

```bash
# 1. SSH into EC2
ssh -i your-key.pem ec2-user@your-ec2-ip

# 2. Clone repo
git clone https://github.com/csupomona-cs480/budget-lunch-web-app-2.git
cd budget-lunch-web-app-2

# 3. Make scripts executable
chmod +x deploy.sh manage.sh

# 4. Deploy
./deploy.sh
```

## Regular Deployment Workflow

### From Your Local Machine:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

### From EC2 (via SSH):
```bash
cd ~/budget-lunch-web-app-2
./deploy.sh
```

**That's it!** The script handles everything:
- ✓ Pulls latest code
- ✓ Activates virtual environment
- ✓ Installs dependencies
- ✓ Stops old process
- ✓ Starts new process

## Useful Commands

```bash
./manage.sh status        # Check if app is running
./manage.sh logs -f       # Watch logs in real-time
./manage.sh restart       # Restart the app
./manage.sh stop          # Stop the app
```

## Access Your App

```
http://your-ec2-ip:5002
```

## Troubleshooting

**App won't start?**
```bash
./manage.sh logs          # Check what went wrong
```

**Need to kill it manually?**
```bash
pkill -f budget_lunch_local_db.py
```

**Port already in use?**
```bash
sudo lsof -i :5002        # See what's using the port
```

## Full Documentation

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

