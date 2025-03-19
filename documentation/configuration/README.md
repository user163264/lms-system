# LMS Configuration Documentation

This directory contains documentation related to the configuration of the LMS system.

## Available Documentation

- [Port Configuration](port_configuration.md) - Details on configuring ports for all services
- [Configuration Variables Reference](config_variables.html) - Comprehensive HTML reference of all configuration variables

## Using the Configuration Variables Reference

The `config_variables.html` file provides a searchable, complete reference of all configuration variables in the LMS system. It includes:

- Default values
- Descriptions
- Where to configure each variable
- Categorized sections for different aspects of the system

To use it:
1. Open the file in any web browser
2. Use the search box to quickly find specific variables
3. Browse by category to understand configuration options for each system component

## Configuration Best Practices

1. Always use environment variables or `.env` files for sensitive information
2. Follow the established naming conventions when adding new configuration variables
3. Document new configuration variables in both code and the configuration reference
4. Use the default values where appropriate
5. Test configuration changes in a development environment before deploying to production 