# JWT Authentication Implementation

## Overview

This document outlines the JWT (JSON Web Token) authentication system implemented for the LMS platform. The authentication system provides secure access to the API endpoints and enables role-based access control.

## Components

1. **User Model**
   - Located in `backend/app/models/user.py`
   - Stores user information including username, email, hashed password, and role
   - Roles include: admin, teacher, and student

2. **User Schemas**
   - Located in `backend/app/schemas/user_schemas.py`
   - Defines data validation schemas for user operations
   - Includes schemas for user creation, update, retrieval, and token handling

3. **Authentication Service**
   - Located in `backend/app/services/auth.py`
   - Provides functions for JWT token generation and validation
   - Implements password hashing using bcrypt
   - Includes dependency functions for securing routes

4. **User CRUD Operations**
   - Located in `backend/app/crud/user_crud.py`
   - Implements database operations for user management
   - Includes functions for user creation, retrieval, update, and deletion

5. **Authentication Routes**
   - Located in `backend/app/routes/auth_routes.py`
   - Provides endpoints for user registration and login
   - Implements OAuth2 compatible token login

6. **User Management Routes**
   - Located in `backend/app/routes/user_routes.py`
   - Provides endpoints for administrator user management
   - Implements role-based access control

## Security Features

1. **Password Hashing**
   - Passwords are never stored in plain text
   - Uses bcrypt for secure password hashing
   - Implements password verification for authentication

2. **JWT Token Security**
   - Tokens include expiration timestamps
   - Includes user role information for authorization
   - Uses HS256 algorithm for signing tokens

3. **Role-Based Access Control**
   - Admin users have full access to all endpoints
   - Teachers have access to content creation and student data
   - Students can only access their own data and public resources

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - OAuth2 compatible token login
- `POST /api/auth/login/simple` - Simple login with username/password in request body
- `GET /api/auth/me` - Get current authenticated user

### User Management (Admin only)

- `GET /api/users/` - List all users
- `POST /api/users/` - Create a new user
- `GET /api/users/{user_id}` - Get specific user
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user

## Integration with Exercise System

The JWT authentication system is fully integrated with the exercise system:

- Exercise templates can only be created by teachers or admins
- Exercise content creation requires teacher or admin privileges
- Exercise responses are associated with the authenticated user
- Users can only view their own response history (admins/teachers can view all)

## Token Usage

To use the authentication system:

1. Register a user or login with credentials
2. Receive a JWT token in the response
3. Include the token in subsequent requests as a Bearer token:
   ```
   Authorization: Bearer <token>
   ```

## Database Migration

A new Alembic migration file (`add_user_auth_tables.py`) has been created to add:
- The `users` table
- Required modifications to the `user_responses` table
- Foreign key relationships

Run the migration with: `alembic upgrade head` 