#!/bin/sh
# =============================================================================
# Automated Backup Script for Customer Journey Analysis Tool
# Runs daily via cron in backup container
# =============================================================================

set -e  # Exit on error

# Configuration
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=${BACKUP_RETENTION_DAYS:-7}

# Database connection
PGHOST="postgres"
PGPORT="5432"
PGUSER="${POSTGRES_USER:-journey_user}"
PGDATABASE="${POSTGRES_DB:-customer_journey}"
export PGPASSWORD="${POSTGRES_PASSWORD}"

# =============================================================================
# Functions
# =============================================================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# =============================================================================
# PostgreSQL Backup
# =============================================================================
backup_postgres() {
    log "Starting PostgreSQL backup..."

    BACKUP_FILE="${BACKUP_DIR}/postgres_${TIMESTAMP}.sql.gz"

    pg_dump -h ${PGHOST} -p ${PGPORT} -U ${PGUSER} -d ${PGDATABASE} \
        --format=plain --no-owner --no-acl \
        | gzip > "${BACKUP_FILE}"

    if [ $? -eq 0 ]; then
        log "PostgreSQL backup completed: ${BACKUP_FILE}"
        log "Backup size: $(du -h ${BACKUP_FILE} | cut -f1)"
    else
        log "ERROR: PostgreSQL backup failed!"
        return 1
    fi
}

# =============================================================================
# Obsidian Vault Backup
# =============================================================================
backup_obsidian() {
    log "Starting Obsidian vault backup..."

    BACKUP_FILE="${BACKUP_DIR}/obsidian_${TIMESTAMP}.tar.gz"

    tar -czf "${BACKUP_FILE}" -C /obsidian_vault .

    if [ $? -eq 0 ]; then
        log "Obsidian vault backup completed: ${BACKUP_FILE}"
        log "Backup size: $(du -h ${BACKUP_FILE} | cut -f1)"
    else
        log "ERROR: Obsidian vault backup failed!"
        return 1
    fi
}

# =============================================================================
# Redis Backup (Optional - data is ephemeral)
# =============================================================================
backup_redis() {
    log "Starting Redis backup..."

    BACKUP_FILE="${BACKUP_DIR}/redis_${TIMESTAMP}.rdb"

    cp /redis_data/dump.rdb "${BACKUP_FILE}" 2>/dev/null || true

    if [ -f "${BACKUP_FILE}" ]; then
        log "Redis backup completed: ${BACKUP_FILE}"
    else
        log "No Redis dump file found (this is normal if Redis hasn't persisted yet)"
    fi
}

# =============================================================================
# Cleanup Old Backups
# =============================================================================
cleanup_old_backups() {
    log "Cleaning up backups older than ${RETENTION_DAYS} days..."

    find ${BACKUP_DIR} -name "postgres_*.sql.gz" -type f -mtime +${RETENTION_DAYS} -delete
    find ${BACKUP_DIR} -name "obsidian_*.tar.gz" -type f -mtime +${RETENTION_DAYS} -delete
    find ${BACKUP_DIR} -name "redis_*.rdb" -type f -mtime +${RETENTION_DAYS} -delete

    log "Cleanup completed"
}

# =============================================================================
# Backup Verification
# =============================================================================
verify_backups() {
    log "Verifying backups..."

    POSTGRES_BACKUP="${BACKUP_DIR}/postgres_${TIMESTAMP}.sql.gz"
    OBSIDIAN_BACKUP="${BACKUP_DIR}/obsidian_${TIMESTAMP}.tar.gz"

    # Check PostgreSQL backup
    if [ -f "${POSTGRES_BACKUP}" ]; then
        SIZE=$(stat -c%s "${POSTGRES_BACKUP}")
        if [ ${SIZE} -gt 1000 ]; then
            log "✓ PostgreSQL backup verified (${SIZE} bytes)"
        else
            log "⚠ WARNING: PostgreSQL backup seems too small (${SIZE} bytes)"
        fi
    else
        log "✗ PostgreSQL backup file not found!"
        return 1
    fi

    # Check Obsidian backup
    if [ -f "${OBSIDIAN_BACKUP}" ]; then
        SIZE=$(stat -c%s "${OBSIDIAN_BACKUP}")
        log "✓ Obsidian backup verified (${SIZE} bytes)"
    else
        log "⚠ WARNING: Obsidian backup file not found"
    fi

    log "Backup verification completed"
}

# =============================================================================
# Main Execution
# =============================================================================

log "=========================================="
log "Starting backup process"
log "=========================================="

# Create backup directory if it doesn't exist
mkdir -p ${BACKUP_DIR}

# Perform backups
backup_postgres
backup_obsidian
backup_redis

# Verify backups
verify_backups

# Cleanup old backups
cleanup_old_backups

log "=========================================="
log "Backup process completed successfully"
log "=========================================="

# Calculate total backup size
TOTAL_SIZE=$(du -sh ${BACKUP_DIR} | cut -f1)
log "Total backup storage used: ${TOTAL_SIZE}"

exit 0
