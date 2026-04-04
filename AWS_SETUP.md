# AWS SETUP — Figurinha Trader

Complete guide to setting up Figurinha Trader infrastructure on AWS using EC2 Free Tier.

---

## 📋 Prerequisites

Before starting, prepare:

- AWS account (create at [aws.amazon.com](https://aws.amazon.com) — eligible for 12 months free)
- Supabase account (backend)
- GitHub account (project repository)
- Composio account (automation with GitHub, EAS, Slack/Google Chat)
- Claude API Key (console.anthropic.com)

---

## 🚀 Step 1 — Create an EC2 Instance on AWS Free Tier

### 1.1 Access EC2 Console
1. Log in at [console.aws.amazon.com](https://console.aws.amazon.com)
2. Go to **EC2 → Instances → Launch Instances**

### 1.2 Configure the Instance

**Name and Tags:**
- Name: `figurinha-trader-n8n`

**AMI (Amazon Machine Image):**
- Select **Ubuntu Server 24.04 LTS** (free tier eligible)
- Confirm it shows "Free tier eligible"

**Instance Type:**
- Select **t2.micro** (1 vCPU, 1GB RAM)
- Status: "Free tier eligible"

**Key Pair:**
- Click "Create new key pair"
- Name: `figurinha-trader-key`
- Type: RSA
- Format: `.pem` (for Mac/Linux) or `.ppk` (for Windows with PuTTY)
- **Save the file securely** — you won't be able to download it again

### 1.3 Configure Storage

**Root Volume:**
- Size: 30GB (free tier allows up to 30GB)
- Type: gp3 (default)
- Encrypt: not required for development
- Delete on termination: ✓ (check)

### 1.4 Configure Security Group

**Inbound Rules:** (add the following)

| Type | Protocol | Port | Source |
|------|----------|------|--------|
| SSH | TCP | 22 | 0.0.0.0/0 (your IP is better) |
| HTTP | TCP | 80 | 0.0.0.0/0 |
| HTTPS | TCP | 443 | 0.0.0.0/0 |
| Custom TCP | TCP | 5678 | 0.0.0.0/0 (N8N) |

**Outbound Rules:**
- Default (all traffic allowed) — OK for development

### 1.5 Review and Launch

- Review all settings
- Click **"Launch Instance"**
- Wait until the Status shows **"Running"** (2-3 minutes)

### 1.6 Get the IP Address

1. Click on the instance to view details
2. Note the **Public IPv4 address** (e.g., `54.123.456.789`)
3. Wait until **Status checks** shows "2/2 checks passed"

---

## 🔐 Step 2 — Connect via SSH

### On Mac/Linux:

```bash
# Set permissions on the key file
chmod 400 ~/Downloads/figurinha-trader-key.pem

# Connect to the instance
ssh -i ~/Downloads/figurinha-trader-key.pem ubuntu@54.123.456.789
```

### On Windows (with PuTTY):

1. Open PuTTY
2. Under "Session", enter: `ubuntu@54.123.456.789`
3. Under "SSH → Auth", point to the `.ppk` file
4. Click "Open"

---

## 🐳 Step 3 — Install Docker

Connected via SSH, run:

```bash
# Update repositories
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu
newgrp docker

# Verify installation
docker --version
```

---

## 📦 Step 4 — Install Docker Compose

```bash
# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Set permissions
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker-compose --version
```

---

## 📝 Step 5 — Create docker-compose.yml for N8N

Create the file with these commands:

```bash
cd ~
mkdir figurinha-trader
cd figurinha-trader
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=${N8N_HOST}
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
      - COMPOSIO_API_KEY=${COMPOSIO_API_KEY}
      - GITHUB_REPO_OWNER=${GITHUB_REPO_OWNER}
      - GITHUB_REPO_NAME=${GITHUB_REPO_NAME}
    volumes:
      - n8n_data:/home/node/.n8n
      - /etc/localtime:/etc/localtime:ro
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:5678/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  n8n_data:
    driver: local
EOF
```

---

## 🔑 Step 6 — Configure Environment Variables

Create a `.env` file:

```bash
cat > .env << 'EOF'
N8N_HOST=54.123.456.789
N8N_PASSWORD=your-super-secure-password-here
N8N_ENCRYPTION_KEY=generate-a-random-32-character-key
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxx
COMPOSIO_API_KEY=your-composio-api-key
GITHUB_REPO_OWNER=your-github-username
GITHUB_REPO_NAME=figurinha-trader
EOF
```

**Tips to generate secure keys:**

```bash
# Generate N8N_ENCRYPTION_KEY (32 random characters)
openssl rand -hex 16

# Generate a secure N8N_PASSWORD
openssl rand -base64 20
```

---

## 🚀 Step 7 — Start N8N

```bash
# Start the container
docker-compose up -d

# Check status
docker-compose ps

# View logs (optional)
docker-compose logs -f n8n
```

Wait 30-60 seconds for N8N to start.

---

## 🌐 Step 8 — Access N8N

Open in your browser:

```
http://54.123.456.789:5678
```

Log in with:
- Username: `admin`
- Password: (the one you set in `N8N_PASSWORD`)

---

## ⚙️ Step 9 — Configure SSL/HTTPS (Recommended for Production)

For production, configure HTTPS using Let's Encrypt:

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate (requires a domain)
sudo certbot certonly --standalone -d your-domain.com
```

Then update `docker-compose.yml` to use HTTPS and mount the certificates.

---

## 📂 Step 10 — Push Configuration Files to GitHub

In your figurinha-trader repository, push:

```bash
git add state.json tasks.json PROTOCOL.md
git commit -m "chore: add automation pipeline configuration"
git push origin main
```

---

## 🔄 Step 11 — Create Workflows in N8N

Access http://54.123.456.789:5678 and follow **N8N_SETUP.md** to create:

1. **Task Runner** — runs scheduled tasks
2. **Daily EAS Build** — generates app builds
3. **Weekly Report** — progress summary
4. **Nightly Cleanup** — artifact cleanup

---

## 🔍 Monitoring & Maintenance

### Check N8N status
```bash
docker-compose ps
```

### View logs
```bash
docker-compose logs -f n8n
```

### Stop N8N
```bash
docker-compose stop
```

### Restart N8N
```bash
docker-compose restart
```

### Update to the latest version
```bash
docker-compose pull
docker-compose up -d
```

---

## 💾 Backup

To back up the N8N database:

```bash
docker-compose exec n8n tar -czf /tmp/n8n-backup.tar.gz /home/node/.n8n
docker cp figurinha-trader-n8n-1:/tmp/n8n-backup.tar.gz ~/backups/
```

---

## ❌ Troubleshooting

### N8N won't start

```bash
# View detailed logs
docker-compose logs n8n

# Clear data (careful!)
docker-compose down -v
docker-compose up -d
```

### "Connection refused" error

- Check if the EC2 instance is running
- Check if the Security Group inbound rules include port 5678
- Check the public IP (it may change if you stop the instance)

### Low performance with t2.micro

If N8N becomes slow:
- Upgrade to t2.small (exits free tier, ~$5/month)
- Or optimize workflows to use less memory

---

## 🎯 Next Steps

1. ✅ EC2 instance created and running
2. ✅ Docker and N8N installed
3. → Configure workflows in N8N (see N8N_SETUP.md)
4. → Connect Composio with GitHub, EAS, Slack
5. → Start automation pipeline

---

**Estimated cost:**
- EC2 t2.micro: $0 (12-month free tier)
- Bandwidth: ~$1-3/month (depends on usage)
- **Total:** $0-3/month for 12 months

After 12 months, EC2 starts billing ~$8-10/month. At that point, you can:
- Stay on t2.micro (paid — cheapest option)
- Migrate to ECS Fargate containers (similar to Heroku)
- Use Lambda for serverless workflows (much cheaper)

---

**Last updated:** 04/04/2026
