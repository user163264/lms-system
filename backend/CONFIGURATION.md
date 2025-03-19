# LMS Configuration System

This document explains how the LMS backend configuration system works and how to customize it.

## Overview

The LMS backend uses a centralized configuration system that:

1. Provides sensible defaults for all settings
2. Allows overriding via environment variables
3. Groups related settings together
4. Makes configuration access consistent throughout the codebase

## Configuration Structure

All configuration settings are centralized in the `app/config/settings.py` file and exposed through the `app/config/__init__.py` module. Settings are categorized into these sections:

- **Database Settings**: Database connection parameters
- **API Settings**: FastAPI application configuration
- **CORS Settings**: Cross-Origin Resource Sharing configuration
- **Auth Settings**: JWT authentication parameters
- **File Storage Settings**: Upload directories and limits
- **Logging Settings**: Log formats, levels, and output locations
- **Application Settings**: General application parameters

## How to Configure the Application

### Using Environment Variables

All settings can be customized by setting environment variables. The naming convention is:

```
LMS_SECTION_NAME
```

For example, to change the database password:

```bash
export LMS_DB_PASSWORD=your_secure_password
```

### Using .env File

For convenience, you can create a `.env` file in the backend directory. Copy the provided `.env.example` file as a starting point:

```bash
cp .env.example .env
```

Then edit the `.env` file to customize your settings.

### Environment Variable Precedence

Settings are loaded in this order (later sources override earlier ones):

1. Default values in `settings.py`
2. Environment variables

## Available Settings

See `.env.example` for a complete list of available settings with their default values and descriptions.

## How to Use Settings in Code

To use settings in your code, import them from the config package:

```python
from app.config import DATABASE_URL, JWT_SECRET_KEY

# Use the settings
db_connection = create_connection(DATABASE_URL)
```

## Adding New Settings

To add new settings:

1. Add the setting to `app/config/settings.py` with an appropriate default value
2. Add the setting to the imports in `app/config/__init__.py`
3. Update `.env.example` with documentation for the new setting
4. Update this documentation if necessary

## Security Considerations

- Never commit secrets to version control
- Use strong, unique passwords for all credentials
- Always override security-sensitive settings (like `JWT_SECRET_KEY`) in production
- Consider using a secrets management system for production deployments 