# Model Management Scripts

This directory contains scripts for managing the data models and schema in the LMS system.

## Scripts

- `fix_models.py` - Consolidated script for fixing model-related issues
- `update_schema.py` - Updates the database schema based on model definitions

## Usage

### Fixing Models

To fix model-related issues:

```bash
python scripts/models/fix_models.py
```

This script consolidates various model fix operations including schema fixes, model save fixes, and database save fixes.

### Updating Schema

To update the database schema based on model definitions:

```bash
python scripts/models/update_schema.py
```

This will analyze the current models and update the database schema accordingly. 