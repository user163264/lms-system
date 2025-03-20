# Backup Procedures

This document outlines the backup procedures for the LMS Spotvogel system.

## Overview

Regular backups are essential for data safety and disaster recovery. The LMS system has automated backup procedures for the database and critical configuration files.

## Backup Directory

All backups are stored in the `/home/ubuntu/lms/backups/` directory, organized by type and date.

## Database Backups

### Automated Schedule

Database backups are performed automatically on the following schedule:

- **Daily backups**: Every day at 1:00 AM UTC
- **Weekly backups**: Every Sunday at 2:00 AM UTC
- **Monthly backups**: First day of each month at 3:00 AM UTC

### Backup Retention

- Daily backups are kept for 7 days
- Weekly backups are kept for 4 weeks
- Monthly backups are kept for 6 months

### Manual Database Backup

To manually create a database backup:

```bash
cd ~/lms
./scripts/backup_database.sh
```

The backup will be stored in the `~/lms/backups/database/` directory with a timestamp.

## Configuration Backups

System configuration files are backed up:

1. Automatically when significant changes are made
2. Weekly on Sunday at 4:00 AM UTC

Key configuration files that are backed up include:

- Nginx configurations
- Environment files (.env)
- Systemd service files
- Frontend and backend configuration files

## Backup Verification

Backups are automatically tested for integrity after creation. The verification process includes:

1. Checking file size and checksums
2. Testing database backup restoration on a test instance
3. Logging verification results

## Backup Restoration

### Database Restoration

To restore a database from backup:

```bash
cd ~/lms
./scripts/restore_database.sh backups/database/postgresql_backup_YYYY-MM-DD.sql
```

### Configuration Restoration

To restore configuration files:

```bash
cd ~/lms
./scripts/restore_configs.sh backups/configs/config_backup_YYYY-MM-DD.tar.gz
```

## Server IP Information

The server's public IP address is: **13.42.249.90**

All backup scripts automatically log the server IP for identification purposes. 