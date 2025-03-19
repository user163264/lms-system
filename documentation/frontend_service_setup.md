# Frontend Service Setup

## Overview

This document outlines the setup of the Next.js frontend as a systemd service to ensure it always runs on the correct port and automatically restarts on system reboots or crashes.

## Problem Solved

Previously, the Next.js server was started manually or through various scripts, which led to inconsistencies:

1. Sometimes the server would run on port 3001 while Nginx was configured for port 3000
2. The server would not automatically restart after system reboots
3. Manual intervention was required when processes crashed

## Solution Implemented

A systemd service has been created to manage the Next.js frontend application:

1. The service ensures Next.js always runs on port 3000
2. It starts automatically when the system boots
3. It restarts automatically if the application crashes
4. It maintains consistency with the Nginx configuration

## Implementation Details

### 1. Startup Script

Location: `/home/ubuntu/lms/start-frontend.sh`

```bash
#!/bin/bash

# Startup script for Spotvogel LMS frontend
cd /home/ubuntu/lms/frontend
export NODE_ENV=production
npm run dev -- -p 3000
```

### 2. Systemd Service File

Location: `/etc/systemd/system/lms-frontend.service`

```ini
[Unit]
Description=Spotvogel LMS Frontend
After=network.target nginx.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/lms/frontend
ExecStart=/home/ubuntu/lms/start-frontend.sh
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=lms-frontend
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

## Nginx Configuration

The Nginx configuration points to the Next.js server running on port 3000:

```nginx
location @nextjs {
    proxy_pass http://127.0.0.1:3000;  # Next.js frontend
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
}
```

## Management Commands

### Check Service Status

```bash
sudo systemctl status lms-frontend
```

### Start/Stop/Restart Service

```bash
sudo systemctl start lms-frontend
sudo systemctl stop lms-frontend
sudo systemctl restart lms-frontend
```

### Enable/Disable Automatic Start

```bash
sudo systemctl enable lms-frontend
sudo systemctl disable lms-frontend
```

### View Service Logs

```bash
sudo journalctl -u lms-frontend
```

## Troubleshooting

If the service fails to start:

1. Check logs: `sudo journalctl -u lms-frontend -n 50`
2. Verify the startup script is executable: `ls -la /home/ubuntu/lms/start-frontend.sh`
3. Ensure the Next.js application can run manually: `cd /home/ubuntu/lms/frontend && npm run dev -- -p 3000`

## Note for Future Development

When making changes to the frontend:

1. Build the changes: `cd /home/ubuntu/lms/frontend && npm run build`
2. Restart the service: `sudo systemctl restart lms-frontend`

The service is configured to always use port 3000, which matches the Nginx configuration, thus preventing port mismatch issues. 