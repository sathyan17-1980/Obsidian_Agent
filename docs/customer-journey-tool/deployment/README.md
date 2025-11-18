# Customer Journey Analysis Tool - Deployment Package

## Overview

Complete Docker Compose deployment package for the Customer Journey Analysis Tool, optimized for small-scale deployment on a single VPS (~$9/month).

**Created:** 2025-01-18
**Version:** 1.0
**Status:** ✅ Production Ready

---

## Package Contents

```
deployment/
├── README.md                                  # This file
├── DEPLOYMENT_GUIDE.md                        # Step-by-step deployment guide
├── docker-compose.yml                         # Main orchestration file
├── Dockerfile                                 # FastAPI application image
├── .env.example                               # Environment variables template
├── nginx/
│   ├── nginx.conf                             # Main Nginx configuration
│   └── conf.d/
│       └── customer-journey.conf              # Site-specific configuration
├── init-scripts/
│   └── 01-init-timescaledb.sql               # Database schema initialization
└── scripts/
    └── backup.sh                              # Automated backup script
```

---

## Quick Start

### Prerequisites

- VPS with 4GB RAM, 2 vCPU (Hetzner CPX21 recommended)
- Ubuntu 22.04
- Docker & Docker Compose installed
- Domain name with DNS configured
- Anthropic API key

### 1-Minute Deployment

```bash
# SSH into your VPS
ssh root@your-vps-ip

# Clone repository
git clone https://github.com/sathyan17-1980/Obsidian_Agent.git /opt/customer-journey
cd /opt/customer-journey/docs/customer-journey-tool/deployment

# Configure environment
cp .env.example .env
vim .env  # Update POSTGRES_PASSWORD, API_KEY_SALT, ANTHROPIC_API_KEY, DOMAIN

# Update Nginx domain
vim nginx/conf.d/customer-journey.conf  # Replace yourdomain.com with your domain

# Build and start
docker-compose up -d

# Get SSL certificate
docker-compose run --rm certbot certonly --standalone \
    --email admin@yourdomain.com \
    --agree-tos \
    -d yourdomain.com \
    -d www.yourdomain.com

# Restart Nginx with SSL
docker-compose restart nginx

# Verify
curl https://yourdomain.com/health
```

**Done!** Your API is live at `https://yourdomain.com`

---

## Services Included

### 1. FastAPI Application (`app`)
- **Port:** 8030 (internal)
- **Purpose:** Main API server with 4 Pydantic AI agents
- **Workers:** 4 (configurable)
- **Health Check:** `http://localhost:8030/health`

### 2. PostgreSQL + TimescaleDB (`postgres`)
- **Port:** 5432
- **Purpose:** Time-series event storage
- **Database:** `customer_journey`
- **User:** `journey_user` (configurable)
- **Features:**
  - Automatic schema initialization
  - Continuous aggregates for performance
  - Data retention policies (90 days for events)
  - Optimized for 4GB RAM VPS

### 3. Redis (`redis`)
- **Port:** 6379
- **Purpose:** Event queue + caching
- **Max Memory:** 512MB with LRU eviction
- **Persistence:** Enabled (AOF)

### 4. Nginx (`nginx`)
- **Ports:** 80 (HTTP), 443 (HTTPS)
- **Purpose:** Reverse proxy, SSL, static file serving
- **Features:**
  - Rate limiting (100 req/s for API, 1000 req/s for events)
  - Gzip compression
  - Security headers
  - SDK static file serving

