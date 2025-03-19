# Import Scripts

This directory contains scripts for importing and exporting data in the LMS system.

## Scripts

- `import_exercise.py` - Script for importing exercise data into the system

## Usage

### Importing Exercises

To import exercises from a JSON file:

```bash
python scripts/import/import_exercise.py --file /path/to/exercises.json
```

#### Supported Formats

- JSON file with exercise data
- CSV file with exercise data (using the --format csv flag)

#### Options

- `--file` - Path to the file containing exercise data
- `--format` - Format of the input file (json or csv, defaults to json)
- `--validate` - Validate exercise data without importing
- `--update` - Update existing exercises if they exist

## Prerequisites

Before running import scripts:

1. Ensure the database is properly set up
2. Verify the data format matches the expected schema
3. Consider running in validate mode first to check for errors 