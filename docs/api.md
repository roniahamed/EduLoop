# Eduloop API Documentation

## Overview
Eduloop provides a RESTful API for managing educational questions in a hierarchical structure: Groups > Subjects > Categories > Subcategories > Questions. The API supports CRUD operations on the hierarchy, session-based question retrieval for quizzes, and bulk question uploads. Authentication is handled via custom AccessTokens.

**Base URL:** `/api/`

**Version:** 1.0.0

**Authentication:** Most endpoints require authentication. Use `Authorization: Token <token>` header or validate tokens via `/api/token-verify/`. Write operations (POST) require admin privileges.

**Pagination:** List endpoints support pagination with `page` and `page_size` query parameters (default page_size=10, max=100).

**Bulk Operations:** Create endpoints accept single objects or lists for bulk creation.

**Error Handling:** Standard HTTP status codes. Validation errors include field-specific messages.

## Authentication

### Validate Access Token
- **Endpoint:** `POST /api/token-verify/`
- **Description:** Validate an AccessToken key.
- **Auth Required:** No
- **Request Body:**
  ```json
  {
    "key": "12345678"
  }
  ```
- **Success Response (200):**
  ```json
  {
    "message": "Das Token ist gültig."
  }
  ```
- **Error Response (400):**
  ```json
  {
    "error": "Ungültiges oder inaktives Token."
  }
  ```

### Obtain DRF Token (if applicable)
- **Endpoint:** `POST /api/api-token-auth/`
- **Description:** Obtain a DRF authentication token (requires user credentials).
- **Auth Required:** No
- **Request Body:**
  ```json
  {
    "username": "admin",
    "password": "password"
  }
  ```
- **Success Response (200):**
  ```json
  {
    "token": "abc123..."
  }
  ```

## Groups

