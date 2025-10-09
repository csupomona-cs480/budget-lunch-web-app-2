# 🚀 Automatic Deployment Setup

Your Budget Lunch app is now configured for **automatic deployment** to your EC2 server via GitHub Actions!

## 📦 What's Been Set Up

I've created a complete GitHub Actions workflow that will automatically deploy your app whenever you push code to the `main` branch.

### Files Created:
- ✅ `.github/workflows/deploy.yml` - Main deployment workflow
- ✅ `.github/DEPLOYMENT_QUICKSTART.md` - Quick 3-step setup guide
- ✅ `.github/DEPLOYMENT_FLOW.md` - Visual flow diagram
- ✅ `GITHUB_DEPLOYMENT_SETUP.md` - Comprehensive setup guide
- ✅ Updated `.gitignore` - Added SSH key protection

## 🎯 Quick Setup (3 Steps)

### Step 1: Add Your SSH Key to GitHub (2 minutes)

1. **Find and copy your EC2 private key:**
   ```bash
   # Replace with your actual key file name
   cat ~/.ssh/your-ec2-key.pem
   ```
   Or on Mac, copy directly to clipboard:
   ```bash
   cat ~/.ssh/your-ec2-key.pem | pbcopy
   ```

2. **Add to GitHub:**
   - Go to your GitHub repository
   - Click **Settings** (top menu)
   - Click **Secrets and variables** → **Actions** (left sidebar)
   - Click **New repository secret**
   - **Name:** `EC2_SSH_KEY`
   - **Value:** Paste your entire private key
   - Click **Add secret**

### Step 2: Verify EC2 Setup (1 minute)

SSH into your EC2 server and verify:
```bash
ssh -i ~/.ssh/your-ec2-key.pem ec2-user@ec2-52-53-253-15.us-west-1.compute.amazonaws.com

# Verify directory and script exist
cd /home/ec2-user/budget-lunch-web-app-2
ls -la deploy.sh

# Make script executable if needed
chmod +x deploy.sh

# Exit EC2
exit
```

### Step 3: Push to GitHub (30 seconds)

```bash
# Stage all files
git add .

# Commit with a message
git commit -m "Add automatic deployment workflow"

# Push to main branch (triggers deployment)
git push origin main
```

## 🎉 Done!

Go to your GitHub repository and click the **Actions** tab to watch your first automated deployment!

---

## 📖 How It Works

### Automatic Deployment
Every time you push to the `main` branch:

```
Your Computer → GitHub → GitHub Actions → EC2 Server → App Deployed ✅
```

### Manual Deployment
You can also trigger deployment manually:
1. Go to GitHub → **Actions** tab
2. Click **Deploy to EC2** workflow
3. Click **Run workflow**

### What Happens During Deployment

The workflow automatically:
1. ✅ Connects to your EC2 server via SSH
2. ✅ Navigates to your project folder
3. ✅ Runs `deploy.sh` which:
   - Pulls latest code from GitHub
   - Activates Python virtual environment
   - Installs/updates dependencies
   - Stops the old application
   - Starts the new application
   - Saves logs to `app.log`

---

## 🔍 Monitoring Your Deployments

### GitHub Actions
- **View all deployments:** GitHub → **Actions** tab
- **Check status:** Green ✓ = success, Red ✗ = failed
- **View logs:** Click on any deployment to see detailed logs

### EC2 Server
```bash
# View real-time logs
ssh ec2-user@ec2-52-53-253-15.us-west-1.compute.amazonaws.com
tail -f /home/ec2-user/budget-lunch-web-app-2/app.log

# Check if app is running
ps aux | grep budget_lunch

# View last 50 lines of log
tail -n 50 /home/ec2-user/budget-lunch-web-app-2/app.log
```

---

## 🎨 Making Changes & Deploying

Simple workflow:

```bash
# 1. Make your changes locally
vim styles.css
# or edit in your IDE

# 2. Test locally (optional but recommended)
python3 budget_lunch_local_db.py

# 3. Commit and push
git add .
git commit -m "Update button colors"
git push origin main

# 4. Watch it deploy automatically! 🚀
# Go to GitHub → Actions tab
```

**Deployment typically takes 2-4 minutes.**

---

## 🛡️ Security Features

- ✅ Private SSH key stored securely in GitHub Secrets (encrypted)
- ✅ Key never exposed in logs or code
- ✅ `.gitignore` prevents accidental key commits
- ✅ SSH connection uses secure protocols
- ✅ Workflow runs in isolated GitHub environment

---

## 📚 Additional Resources

For more detailed information, see:

- **Quick Reference:** `.github/DEPLOYMENT_QUICKSTART.md`
- **Complete Guide:** `GITHUB_DEPLOYMENT_SETUP.md`
- **Flow Diagram:** `.github/DEPLOYMENT_FLOW.md`

---

## ❓ Troubleshooting

### "Permission denied (publickey)"
→ Check that `EC2_SSH_KEY` secret is set correctly in GitHub

### "deploy.sh: Permission denied"
→ Run: `chmod +x /home/ec2-user/budget-lunch-web-app-2/deploy.sh`

### "Application failed to start"
→ Check logs: `tail -f /home/ec2-user/budget-lunch-web-app-2/app.log`

### Deployment stuck or slow
→ Check GitHub Actions logs for specific error messages

---

## 🎯 Test Your Setup

Make a small test change:

```bash
echo "# Test deployment" >> README.md
git add README.md
git commit -m "Test automatic deployment"
git push origin main
```

Then watch it deploy in GitHub → Actions tab! 🎉

---

## 💡 Tips

- **First deployment:** Watch the Actions tab carefully to catch any issues
- **Commit messages:** Use clear messages so you know what deployed when
- **Before big changes:** Test locally first
- **Check logs:** After deployment, verify app.log on EC2
- **Rollback if needed:** You can always revert to a previous commit

---

## 🎊 Success Checklist

After your first successful deployment, you should see:

- ✅ Green checkmark in GitHub Actions
- ✅ New timestamp in app.log
- ✅ Application accessible at your EC2 URL
- ✅ Your changes visible on the website

---

**Need help?** Check the detailed guides in `.github/` folder or review the deployment logs in GitHub Actions.

**Happy deploying!** 🚀

