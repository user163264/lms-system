# LMS API Overview

This document provides a comprehensive overview of the LMS API, its structure, and usage patterns.

## API Base URL

- Development: `http://localhost:8000/api`
- Production: `http://13.42.249.90/api`

## Authentication

All API endpoints except for login and registration require authentication. Authentication is handled using JWT (JSON Web Tokens).

To authenticate requests, include the JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

For details on authentication, see [Authentication Documentation](./authentication.md).

## API Structure

The API is organized by resource type and follows RESTful conventions:

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/register` | User registration |
| POST | `/api/auth/refresh` | Refresh access token |
| POST | `/api/auth/logout` | User logout |

### User Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/me` | Get current user profile |
| GET | `/api/users/{user_id}` | Get user by ID |
| PUT | `/api/users/{user_id}` | Update user |
| DELETE | `/api/users/{user_id}` | Delete user |

### Course Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses` | List all courses |
| GET | `/api/courses/{course_id}` | Get course by ID |
| POST | `/api/courses` | Create new course |
| PUT | `/api/courses/{course_id}` | Update course |
| DELETE | `/api/courses/{course_id}` | Delete course |
| GET | `/api/courses/{course_id}/lessons` | List lessons in course |

### Lesson Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/lessons` | List all lessons |
| GET | `/api/lessons/{lesson_id}` | Get lesson by ID |
| POST | `/api/lessons` | Create new lesson |
| PUT | `/api/lessons/{lesson_id}` | Update lesson |
| DELETE | `/api/lessons/{lesson_id}` | Delete lesson |
| GET | `/api/lessons/{lesson_id}/exercises` | List exercises in lesson |

### Exercise Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/exercises` | List all exercises |
| GET | `/api/exercises/{exercise_id}` | Get exercise by ID |
| POST | `/api/exercises` | Create new exercise |
| PUT | `/api/exercises/{exercise_id}` | Update exercise |
| DELETE | `/api/exercises/{exercise_id}` | Delete exercise |
| POST | `/api/exercises/submit` | Submit exercise answer |

### Submission Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/submissions` | List user's submissions |
| GET | `/api/submissions/{submission_id}` | Get submission by ID |
| POST | `/api/submissions` | Create new submission |
| GET | `/api/users/{user_id}/submissions` | Get user's submissions |

### Log Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/logs` | Send client-side logs to server |

## Response Format

All API responses follow a consistent format:

### Success Response

```json
{
  "status": "success",
  "data": {
    // Response data here
  }
}
```

### Error Response

```json
{
  "status": "error",
  "message": "Error message",
  "detail": "Optional detailed error information"
}
```

## Status Codes

The API uses standard HTTP status codes:

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `204 No Content`: Request successful, no content to return
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## Pagination

List endpoints support pagination with the following query parameters:

- `page`: Page number (default: 1)
- `limit`: Number of items per page (default: 10)

Example:

```
GET /api/courses?page=2&limit=20
```

Response includes pagination metadata:

```json
{
  "status": "success",
  "data": {
    "items": [...],
    "pagination": {
      "total": 100,
      "pages": 5,
      "page": 2,
      "limit": 20,
      "has_next": true,
      "has_prev": true
    }
  }
}
```

## Filtering and Sorting

Many list endpoints support filtering and sorting:

- Filtering: `?filter_<field>=<value>`
- Sorting: `?sort=<field>` (ascending) or `?sort=-<field>` (descending)

Example:

```
GET /api/exercises?filter_type=multiple_choice&sort=-created_at
```

## Rate Limiting

API requests are rate-limited to prevent abuse. Current limits:

- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

Rate limit information is included in response headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1624982400
```

## API Versioning

The current API version is v1 (implicit in the routes). Future versions will include explicit version numbers in the URL.

## Error Handling

For detailed information on API error handling, see [Error Handling](./error_handling.md).

## Using the API with JavaScript

Example of making an authenticated API request:

```javascript
async function fetchCourses() {
  const token = localStorage.getItem('token');
  
  const response = await fetch('http://localhost:8000/api/courses', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message);
  }
  
  return response.json();
}
```

## API Documentation

Full API documentation is available using Swagger UI at `/docs` when running the backend locally. 