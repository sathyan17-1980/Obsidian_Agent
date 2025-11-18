# Customer Journey Analysis Tool - Deployment Guide

## Overview

Complete step-by-step guide for deploying the Customer Journey Analysis Tool on a Hetzner CPX21 VPS (4GB RAM, 2 vCPU, 80GB SSD) for ~$9/month.

**Target Capacity:** <10,000 events/day (small scale)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [VPS Setup](#vps-setup)
3. [SSL Certificate Setup](#ssl-certificate-setup)
4. [Application Deployment](#application-deployment)
5. [Verification](#verification)
6. [Monitoring](#monitoring)
7. [Backup & Restore](#backup--restore)
8. [Scaling to Medium](#scaling-to-medium)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts

- ✅ **Hetzner Cloud Account** (https://hetzner.com)
- ✅ **Domain Name** (for SSL/HTTPS)
- ✅ **Anthropic API Key** (https://console.anthropic.com/)
- ✅ **GitHub/GitLab Account** (for code repository)

### Required Tools on Your Local Machine

```bash
# SSH client (usually pre-installed)
ssh -V

# Git (for cloning repository)
git --version

# Optional: Docker Desktop (for local testing)
docker --version
```

---

## VPS Setup

### Step 1: Create Hetzner VPS

1. **Log in to Hetzner Cloud Console**
   - Go to: https://console.hetzner.cloud/

2. **Create New Project**
   - Name: `customer-journey-prod`

3. **Create Server**
   - Location: Choose closest to your target audience (e.g., `Nuremberg, Germany`)
   - Image: `Ubuntu 22.04`
   - Type: `CPX21` (2 vCPU, 4GB RAM, 80GB SSD) - €8.46/month
   - Volume: None (not needed for small scale)
   - Network: Default
   - SSH Key: Add your public SSH key
   - Name: `journey-app-1`

4. **Note the IP Address**
   - Example: `95.217.123.45`

### Step 2: Configure DNS

Point your domain to the VPS IP:

```
# A Records
yourdomain.com       A     95.217.123.45
www.yourdomain.com   A     95.217.123.45
api.yourdomain.com   A     95.217.123.45
```

**Wait 10-30 minutes for DNS propagation.**

Verify with:
```bash
dig yourdomain.com +short
# Should return: 95.217.123.45
```

### Step 3: Initial Server Setup

SSH into your VPS:

```bash
ssh root@95.217.123.45
```

Update system packages:

```bash
apt update && apt upgrade -y
```

Install required packages:

```bash
apt install -y \
    docker.io \
    docker-compose \
    git \
    curl \
    vim \
    htop \
    ufw \
    fail2ban
```

Enable Docker:

```bash
systemctl enable docker
systemctl start docker
```

Verify Docker installation:

```bash
docker --version
docker-compose --version
```

### Step 4: Configure Firewall

```bash
# Allow SSH
ufw allow 22/tcp

# Allow HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Enable firewall
ufw --force enable

# Verify
ufw status
```

### Step 5: Install Fail2Ban (Security)

```bash
# Already installed above
systemctl enable fail2ban
systemctl start fail2ban
```

---

## Application Deployment

### Step 1: Clone Repository

```bash
# Create app directory
mkdir -p /opt/customer-journey
cd /opt/customer-journey

# Clone repository
git clone https://github.com/sathyan17-1980/Obsidian_Agent.git .

# Navigate to deployment directory
cd docs/customer-journey-tool/deployment
```

### Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit configuration
vim .env
```

**Update the following variables:**

```bash
# Database Password (IMPORTANT!)
POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD_HERE_CHANGE_ME

# API Key Salt (generate with: openssl rand -base64 32)
API_KEY_SALT=YOUR_RANDOM_SALT_HERE_CHANGE_ME

# Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE

# Domain Configuration
DOMAIN=yourdomain.com
LETSENCRYPT_EMAIL=admin@yourdomain.com

# CORS Origins
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Generate secure passwords:**

```bash
# Generate database password
openssl rand -base64 32

# Generate API key salt
openssl rand -base64 32
```

### Step 3: Update Nginx Configuration

Edit the Nginx site configuration:

```bash
vim nginx/conf.d/customer-journey.conf
```

**Replace all instances of `yourdomain.com` with your actual domain.**

Use find/replace in vim:
```
:%s/yourdomain.com/yourACTUALdomain.com/g
```

### Step 4: Build and Start Services

```bash
# Build Docker images
docker-compose build

# Start services (without SSL first)
docker-compose up -d postgres redis app

# Check if services are running
docker-compose ps
```

Expected output:
```
NAME                        STATUS
customer_journey_postgres   Up
customer_journey_redis      Up
customer_journey_app        Up (healthy)
```

### Step 5: Verify Database Initialization

```bash
# Check PostgreSQL logs
docker-compose logs postgres | tail -20

# Should see: "Customer Journey database schema initialized successfully"
```

### Step 6: Verify Application Health

```bash
# Test health endpoint
curl http://localhost:8030/health

# Expected response: {"status":"healthy"}
```

---

## SSL Certificate Setup

### Step 1: Initial Certificate Request

**Before starting Nginx, get SSL certificate:**

```bash
# Run Certbot standalone
docker-compose run --rm certbot certonly \
    --standalone \
    --email admin@yourdomain.com \
    --agree-tos \
    --no-eff-email \
    -d yourdomain.com \
    -d www.yourdomain.com
```

**IMPORTANT:** Make sure ports 80/443 are not in use during this step.

Expected output:
```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/yourdomain.com/fullchain.pem
Key is saved at: /etc/letsencrypt/live/yourdomain.com/privkey.pem
```

### Step 2: Start Nginx with SSL

```bash
# Now start Nginx and Certbot
docker-compose up -d nginx certbot

# Verify Nginx is running
docker-compose ps nginx
```

### Step 3: Test HTTPS

```bash
# Test HTTPS endpoint
curl https://yourdomain.com/health

# Should redirect to HTTPS and return: {"status":"healthy"}
```

---

## Verification

### 1. Check All Services

```bash
docker-compose ps
```

Expected state - all services `Up` or `Up (healthy)`:

```
NAME                        STATE
customer_journey_app        Up (healthy)
customer_journey_postgres   Up (healthy)
customer_journey_redis      Up (healthy)
customer_journey_nginx      Up (healthy)
customer_journey_certbot    Up
customer_journey_backup     Up
```

### 2. Test API Endpoints

```bash
# Health check
curl https://yourdomain.com/health

# API documentation
curl https://yourdomain.com/docs

# Test event ingestion (should return 401 without API key)
curl -X POST https://yourdomain.com/api/v1/events \
    -H "Content-Type: application/json" \
    -d '{"events":[]}'
```

### 3. Check Logs

```bash
# Application logs
docker-compose logs -f app

# Nginx access logs
docker-compose logs -f nginx

# PostgreSQL logs
docker-compose logs -f postgres
```

### 4. Test SDK Serving

```bash
# SDK should be accessible (after you build and place it)
curl https://yourdomain.com/sdk/customer-journey.min.js
```

---

## Monitoring

### System Resources

```bash
# Install htop (if not already installed)
apt install htop

# Monitor system resources
htop

# Check Docker resource usage
docker stats
```

### Service Health

```bash
# Check Docker service health
docker-compose ps

# Restart unhealthy service
docker-compose restart app
```

### Logs Monitoring

```bash
# Follow application logs
docker-compose logs -f app

# View last 100 lines
docker-compose logs --tail=100 app

# Search logs for errors
docker-compose logs app | grep ERROR
```

### Database Monitoring

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U journey_user -d customer_journey

# Check database size
\l+

# Check table sizes
\dt+

# Check event count
SELECT COUNT(*) FROM events;

# Check recent events
SELECT * FROM events ORDER BY timestamp DESC LIMIT 10;

# Exit
\q
```

### Disk Usage

```bash
# Check disk usage
df -h

# Check Docker disk usage
docker system df

# Clean up unused Docker resources (careful!)
docker system prune -a
```

---

## Backup & Restore

### Manual Backup

```bash
# Run backup script manually
docker-compose exec backup /backup.sh

# Check backups
ls -lh /var/lib/docker/volumes/deployment_backups/_data/
```

### Automated Daily Backups

Backups are configured to run automatically daily at 2 AM via the backup container.

**Backup retention:** 7 days (configurable in `.env`)

### Restore from Backup

#### Restore PostgreSQL

```bash
# Stop application
docker-compose stop app

# Restore database
gunzip -c /path/to/backup/postgres_20250118_020000.sql.gz | \
    docker-compose exec -T postgres psql -U journey_user -d customer_journey

# Restart application
docker-compose start app
```

#### Restore Obsidian Vault

```bash
# Extract vault backup
tar -xzf /path/to/backup/obsidian_20250118_020000.tar.gz \
    -C /var/lib/docker/volumes/deployment_obsidian_vault/_data/
```

### Off-site Backups (Recommended)

```bash
# Install rsync
apt install rsync

# Sync backups to remote server
rsync -avz --delete \
    /var/lib/docker/volumes/deployment_backups/_data/ \
    user@remote-server:/backups/customer-journey/

# Or use cloud storage (S3, Backblaze B2, etc.)
```

---

## Scaling to Medium (10K-100K events/day)

When you outgrow single-server setup:

### Step 1: Add Dedicated Database Server

```bash
# Create new Hetzner server (CPX21 or CPX31)
# - Name: journey-db-1
# - Install PostgreSQL + TimescaleDB
# - Migrate data from app server
```

### Step 2: Update docker-compose.yml

```yaml
# Comment out postgres service
# Update DATABASE_URL to point to dedicated server
environment:
  DATABASE_URL: postgresql://user:pass@journey-db-1:5432/customer_journey
```

### Step 3: Add Load Balancer (Optional)

```bash
# Create HAProxy or Nginx load balancer
# - Name: journey-lb-1
# - Point to multiple app servers
```

**Total cost at medium scale:** ~$100-145/month

See main planning document for detailed medium-scale architecture.

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs for error messages
docker-compose logs [service-name]

# Restart service
docker-compose restart [service-name]

# Rebuild and restart
docker-compose up -d --build [service-name]
```

### Database Connection Errors

```bash
# Verify PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Test connection
docker-compose exec postgres psql -U journey_user -d customer_journey -c "SELECT 1;"
```

### High Memory Usage

```bash
# Check memory usage
free -h

# Check Docker stats
docker stats

# Reduce PostgreSQL shared_buffers in docker-compose.yml
POSTGRES_SHARED_BUFFERS=512MB  # Instead of 1GB

# Restart services
docker-compose restart
```

### SSL Certificate Renewal Failed

```bash
# Check certbot logs
docker-compose logs certbot

# Manual renewal
docker-compose run --rm certbot renew

# Reload Nginx
docker-compose exec nginx nginx -s reload
```

### Port Already in Use

```bash
# Check what's using port 80/443
sudo lsof -i :80
sudo lsof -i :443

# Kill process or change ports in docker-compose.yml
```

### Events Not Being Tracked

1. **Check SDK is loaded:**
   ```javascript
   console.log(window.customerJourney);
   ```

2. **Check browser console** for errors

3. **Verify API endpoint:**
   ```bash
   curl https://yourdomain.com/api/v1/events/batch
   ```

4. **Check CORS headers:**
   ```bash
   curl -I https://yourdomain.com/api/v1/events/batch \
       -H "Origin: https://your-frontend.com"
   ```

### Disk Space Full

```bash
# Check disk usage
df -h

# Clean Docker
docker system prune -a --volumes

# Clean old logs
docker-compose exec app find /app/logs -mtime +7 -delete

# Reduce retention policies in TimescaleDB
```

---

## Maintenance Tasks

### Weekly

- ✅ Check disk usage
- ✅ Review application logs for errors
- ✅ Verify backups are running

### Monthly

- ✅ Update system packages
- ✅ Review performance metrics
- ✅ Test backup restoration
- ✅ Check SSL certificate expiration

### Quarterly

- ✅ Review and optimize database queries
- ✅ Update Docker images
- ✅ Security audit
- ✅ Capacity planning review

---

## Security Checklist

- ✅ Firewall enabled (UFW)
- ✅ Fail2ban installed and active
- ✅ SSH key authentication only (disable password auth)
- ✅ Database password changed from default
- ✅ API key salt changed from default
- ✅ HTTPS/SSL enabled
- ✅ Regular backups enabled
- ✅ Non-root user for Docker containers
- ✅ CORS properly configured
- ✅ Rate limiting enabled (Nginx)

---

## Performance Optimization

### For Small Scale (<10K events/day)

Current configuration is optimal. No changes needed.

### If Experiencing Slowness

1. **Increase PostgreSQL shared_buffers:**
   ```yaml
   POSTGRES_SHARED_BUFFERS=1.5GB  # Increase from 1GB
   ```

2. **Add database indexes:**
   ```sql
   CREATE INDEX CONCURRENTLY idx_events_custom ON events USING GIN (custom_properties);
   ```

3. **Enable Redis persistence:**
   ```yaml
   command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru --appendonly yes --appendfsync everysec
   ```

4. **Increase worker count:**
   ```yaml
   WORKERS=8  # Increase from 4
   ```

---

## Support Resources

**Documentation:**
- Main README: `/docs/customer-journey-tool/README.md`
- Schemas: `/docs/customer-journey-tool/schemas.py`
- Templates: `/docs/customer-journey-tool/templates/`

**Logs Location:**
```bash
# Application logs
docker-compose logs app

# Nginx logs
docker-compose exec nginx tail -f /var/log/nginx/journey_access.log

# PostgreSQL logs
docker-compose logs postgres
```

**Common Commands:**

```bash
# Restart all services
docker-compose restart

# View resource usage
docker stats

# Clean up
docker system prune

# Update services
docker-compose pull
docker-compose up -d
```

---

## Success Checklist

- ✅ VPS provisioned and configured
- ✅ DNS pointing to VPS IP
- ✅ SSL certificate obtained
- ✅ Docker services running
- ✅ Database initialized
- ✅ API accessible via HTTPS
- ✅ SDK serving correctly
- ✅ Automatic backups configured
- ✅ Monitoring set up
- ✅ First test event tracked successfully

---

**Deployment Complete! 🎉**

Your Customer Journey Analysis Tool is now live and ready to track customer interactions.

**Next Steps:**
1. Deploy JavaScript SDK to your website
2. Configure first conversion funnel
3. Set up Obsidian vault sync
4. Create drop-off alerts

---

**Need Help?**
- GitHub Issues: https://github.com/sathyan17-1980/Obsidian_Agent/issues
- Email: support@yourdomain.com