### List Groups
- **Endpoint:** `GET /api/groups/`
- **Description:** Retrieve a paginated list of all groups.
- **Auth Required:** Yes (read-only)
- **Query Params:** `page`, `page_size`
- **Success Response (200):**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Mathematics",
        "description": "Math-related questions",
        "created_at": "2023-01-01T00:00:00Z"
      }
    ]
  }
  ```

### Create Group(s)
- **Endpoint:** `POST /api/groups/`
- **Description:** Create one or more groups.
- **Auth Required:** Yes (admin)
- **Request Body:** Single object or list
  ```json
  [
    {
      "name": "Science",
      "description": "Science questions"
    }
  ]
  ```
- **Success Response (201):**
  ```json
  [
    {
      "id": 2,
      "name": "Science",
      "description": "Science questions",
      "created_at": "2023-01-01T00:00:00Z"
    }
  ]
  ```
- **Error Response (400):** Validation errors (e.g., duplicate name)

## Subjects

### List Subjects
- **Endpoint:** `GET /api/subjects/`
- **Description:** Retrieve a paginated list of all subjects.
- **Auth Required:** Yes (read-only)
- **Query Params:** `page`, `page_size`
- **Success Response (200):** Similar to groups, includes `group` (group name)

### Create Subject(s)
- **Endpoint:** `POST /api/subjects/`
- **Description:** Create one or more subjects.
- **Auth Required:** Yes (admin)
- **Request Body:**
  ```json
  [
    {
      "name": "Algebra",
      "description": "Algebra topics",
      "group": "Mathematics"
    }
  ]
  ```
- **Success Response (201):** Created subjects
- **Error Response (400):** Invalid group or duplicate name in group

### List Subjects by Group
- **Endpoint:** `GET /api/subject/{group_id}/`
- **Description:** Retrieve subjects for a specific group.
- **Auth Required:** Yes (read-only)
- **Path Params:** `group_id` (integer)
- **Query Params:** `page`, `page_size`
- **Success Response (200):**
  ```json
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Algebra",
        "description": "Algebra topics",
        "group": "Mathematics",
        "created_at": "2023-01-01T00:00:00Z"
      },
      {
        "id": 2,
        "name": "Geometry",
        "description": "Geometry topics",
        "group": "Mathematics",
        "created_at": "2023-01-01T00:00:00Z"
      }
    ]
  }
  ```
- **Error Response (404):** Group not found

## Categories

### List Categories
- **Endpoint:** `GET /api/categories/`
- **Description:** Retrieve a paginated list of all categories.
- **Auth Required:** Yes (read-only)
- **Query Params:** `page`, `page_size`
- **Success Response (200):** Includes `subject` and `group` (names)

### Create Category(ies)
- **Endpoint:** `POST /api/categories/`
- **Description:** Create one or more categories.
- **Auth Required:** Yes (admin)
- **Request Body:**
  ```json
  [
    {
      "name": "Linear Equations",
      "subject": "Algebra",
      "group": "Mathematics"
    }
  ]
  ```
- **Success Response (201):** Created categories
- **Error Response (400):** Invalid subject/group or duplicate

### List Categories by Subject
- **Endpoint:** `GET /api/categories/{subject_id}/`
- **Description:** Retrieve categories for a specific subject.
- **Auth Required:** Yes (read-only)
- **Path Params:** `subject_id` (integer)
- **Query Params:** `page`, `page_size`
- **Success Response (200):**
  ```json
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Linear Equations",
        "subject": "Algebra",
        "group": "Mathematics",
        "created_at": "2023-01-01T00:00:00Z"
      },
      {
        "id": 2,
        "name": "Quadratic Equations",
        "subject": "Algebra",
        "group": "Mathematics",
        "created_at": "2023-01-01T00:00:00Z"
      }
    ]
  }
  ```
- **Error Response (404):** Subject not found

## Subcategories

### List Subcategories
- **Endpoint:** `GET /api/subcategories/`
- **Description:** Retrieve a paginated list of all subcategories.
- **Auth Required:** Yes (read-only)
- **Query Params:** `page`, `page_size`
- **Success Response (200):** Includes `category`, `subject`, `group` (names)

### Create Subcategory(ies)
- **Endpoint:** `POST /api/subcategories/`
- **Description:** Create one or more subcategories.
- **Auth Required:** Yes (admin)
- **Request Body:**
  ```json
  [
    {
      "name": "Basic Equations",
      "category": "Linear Equations",
      "subject": "Algebra",
      "group": "Mathematics"
    }
  ]
  ```
- **Success Response (201):** Created subcategories
- **Error Response (400):** Invalid relations or duplicate

### List Subcategories by Category
- **Endpoint:** `GET /api/subcategories/{category_id}/`
- **Description:** Retrieve subcategories for a specific category.
- **Auth Required:** Yes (read-only)
- **Path Params:** `category_id` (integer)
- **Query Params:** `page`, `page_size`
- **Success Response (200):**
  ```json
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Basic Linear Equations",
        "category": "Linear Equations",
        "subject": "Algebra",
        "group": "Mathematics",
        "created_at": "2023-01-01T00:00:00Z"
      },
      {
        "id": 2,
        "name": "Advanced Linear Equations",
        "category": "Linear Equations",
        "subject": "Algebra",
        "group": "Mathematics",
        "created_at": "2023-01-01T00:00:00Z"
      }
    ]
  }
  ```
- **Error Response (404):** Category not found

## Questions

### Start Question Session
- **Endpoint:** `POST /api/questions/`
- **Description:** Start a new question session with filters. Initializes session state for random question retrieval.
- **Auth Required:** Yes
- **Request Body:**
  ```json
  {
    "group_id": 1,
    "subject_id": 2,
    "category_ids": [3, 4],  // optional
    "subcategory_ids": [5],  // optional, overrides category_ids if provided
    "levels": ["easy", "medium"]  // optional
  }
  ```
- **Success Response (200):** First question in session (see GET below)
- **Error Response (400):** Missing group/subject

### Get Next Question
- **Endpoint:** `GET /api/questions/`
- **Description:** Retrieve the next random unseen question from the active session. Uses batches of 50 questions.
- **Auth Required:** Yes
- **Success Response (200):**
  ```json
  {
    "id": 10,
    "group": "Mathematics",
    "subject": "Algebra",
    "category": "Linear Equations",
    "subcategory": "Basic Equations",
    "level": "easy",
    "type": "mcq",
    "metadata": {"question": "What is 2+2?", "options": ["3", "4"], "answer": "4"},
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
  ```
- **Error Response (400):** No active session
- **Error Response (404):** No more questions available

### Reset Question Session
- **Endpoint:** `DELETE /api/questions/`
- **Description:** Clear the current session state.
- **Auth Required:** Yes
- **Success Response (200):**
  ```json
  {
    "message": "Question session has been reset."
  }
  ```

## Bulk Question Upload
- **Endpoint:** `POST /api/upload-questions/`
- **Description:** Bulk create questions. Relations must exist; errors reported for invalid items.
- **Auth Required:** Yes (admin)
- **Request Body:** List of question objects
  ```json
  [
    {
      "group": "Mathematics",
      "subject": "Algebra",
      "category": "Linear Equations",
      "subcategory": "Basic Equations",  // optional
      "level": "easy",
      "type": "mcq",
      "metadata": {"question": "Solve x+1=2", "answer": "x=1"}
    }
  ]
  ```
- **Success Response (201/207):**
  ```json
  {
    "message": "Successfully uploaded 1 out of 1 questions."
  }
  ```
- **Partial Success (207):** Includes `failed_items` array with row numbers and errors
- **Error Response (400):** Invalid format or all items failed

## Models

### Group
- `id` (int): Primary key
- `name` (str): Unique name
- `description` (str): Optional
- `created_at` (datetime)

### Subject
- `id` (int)
- `name` (str): Unique per group
- `description` (str): Optional
- `group` (str): Group name
- `created_at` (datetime)

### Category
- `id` (int)
- `name` (str): Unique per subject/group
- `subject` (str): Subject name
- `group` (str): Group name
- `created_at` (datetime)

### SubCategory
- `id` (int)
- `name` (str): Unique per category/subject/group
- `category` (str): Category name
- `subject` (str): Subject name
- `group` (str): Group name
- `created_at` (datetime)

### Question
- `id` (int)
- `group` (str): Group name
- `subject` (str): Subject name
- `category` (str): Category name
- `subcategory` (str): Subcategory name (optional)
- `level` (str): "easy", "medium", "advance"
- `type` (str): Question type (e.g., "mcq")
- `metadata` (dict): JSON field for question data
- `created_at` (datetime)
- `updated_at` (datetime)

### AccessToken
- `key` (str): 8-digit unique key
- `description` (str): Optional
- `is_active` (bool)
- `created_at` (datetime)

## Notes
- All names are case-sensitive for lookups.
- Question sessions are per-user (via Django sessions).
- Bulk uploads skip invalid items but report errors.
- For production, ensure HTTPS and proper token management.
