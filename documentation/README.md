# LMS Documentation

This directory contains comprehensive documentation for the Learning Management System (LMS).

## Server Information

- **Public IP Address**: 13.42.249.90
- **Hostname**: lms-spotvogel
- **Environment**: Production

## Documentation Sections

### Setup & Installation
- [Database Setup](setup/database_setup.md)
- [Backend Installation](setup/backend_installation.md)
- [Frontend Setup](setup/frontend_setup.md)
- [Production Deployment](setup/production_deployment.md)
- [Backup Procedures](setup/backup_procedures.md)

### Development Guides
- [Coding Workflow](development/coding_workflow.md)
- [Database Migration](database/README.md)
- [Exercise Types](development/exercise_types.md)
- [Frontend Development](development/frontend_development.md)
- [Backend Development](development/backend_development.md)
- [Authentication Implementation](development/jwt_auth_implementation.md)

### Architecture
- [LMS Overview](architecture/lms_overview.md)
- [Backend Structure](architecture/backend_structure.md)
- [Frontend Architecture](architecture/frontend_architecture.md)
- [Database Schema](architecture/database_schema.md)

### API Documentation
- [API Overview](api/api_overview.md)
- [Authentication](api/authentication.md)
- [Courses & Lessons](api/courses_lessons.md)
- [Exercises & Submissions](api/exercises_submissions.md)
- [Users & Profiles](api/users_profiles.md)

### Configuration
- [Port Configuration](configuration/port_configuration.md)
- [Nginx Configuration](configuration/nginx_configuration.md)
- [Environment Variables](configuration/environment_variables.md)

### Troubleshooting
- [Common Issues](troubleshooting/common_issues.md)
- [Hydration Error Solutions](troubleshooting/hydration_error_solution.md)
- [Database Troubleshooting](troubleshooting/database_troubleshooting.md)
- [Frontend Issues](troubleshooting/frontend_issues.md)

### Logging System
- [Logging Overview](logging_guide.md)
- [Production Log Aggregation](log_aggregation.md)

### User Guides
- [Administrator Guide](user-guides/administrator_guide.md)
- [Teacher Guide](user-guides/teacher_guide.md)
- [Student Guide](user-guides/student_guide.md)

## Recent Documentation Updates

- Added server IP information to documentation
- Created backup procedures documentation
- Added Nginx configuration documentation
- Fixed incorrectly dated troubleshooting file
- Updated port configuration implementation to match documented standards
- Added comprehensive logging system documentation
- Consolidated database documentation into a single section
- Reorganized exercise type documentation

## Documentation Standards

All documentation should follow these standards:
1. Use Markdown format for all documentation files
2. Follow consistent heading structure (# for title, ## for sections, ### for subsections)
3. Include code examples where appropriate, using proper syntax highlighting
4. Keep documentation up to date with code changes
5. Include visuals (diagrams, screenshots) when they aid understanding
6. Provide cross-references to related documentation
7. Follow the directory structure organization by topic area

## Contributing

When adding new documentation:
1. Place files in the appropriate subdirectory
2. Add a link to the new documentation in the main README.md
3. Follow the documentation standards above
4. Update the "Recent Documentation Updates" section as needed 