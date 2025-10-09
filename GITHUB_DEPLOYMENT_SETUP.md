# GitHub Actions Deployment Setup Guide

This guide will help you set up automatic deployment to your EC2 server using GitHub Actions.

## 📋 Prerequisites

- GitHub repository with your code
- EC2 server running and accessible
- SSH private key for EC2 access
- Git installed on your EC2 server

## 🔑 Step 1: Add SSH Key to GitHub Secrets

### Option A: Using GitHub Web Interface

1. **Locate your SSH private key**
   - The key file is typically at `~/.ssh/your-key-name.pem` or `~/.ssh/id_rsa`
   - For AWS EC2, it's the `.pem` file you downloaded when creating the instance

2. **Copy the private key content**
   ```bash
   # On Mac/Linux, copy the key content:
   cat ~/.ssh/your-ec2-key.pem
   
   # Or use pbcopy to copy directly to clipboard:
   cat ~/.ssh/your-ec2-key.pem | pbcopy
   ```
   
   The key should look like:
   ```
   -----BEGIN RSA PRIVATE KEY-----
   MIIEpAIBAAKCAQEA...
   ...
   -----END RSA PRIVATE KEY-----
   ```

3. **Add the secret to GitHub**
   - Go to your GitHub repository
   - Click on **Settings** tab
   - In the left sidebar, click **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `EC2_SSH_KEY`
   - Value: Paste your entire private key (including the BEGIN and END lines)
   - Click **Add secret**

### Option B: Using GitHub CLI

If you have GitHub CLI installed:

```bash
# Set the secret using gh CLI
gh secret set EC2_SSH_KEY < ~/.ssh/your-ec2-key.pem
```

## ⚙️ Step 2: Verify EC2 Server Setup

Make sure your EC2 server is properly configured:

1. **SSH into your EC2 server** (test manually first):
   ```bash
   ssh -i ~/.ssh/your-ec2-key.pem ec2-user@ec2-52-53-253-15.us-west-1.compute.amazonaws.com
   ```

2. **Verify the project directory exists**:
   ```bash
   cd /home/ec2-user/budget-lunch-web-app-2
   pwd
   ```

3. **Verify the deploy script exists**:
   ```bash
   ls -la deploy.sh
   ```

4. **Ensure the repository is set up** (if not already):
   ```bash
   # If the directory doesn't exist, clone the repository first
   cd /home/ec2-user
   git clone https://github.com/YOUR-USERNAME/budget-lunch-web-app-2.git
   
   # Or initialize git if needed
   cd /home/ec2-user/budget-lunch-web-app-2
   git init
   git remote add origin https://github.com/YOUR-USERNAME/budget-lunch-web-app-2.git
   ```

5. **Make deploy script executable**:
   ```bash
   chmod +x /home/ec2-user/budget-lunch-web-app-2/deploy.sh
   ```

## 🚀 Step 3: Deploy

Once everything is set up, deployment will happen automatically:

### Automatic Deployment
- **Push to main branch**: Any push to the `main` branch will trigger deployment
  ```bash
  git add .
  git commit -m "Update application"
  git push origin main
  ```

### Manual Deployment
1. Go to your GitHub repository
2. Click on the **Actions** tab
3. Select **Deploy to EC2** workflow
4. Click **Run workflow** button
5. Select the branch and click **Run workflow**

## 📊 Monitor Deployment

1. Go to **Actions** tab in your GitHub repository
2. Click on the latest workflow run
3. Watch the deployment progress in real-time
4. Check for any errors in the logs

## 🔒 Security Best Practices

✅ **DO:**
- Keep your SSH private key secret and never commit it to the repository
- Use GitHub Secrets to store sensitive information
- Regularly rotate your SSH keys
- Use specific branch protection rules
- Limit EC2 security group to only necessary IPs if possible

❌ **DON'T:**
- Don't share your `EC2_SSH_KEY` secret
- Don't commit the private key file to git
- Don't use the same key for multiple critical servers

## 🛠️ Troubleshooting

### Issue: "Permission denied (publickey)"
**Solution:**
- Verify the SSH key in GitHub Secrets is correct and complete
- Ensure the key corresponds to the EC2 instance
- Check EC2 security group allows SSH (port 22) from GitHub Actions IPs

### Issue: "Host key verification failed"
**Solution:**
- The workflow includes `ssh-keyscan` to prevent this
- If it persists, you may need to update the `known_hosts` handling

### Issue: "deploy.sh: command not found"
**Solution:**
```bash
# SSH into EC2 and make script executable
chmod +x /home/ec2-user/budget-lunch-web-app-2/deploy.sh
```

### Issue: Git pull fails
**Solution:**
- Ensure git is configured on EC2
- Set up git credentials if using private repository
- Or use SSH deploy keys

## 🔄 Workflow Configuration

The workflow (`.github/workflows/deploy.yml`) is configured to:

1. ✅ Trigger on push to `main` branch
2. ✅ Allow manual deployment via GitHub UI
3. ✅ Checkout the latest code
4. ✅ Configure SSH with your key
5. ✅ Connect to EC2 server
6. ✅ Pull latest changes
7. ✅ Run deployment script
8. ✅ Report success/failure status

## 📝 Customization

### Change deployment branch
Edit `.github/workflows/deploy.yml`:
```yaml
on:
  push:
    branches:
      - develop  # Change from 'main' to 'develop'
```

### Add environment variables
Add more secrets in GitHub and reference them:
```yaml
- name: Deploy to EC2
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  run: |
    ssh ec2-user@... << 'EOF'
      export DATABASE_URL="${{ secrets.DATABASE_URL }}"
      cd /home/ec2-user/budget-lunch-web-app-2
      bash deploy.sh
    EOF
```

### Add notifications
Add a notification step (e.g., Slack, Discord):
```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## ✅ Verification Checklist

Before your first deployment, verify:

- [ ] SSH key added to GitHub Secrets as `EC2_SSH_KEY`
- [ ] EC2 server is accessible via SSH
- [ ] Project directory exists: `/home/ec2-user/budget-lunch-web-app-2`
- [ ] `deploy.sh` script exists and is executable
- [ ] Git is configured on EC2 server
- [ ] Security group allows SSH access
- [ ] Workflow file is committed: `.github/workflows/deploy.yml`

## 🎉 Success!

Once set up, every push to `main` will automatically deploy your changes to EC2! Monitor the Actions tab to see your deployments in progress.

---

**Need Help?** Check the Actions tab for detailed logs of each deployment attempt.