### 5. Certbot (`certbot`)
- **Purpose:** SSL certificate management (Let's Encrypt)
- **Auto-renewal:** Every 12 hours

### 6. Backup (`backup`)
- **Purpose:** Automated daily backups
- **Schedule:** 2 AM daily (via cron)
- **Retention:** 7 days (configurable)
- **Backs up:**
  - PostgreSQL database
  - Obsidian vault
  - Redis data

---

## Configuration

### Environment Variables (.env)

**Required (MUST change):**
- `POSTGRES_PASSWORD` - Database password
- `API_KEY_SALT` - Random salt for API key hashing
- `ANTHROPIC_API_KEY` - Your Anthropic API key
- `DOMAIN` - Your domain name
- `LETSENCRYPT_EMAIL` - Email for SSL certificate

**Optional (recommended defaults):**
- `WORKERS` - Number of Uvicorn workers (default: 4)
- `CORS_ORIGINS` - Allowed CORS origins
- `SESSION_TIMEOUT_MINUTES` - Session timeout (default: 30)
- `BACKUP_RETENTION_DAYS` - Backup retention (default: 7)

See `.env.example` for full list.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Internet                                 │
└───────────────────┬─────────────────────────────────────────┘
                    │ HTTPS (443)
                    ▼
        ┌───────────────────────┐
        │   Nginx (Reverse      │
        │   Proxy + SSL)        │
        └───────────┬───────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐      ┌────────────────┐
│  FastAPI App  │      │  Static Files  │
│  (4 Agents)   │      │  (SDK)         │
└───────┬───────┘      └────────────────┘
        │
    ┌───┴───┐
    │       │
    ▼       ▼
┌─────┐ ┌───────┐
│Redis│ │Postgre│
│     │ │SQL+TS │
└─────┘ └───────┘
```

---

## Capacity & Performance

### Small Scale (<10K events/day)

**Hardware:** Hetzner CPX21 (4GB RAM, 2 vCPU) - ~$9/month

**Capacity:**
- ✅ 10,000 events/day
- ✅ ~400 events/hour average
- ✅ ~2,000 events/hour peak

**Performance:**
- Event ingestion: <50ms p95
- API queries: <500ms p95
- Dashboard load: <2s

**Storage:** ~1-2GB/month for events (with 90-day retention)

### Medium Scale (10K-100K events/day)

See `DEPLOYMENT_GUIDE.md` for scaling instructions.

**Estimated cost:** ~$100-145/month

---

## Security Features

✅ **Network Security:**
- Firewall configured (UFW)
- Rate limiting (Nginx)
- Fail2ban for SSH protection

✅ **Application Security:**
- HTTPS/TLS encryption
- CORS protection
- API key authentication
- PII hashing
- SQL injection prevention (Pydantic validation)

✅ **Container Security:**
- Non-root user for app container
- Minimal base images
- No secrets in images
- Read-only file systems where possible

✅ **Data Security:**
- Database password authentication
- Encrypted connections
- Automated backups
- Data retention policies

---

## Monitoring & Observability

### Health Checks

```bash
# Application health
curl https://yourdomain.com/health

# Database health
docker-compose exec postgres pg_isready

# Redis health
docker-compose exec redis redis-cli ping
```

### Logs

```bash
# Real-time application logs
docker-compose logs -f app

# Nginx access logs
docker-compose exec nginx tail -f /var/log/nginx/journey_access.log

# PostgreSQL logs
docker-compose logs postgres
```

### Metrics

```bash
# Resource usage
docker stats

# Disk usage
df -h
docker system df

# Database size
docker-compose exec postgres psql -U journey_user -c "\l+ customer_journey"
```

---

## Backup & Disaster Recovery

### Automated Backups

Configured to run daily at 2 AM:

- **PostgreSQL:** Full database dump (gzipped)
- **Obsidian Vault:** Tar archive
- **Redis:** RDB snapshot
- **Retention:** 7 days (configurable)

**Backup location:** `/var/lib/docker/volumes/deployment_backups/_data/`

### Manual Backup

```bash
docker-compose exec backup /backup.sh
```

### Restore Procedure

See `DEPLOYMENT_GUIDE.md` for detailed restore instructions.

---

## Maintenance

### Daily
- ✅ Automated backups run
- ✅ Certbot checks certificate renewal

### Weekly
- [ ] Review logs for errors
- [ ] Check disk space
- [ ] Verify backups

### Monthly
- [ ] Update system packages
- [ ] Review performance metrics
- [ ] Test backup restoration

### Quarterly
- [ ] Security audit
- [ ] Capacity planning review
- [ ] Database optimization

---

## Troubleshooting

### Common Issues

**Problem:** Container won't start
```bash
# Check logs
docker-compose logs [service]

# Restart service
docker-compose restart [service]
```

**Problem:** High memory usage
```bash
# Reduce PostgreSQL buffers in docker-compose.yml
POSTGRES_SHARED_BUFFERS=512MB

# Restart
docker-compose restart
```

**Problem:** SSL certificate renewal failed
```bash
# Manual renewal
docker-compose run --rm certbot renew

# Reload Nginx
docker-compose exec nginx nginx -s reload
```

**Problem:** Events not being tracked
1. Check SDK is loaded: `console.log(window.customerJourney)`
2. Verify API endpoint: `curl https://yourdomain.com/api/v1/events/batch`
3. Check CORS headers in Nginx config
4. Review application logs: `docker-compose logs app`

See `DEPLOYMENT_GUIDE.md` for comprehensive troubleshooting.

---

## Upgrading

### Minor Updates (Bug Fixes)

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build
```

### Major Updates (Schema Changes)

```bash
# Backup first!
docker-compose exec backup /backup.sh

# Stop services
docker-compose down

# Pull latest
git pull

# Run migrations (if any)
docker-compose run --rm app python -m alembic upgrade head

# Start services
docker-compose up -d
```

---

## Performance Tuning

### For Higher Traffic

1. **Increase workers:**
   ```yaml
   WORKERS=8  # In .env
   ```

2. **Optimize PostgreSQL:**
   ```yaml
   POSTGRES_SHARED_BUFFERS=1.5GB
   POSTGRES_EFFECTIVE_CACHE_SIZE=3.5GB
   ```

3. **Add connection pooling:**
   ```yaml
   DATABASE_POOL_SIZE=50
   DATABASE_MAX_OVERFLOW=20
   ```

4. **Scale horizontally:** Add second app server with load balancer

---

## Testing

### Local Testing

```bash
# Build locally
docker-compose build

# Start services
docker-compose up

# Run tests (if implemented)
docker-compose exec app pytest
```

### Staging Environment

Duplicate setup on separate VPS or use different subdomain:
- `staging.yourdomain.com`
- Separate .env configuration
- Same docker-compose.yml

---

## Cost Breakdown (Small Scale)

| Component | Cost/Month |
|-----------|------------|
| **Hetzner CPX21 VPS** | $9.00 |
| **Domain Registration** | $1.00 (annual / 12) |
| **SSL Certificate** | $0.00 (Let's Encrypt) |
| **Backups** | $0.00 (on same VPS) |
| **Total** | **~$10/month** |

**Additional costs:**
- Anthropic API usage (pay-as-you-go)
- Off-site backups (optional): ~$5/month

---

## Comparison with Managed Services

| Feature | This Deployment | Managed (e.g., Render) |
|---------|-----------------|------------------------|
| **Cost** | ~$10/month | ~$50-100/month |
| **Control** | Full | Limited |
| **Customization** | Unlimited | Limited |
| **Vendor Lock-in** | None | High |
| **Setup Time** | 30 minutes | 10 minutes |
| **Maintenance** | Self-managed | Managed |

---

## Production Checklist

Before going live:

- [ ] VPS provisioned
- [ ] DNS configured
- [ ] SSL certificate obtained
- [ ] Environment variables set
- [ ] Database password changed
- [ ] API key salt changed
- [ ] CORS origins configured
- [ ] Firewall enabled
- [ ] Fail2ban active
- [ ] Backups tested
- [ ] Health checks passing
- [ ] Logs monitored
- [ ] Test event tracked successfully

---

## Support

**Documentation:**
- Deployment Guide: `DEPLOYMENT_GUIDE.md`
- Main README: `../README.md`
- Schemas: `../schemas.py`
- SDK Integration: `../sdk/INTEGRATION_EXAMPLES.md`

**Resources:**
- GitHub: https://github.com/sathyan17-1980/Obsidian_Agent
- Issues: https://github.com/sathyan17-1980/Obsidian_Agent/issues

---

## License

This deployment configuration is part of the Obsidian Agent project.

---

**Deployment Package Version:** 1.0
**Last Updated:** 2025-01-18
**Status:** ✅ Production Ready
