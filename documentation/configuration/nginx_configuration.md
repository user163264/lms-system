# Nginx Configuration

This document outlines the Nginx configuration for the LMS Spotvogel system.

## Active Configuration Files

The LMS system uses the following Nginx configuration files:

| File | Purpose | Status | Port |
|------|---------|--------|------|
| `lms.conf` | Main application routing | **ACTIVE** | 80 (public) |
| `docs.conf` | Documentation server within API | **DEPRECATED** | 8000 |
| `docs_standalone.conf` | Standalone documentation server | Testing only | 8000 |
| `documentation.conf` | Internal documentation | **ACTIVE** | Included in main server |

## Port Configuration

The Nginx configurations use the following ports:

- **Port 80**: Main HTTP server (public)
- **Port 3002**: Frontend service (internal)
- **Port 8000**: Backend API service (internal)

**Note:** The `docs.conf` and `docs_standalone.conf` files both use port 8000, which conflicts with the backend API port. These configurations should not be used simultaneously with the backend service.

## Server Public IP

The server's public IP address is: **13.42.249.90**

All publicly accessible services should be accessed through this IP address.

## Installation

To install the Nginx configuration:

1. Copy the appropriate configuration file to `/etc/nginx/sites-available/`:
   ```bash
   sudo cp lms.conf /etc/nginx/sites-available/lms
   ```

2. Create a symbolic link in `sites-enabled`:
   ```bash
   sudo ln -s /etc/nginx/sites-available/lms /etc/nginx/sites-enabled/
   ```

3. Test the configuration:
   ```bash
   sudo nginx -t
   ```

4. Restart Nginx:
   ```bash
   sudo systemctl restart nginx
   ```

## Environment Variable Support

The `lms.conf` file includes instructions for using environment variables in Nginx. This approach requires:

1. Installing the nginx-module-perl package
2. Loading the perl module in the main nginx.conf
3. Adding perl directives to access environment variables
4. Setting up the environment file in the systemd service configuration

See the comments in `lms.conf` for detailed instructions. 