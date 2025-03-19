# Frontend Scripts

This directory contains scripts for managing the frontend of the LMS system.

## Scripts

- `update_structure.sh` - Script for updating the frontend directory structure

## Usage

### Updating Frontend Structure

To update the frontend directory structure:

```bash
./scripts/frontend/update_structure.sh
```

This script:
1. Creates a structured directory layout
2. Moves components to appropriate locations
3. Consolidates test directories
4. Updates .gitignore for log files
5. Removes redundant configuration files

## Prerequisites

Before running frontend scripts:

1. Ensure you have committed any important changes
2. Verify that the frontend dependencies are installed
3. Review script actions before execution 