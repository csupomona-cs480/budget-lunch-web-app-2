# 🔄 Deployment Flow Diagram

## Complete Deployment Process

```
┌─────────────────────────────────────────────────────────────────┐
│                     DEVELOPER WORKFLOW                           │
└─────────────────────────────────────────────────────────────────┘

    1. Developer makes changes locally
           │
           ├─ Edit code (styles.css, script.js, etc.)
           ├─ Test locally
           └─ Commit changes
           
    2. Push to GitHub
           │
           └─ git push origin main

┌─────────────────────────────────────────────────────────────────┐
│                     GITHUB ACTIONS                               │
└─────────────────────────────────────────────────────────────────┘

    3. GitHub Actions triggered automatically
           │
           ├─ [STEP 1] Checkout code
           │      └─ Uses: actions/checkout@v4
           │
           ├─ [STEP 2] Configure SSH
           │      ├─ Create ~/.ssh directory
           │      ├─ Write EC2_SSH_KEY to ~/.ssh/id_rsa
           │      ├─ Set permissions (chmod 600)
           │      └─ Add EC2 host to known_hosts
           │
           └─ [STEP 3] Deploy to EC2
                  └─ SSH into EC2 server
                       │
                       └─ ec2-user@ec2-52-53-253-15.us-west-1.compute.amazonaws.com

┌─────────────────────────────────────────────────────────────────┐
│                     EC2 SERVER                                   │
└─────────────────────────────────────────────────────────────────┘

    4. Deployment Script Execution
           │
           ├─ Navigate to project directory
           │      └─ cd /home/ec2-user/budget-lunch-web-app-2
           │
           └─ Run deploy.sh
                  │
                  ├─ [STEP 1/5] Git Pull
                  │      ├─ git fetch origin
                  │      └─ git pull origin main
                  │
                  ├─ [STEP 2/5] Activate Virtual Environment
                  │      ├─ Check if venv exists
                  │      ├─ Create if missing
                  │      └─ source venv/bin/activate
                  │
                  ├─ [STEP 3/5] Install Dependencies
                  │      ├─ pip install --upgrade pip
                  │      └─ pip install -r requirements.txt
                  │
                  ├─ [STEP 4/5] Stop Existing Application
                  │      ├─ Read PID from app.pid
                  │      ├─ Kill process if running
                  │      └─ Clean up PID file
                  │
                  └─ [STEP 5/5] Start New Application
                         ├─ Run: nohup python3 budget_lunch_local_db.py
                         ├─ Save PID to app.pid
                         ├─ Redirect logs to app.log
                         └─ Verify process is running

┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION RUNNING                          │
└─────────────────────────────────────────────────────────────────┘

    5. Flask Application Status
           │
           ├─ Process ID saved in: app.pid
           ├─ Logs written to: app.log
           ├─ Running on port: (from Python file)
           └─ Accessible at: http://ec2-52-53-253-15.us-west-1.compute.amazonaws.com

┌─────────────────────────────────────────────────────────────────┐
│                     MONITORING                                   │
└─────────────────────────────────────────────────────────────────┘

    6. View Status
           │
           ├─ GitHub Actions Tab
           │      └─ Real-time deployment logs
           │
           └─ EC2 Server
                  ├─ View logs: tail -f /home/ec2-user/budget-lunch-web-app-2/app.log
                  ├─ Check process: ps aux | grep budget_lunch
                  └─ Test app: curl http://localhost:PORT
```

## Key Components

### 🔐 GitHub Secret
- **Name:** `EC2_SSH_KEY`
- **Content:** Your EC2 private key (.pem file)
- **Location:** GitHub Repo → Settings → Secrets and variables → Actions

### 📂 Project Structure
```
/home/ec2-user/budget-lunch-web-app-2/
├── budget_lunch_local_db.py    # Main application
├── deploy.sh                    # Deployment script
├── requirements.txt             # Python dependencies
├── venv/                        # Virtual environment
├── app.log                      # Application logs
├── app.pid                      # Process ID file
└── static files...
```

### 🚀 Workflow File
```
.github/workflows/deploy.yml
```

### 🎯 Triggers
1. **Automatic:** Push to `main` branch
2. **Manual:** GitHub Actions → Run workflow button

## Timeline

```
Push Code → GitHub Actions (1-2 min) → SSH to EC2 (5s) → 
Deploy Script (30s-2min) → App Running ✅

Total Time: ~2-4 minutes
```

## Success Indicators

✅ **GitHub Actions:**
- Green checkmark on commit
- "Deployment to EC2 completed successfully!" message

✅ **EC2 Server:**
- New PID in app.pid
- Fresh logs in app.log
- Process visible in `ps aux | grep python`

✅ **Application:**
- Website accessible
- Latest changes visible
- No errors in browser console

## Troubleshooting Points

| Step | Issue | Check |
|------|-------|-------|
| SSH Connection | Permission denied | EC2_SSH_KEY secret is correct |
| Git Pull | Authentication failed | Git credentials on EC2 |
| Dependencies | Install fails | requirements.txt exists |
| App Start | Process dies | Check app.log for errors |
| Port Access | Cannot connect | Security group allows port |

## Security Flow

```
GitHub Secret (encrypted)
    ↓
GitHub Actions Runner (temporary)
    ↓
SSH Connection (encrypted)
    ↓
EC2 Server (authorized_keys)
    ↓
Deployment (isolated venv)
    ↓
Running Application
```

**Note:** Private key never leaves GitHub's secure environment and is only used in memory during deployment.

## Rollback Process

If deployment fails:

1. **GitHub Actions** will show the error
2. **Previous version** continues running (deploy.sh kills old process only after successful start)
3. **Manual rollback:**
   ```bash
   ssh ec2-user@ec2-52-53-253-15.us-west-1.compute.amazonaws.com
   cd /home/ec2-user/budget-lunch-web-app-2
   git checkout <previous-commit>
   bash deploy.sh
   ```

## Best Practices

✅ Test changes locally first
✅ Use meaningful commit messages
✅ Monitor first few deployments
✅ Keep `deploy.sh` idempotent
✅ Check logs after deployment
✅ Set up monitoring/alerting
✅ Regular backups of app data
✅ Rotate SSH keys periodically

---

**Questions?** Check the [full setup guide](../GITHUB_DEPLOYMENT_SETUP.md) or [quick start](./DEPLOYMENT_QUICKSTART.md).

