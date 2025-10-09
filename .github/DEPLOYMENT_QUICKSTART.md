# 🚀 Deployment Quick Start

## Three Simple Steps to Enable Auto-Deployment

### 1️⃣ Add SSH Key to GitHub (2 minutes)

```bash
# Copy your EC2 private key
cat ~/.ssh/your-ec2-key.pem

# Or copy to clipboard on Mac:
cat ~/.ssh/your-ec2-key.pem | pbcopy
```

Then:
1. Go to GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `EC2_SSH_KEY`
4. Paste the entire key content
5. Click **Add secret**

### 2️⃣ Verify EC2 Server (1 minute)

```bash
# SSH into your server
ssh -i ~/.ssh/your-ec2-key.pem ec2-user@ec2-52-53-253-15.us-west-1.compute.amazonaws.com

# Make sure the directory exists and script is executable
cd /home/ec2-user/budget-lunch-web-app-2
chmod +x deploy.sh
```

### 3️⃣ Commit and Push (30 seconds)

```bash
# Commit the workflow file
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Actions deployment workflow"
git push origin main
```

## ✅ Done!

Every push to `main` now automatically deploys to your EC2 server!

Watch it work: Go to **Actions** tab in GitHub.

---

### Manual Deployment

Want to deploy without pushing?
1. Go to GitHub → **Actions** tab
2. Select **Deploy to EC2**
3. Click **Run workflow**

### Testing

Make a test change:
```bash
echo "# Test" >> README.md
git add README.md
git commit -m "Test deployment"
git push origin main
```

Check GitHub Actions tab to see it deploy! 🎉

