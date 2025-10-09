# Deployment Scripts Overview

This project includes automated deployment scripts for EC2 deployment.

## 📁 Files Created

| File | Purpose |
|------|---------|
| `deploy.sh` | Main deployment script - automates the entire deployment process |
| `manage.sh` | Application management - status, logs, stop, restart commands |
| `DEPLOYMENT.md` | Comprehensive deployment documentation |
| `QUICKSTART.md` | Quick reference guide for common tasks |
| `app.log` | Application logs (auto-generated, gitignored) |
| `app.pid` | Process ID file (auto-generated, gitignored) |

## 🚀 Quick Usage

### Deploy to EC2
```bash
./deploy.sh
```

### Check Status
```bash
./manage.sh status
```

### View Logs
```bash
./manage.sh logs -f
```

### Restart App
```bash
./manage.sh restart
```

## 📚 Documentation

- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **Full Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Notes**: See [notes.txt](notes.txt)

## ✨ Features

### deploy.sh
- ✅ Pulls latest code from GitHub
- ✅ Manages virtual environment automatically
- ✅ Installs/updates dependencies
- ✅ Gracefully stops existing processes
- ✅ Starts application in background with nohup
- ✅ Verifies successful startup
- ✅ Provides detailed output with status indicators

### manage.sh
- 📊 **Status**: Shows PID, port, memory usage, uptime
- 📝 **Logs**: View or follow application logs
- 🛑 **Stop**: Gracefully stop the application
- 🔄 **Restart**: Full restart with deployment

## 🎯 Deployment Workflow

```
Local Machine              EC2 Instance
─────────────             ─────────────
                          
1. Make changes           
                          
2. Test locally           
                          
3. git push               
                          
                          4. SSH to EC2
                          
                          5. ./deploy.sh
                          
                          6. ./manage.sh status
                          
                          ✅ Deployed!
```

## 🔧 Configuration

Both scripts are configurable:

```bash
# Deploy specific app file
./deploy.sh budget_lunch.py

# Deploy default (budget_lunch_local_db.py)
./deploy.sh
```

## 🛟 Troubleshooting

**Problem**: Application won't start
```bash
./manage.sh logs  # Check error messages
```

**Problem**: Port already in use
```bash
sudo lsof -i :5002  # See what's using the port
./manage.sh stop    # Stop the app
```

**Problem**: Permission denied
```bash
chmod +x deploy.sh manage.sh  # Make executable
```

## 📋 Manual Commands

If you need to do things manually:

```bash
# Pull changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start manually
nohup python3 budget_lunch_local_db.py > app.log 2>&1 &

# Save PID
echo $! > app.pid

# Stop manually
kill $(cat app.pid)
```

## 🔐 Security Notes

- Never commit `app.log` or `app.pid` (already in .gitignore)
- Keep your EC2 key pair secure
- Use Security Groups to restrict access
- Consider using environment variables for sensitive data
- Regularly update dependencies

## 🌟 Best Practices

1. **Always test locally first**
2. **Use meaningful commit messages**
3. **Check logs after deployment**: `./manage.sh logs`
4. **Monitor application status**: `./manage.sh status`
5. **Keep documentation updated**
6. **Regular security updates**: `sudo yum update -y`

## 📞 Support

For detailed instructions, see:
- [DEPLOYMENT.md](DEPLOYMENT.md) - Complete deployment guide
- [QUICKSTART.md](QUICKSTART.md) - Quick reference
- [AUTH_SETUP.md](AUTH_SETUP.md) - Authentication setup

---

**Created**: 2025-10-09  
**Scripts**: `deploy.sh`, `manage.sh`  
**Compatible with**: Amazon Linux 2, Ubuntu, RHEL

