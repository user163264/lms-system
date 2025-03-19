# Service Management Scripts

This directory contains scripts for managing the LMS system services.

## Subdirectories

### check

Scripts in this directory are used for checking the status and health of services:

- `check_services.py` - Checks the status of all LMS services (database, backend, frontend)

### control

Scripts in this directory are used for controlling services (start, stop, restart):

- `start_backend.sh` - Starts the backend API service
- `start_frontend.sh` - Starts the frontend service

## Usage

### Checking Services

To check the status of all services:

```bash
python scripts/services/check/check_services.py
```

This will output the status of each service and exit with a non-zero code if any service is not running properly.

### Starting Services

To start the backend service:

```bash
./scripts/services/control/start_backend.sh
```

To start the frontend service:

```bash
./scripts/services/control/start_frontend.sh
```

These scripts will handle environment setup and start the respective services. 