# Django REST API - Book Management Management

## Overview
A Django REST Framework API for managing users, books, and reading lists. Features include user registration/login (JWT-based), book creation/removal, and reading list management. Tested using **Postman**.

## Prerequisites
- Python 3.8+
- Django 4.2+
- `djangorestframework`, `djangorestframework-simplejwt`

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd project_name
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run Server**:
   ```bash
   python manage.py runserver
   ```
   API available at `http://localhost:8000/api/`.

## Authentication
Uses **JWT** (`djangorestframework-simplejwt`). Include the access token in Postman:
- Header: `Authorization: Bearer <access_token>`

## Testing with Postman
1. Import the Postman collection (create one or use examples below).
2. Set the base URL to `http://localhost:8000/api/`.
3. Add `Content-Type: application/json` to request headers for POST/PUT requests.

## API Endpoints

### Authentication
1. **Register User**
   - **POST** `/users/register/`
   - **Body** (JSON):
     ```json
     {
         "username": "testuser",
         "email": "test@example.com",
         "password": "Secure123!",
         "password2": "Secure123!",
         "first_name": "Test",
         "last_name": "User"
     }
     ```
   - **Response** (201):
     ```json
     {"message": "User registered successfully"}
     ```
   - **Validations**:
     - `username`: Alphabets only, min 3 chars, unique.
     - `email`: Valid, unique.
     - `password`: Min 6 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char (@$!%*?&).
     - `password2`: Must match `password`.

2. **Login (Obtain JWT)**
   - **POST** `/users/login/`
   - **Body**:
     ```json
     {
         "username": "testuser",
         "password": "Secure123!"
     }
     ```
   - **Response** (200):
     ```json
     {
         "refresh": "<refresh_token>",
         "access": "<access_token>"
     }
     ```
   - **Postman**: Save `access` token for authenticated requests.

3. **Refresh Token**
   - **POST** `/users/token/refresh/`
   - **Body**:
     ```json
     {
         "refresh": "<refresh_token>"
     }
     ```
   - **Response** (200):
     ```json
     {"access": "<new_access_token>"}
     ```

4. **User Profile**
   - **GET/PUT** `/users/profile/`
   - **Permissions**: Authenticated
   - **Body (PUT)**:
     ```json
     {
         "first_name": "Updated",
         "last_name": "Name"
     }
     ```
   - **Response** (200):
     ```json
     {
         "username": "testuser",
         "email": "test@example.com",
         "first_name": "Updated",
         "last_name": "Name"
     }
     ```
   - **Postman**: Add `Authorization: Bearer <access_token>` to headers.

### Book Management
1. **List/Create Books**
   - **GET/POST** `/books/`
   - **Permissions**: GET (public), POST (authenticated)
   - **Body (POST)**:
     ```json
     {
         "title": "Sample Book",
         "authors": "Author Name",
         "genre": "Fiction",
         "publication_date": "2023-01-01",
         "description": "A sample book"
     }
     ```
   - **Response** (201):
     ```json
     {
         "id": 1,
         "title": "Sample Book",
         "authors": "Author Name",
         "genre": "Fiction",
         "publication_date": "2023-01-01",
         "description": "A sample book",
         "created_by": 1,
         "created_at": "2025-08-10T17:24:00Z",
         "updated_at": "2025-08-10T17:24:00Z"
     }
     ```
   - **Postman**: For POST, add `Authorization` header.

2. **Retrieve/Delete Book**
   - **GET/DELETE** `/books/<id>/`
   - **Permissions**: GET (public), DELETE (creator only)
   - **Response (DELETE)**: 204 or 403 (if not creator)
   - **Postman**: Add `Authorization` for DELETE.

### Reading Lists
1. **List/Create Reading Lists**
   - **GET/POST** `/reading-lists/`
   - **Permissions**: Authenticated
   - **Body (POST)**:
     ```json
     {
         "name": "My Favorites"
     }
     ```
   - **Response** (201):
     ```json
     {
         "id": 1,
         "user": 1,
         "name": "My Favorites",
         "created_at": "2025-08-10T17:24:00Z",
         "updated_at": "2025-08-10T17:24:00Z"
     }
     ```
   - **Postman**: Add `Authorization` header.

2. **Retrieve/Update/Delete Reading List**
   - **GET/PUT/DELETE** `/reading-lists/<id>/`
   - **Permissions**: Authenticated (owner only)
   - **Body (PUT)**:
     ```json
     {
         "name": "Updated Favorites"
     }
     ```

3. **Add/Remove Book from Reading List**
   - **POST** `/reading-lists/<id>/items/`, **DELETE** `/reading-lists/<id>/items/<book_id>/`
   - **Permissions**: Authenticated (owner only)
   - **Body (POST)**:
     ```json
     {
         "book_id": 1,
         "order": 1
     }
     ```
   - **Response** (201):
     ```json
     {
         "id": 1,
         "reading_list": 1,
         "book": {
             "id": 1,
             "title": "Sample Book",
             ...
         },
         "book_id": 1,
         "order": 1,
         "added_at": "2025-08-10T17:24:00Z"
     }
     ```
   - **Postman**: Add `Authorization` header.

## Postman Collection Example
Create a Postman collection with the following:
1. **Register**: POST `http://localhost:8000/api/users/register/`
   - Body: Raw JSON (see above).
2. **Login**: POST `http://localhost:8000/api/users/login/`
   - Save `access` token as an environment variable: `{{access_token}}`.
3. **Profile**: GET/PUT `http://localhost:8000/api/users/profile/`
   - Headers: `Authorization: Bearer {{access_token}}`
4. **Books**: GET/POST `http://localhost:8000/api/books/`
   - POST Headers: `Authorization: Bearer {{access_token}}`
5. **Reading Lists**: GET/POST `http://localhost:8000/api/reading-lists/`
   - Headers: `Authorization: Bearer {{access_token}}`
6. **Reading List Items**: POST/DELETE `http://localhost:8000/api/reading-lists/<id>/items/`
   - Headers: `Authorization: Bearer {{access_token}}`

## Error Handling
- **400 Bad Request**: Invalid input (e.g., mismatched passwords).
- **401 Unauthorized**: Missing/invalid JWT.
- **403 Forbidden**: Action not allowed (e.g., deleting another user's book).
- **404 Not Found**: Resource not found.
- Example error:
  ```json
  {"password": ["Passwords do not match."]}
  ```

## Notes
- Uses SQLite by default; configure PostgreSQL in `settings.py` for production.

# Django REST API - Book Management Management

## Overview
A Django REST Framework API for managing users, books, and reading lists. Features include user registration/login (JWT-based), book creation/removal, and reading list management. Tested using **Postman**.

## Prerequisites
- Python 3.8+
- Django 4.2+
- `djangorestframework`, `djangorestframework-simplejwt`

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd project_name
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run Server**:
   ```bash
   python manage.py runserver
   ```
   API available at `http://localhost:8000/api/`.

## Authentication
Uses **JWT** (`djangorestframework-simplejwt`). Include the access token in Postman:
- Header: `Authorization: Bearer <access_token>`

## Testing with Postman
1. Import the Postman collection (create one or use examples below).
2. Set the base URL to `http://localhost:8000/api/`.
3. Add `Content-Type: application/json` to request headers for POST/PUT requests.

## API Endpoints

### Authentication
1. **Register User**
   - **POST** `/users/register/`
   - **Body** (JSON):
     ```json
     {
         "username": "testuser",
         "email": "test@example.com",
         "password": "Secure123!",
         "password2": "Secure123!",
         "first_name": "Test",
         "last_name": "User"
     }
     ```
   - **Response** (201):
     ```json
     {"message": "User registered successfully"}
     ```
   - **Validations**:
     - `username`: Alphabets only, min 3 chars, unique.
     - `email`: Valid, unique.
     - `password`: Min 6 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char (@$!%*?&).
     - `password2`: Must match `password`.

2. **Login (Obtain JWT)**
   - **POST** `/users/login/`
   - **Body**:
     ```json
     {
         "username": "testuser",
         "password": "Secure123!"
     }
     ```
   - **Response** (200):
     ```json
     {
         "refresh": "<refresh_token>",
         "access": "<access_token>"
     }
     ```
   - **Postman**: Save `access` token for authenticated requests.

3. **Refresh Token**
   - **POST** `/users/token/refresh/`
   - **Body**:
     ```json
     {
         "refresh": "<refresh_token>"
     }
     ```
   - **Response** (200):
     ```json
     {"access": "<new_access_token>"}
     ```

4. **User Profile**
   - **GET/PUT** `/users/profile/`
   - **Permissions**: Authenticated
   - **Body (PUT)**:
     ```json
     {
         "first_name": "Updated",
         "last_name": "Name"
     }
     ```
   - **Response** (200):
     ```json
     {
         "username": "testuser",
         "email": "test@example.com",
         "first_name": "Updated",
         "last_name": "Name"
     }
     ```
   - **Postman**: Add `Authorization: Bearer <access_token>` to headers.

### Book Management
1. **List/Create Books**
   - **GET/POST** `/books/`
   - **Permissions**: GET (public), POST (authenticated)
   - **Body (POST)**:
     ```json
     {
         "title": "Sample Book",
         "authors": "Author Name",
         "genre": "Fiction",
         "publication_date": "2023-01-01",
         "description": "A sample book"
     }
     ```
   - **Response** (201):
     ```json
     {
         "id": 1,
         "title": "Sample Book",
         "authors": "Author Name",
         "genre": "Fiction",
         "publication_date": "2023-01-01",
         "description": "A sample book",
         "created_by": 1,
         "created_at": "2025-08-10T17:24:00Z",
         "updated_at": "2025-08-10T17:24:00Z"
     }
     ```
   - **Postman**: For POST, add `Authorization` header.

2. **Retrieve/Delete Book**
   - **GET/DELETE** `/books/<id>/`
   - **Permissions**: GET (public), DELETE (creator only)
   - **Response (DELETE)**: 204 or 403 (if not creator)
   - **Postman**: Add `Authorization` for DELETE.

### Reading Lists
1. **List/Create Reading Lists**
   - **GET/POST** `/reading-lists/`
   - **Permissions**: Authenticated
   - **Body (POST)**:
     ```json
     {
         "name": "My Favorites"
     }
     ```
   - **Response** (201):
     ```json
     {
         "id": 1,
         "user": 1,
         "name": "My Favorites",
         "created_at": "2025-08-10T17:24:00Z",
         "updated_at": "2025-08-10T17:24:00Z"
     }
     ```
   - **Postman**: Add `Authorization` header.

2. **Retrieve/Update/Delete Reading List**
   - **GET/PUT/DELETE** `/reading-lists/<id>/`
   - **Permissions**: Authenticated (owner only)
   - **Body (PUT)**:
     ```json
     {
         "name": "Updated Favorites"
     }
     ```

3. **Add/Remove Book from Reading List**
   - **POST** `/reading-lists/<id>/items/`, **DELETE** `/reading-lists/<id>/items/<book_id>/`
   - **Permissions**: Authenticated (owner only)
   - **Body (POST)**:
     ```json
     {
         "book_id": 1,
         "order": 1
     }
     ```
   - **Response** (201):
     ```json
     {
         "id": 1,
         "reading_list": 1,
         "book": {
             "id": 1,
             "title": "Sample Book",
         },
         "book_id": 1,
         "order": 1,
         "added_at": "2025-08-10T17:24:00Z"
     }
     ```
   - **Postman**: Add `Authorization` header.

## Postman Collection Example
Create a Postman collection with the following:
1. **Register**: POST `http://localhost:8000/api/users/register/`
   - Body: Raw JSON (see above).
2. **Login**: POST `http://localhost:8000/api/users/login/`
   - Save `access` token as an environment variable: `{{access_token}}`.
3. **Profile**: GET/PUT `http://localhost:8000/api/users/profile/`
   - Headers: `Authorization: Bearer {{access_token}}`
4. **Books**: GET/POST `http://localhost:8000/api/books/`
   - POST Headers: `Authorization: Bearer {{access_token}}`
5. **Reading Lists**: GET/POST `http://localhost:8000/api/reading-lists/`
   - Headers: `Authorization: Bearer {{access_token}}`
6. **Reading List Items**: POST/DELETE `http://localhost:8000/api/reading-lists/<id>/items/`
   - Headers: `Authorization: Bearer {{access_token}}`

## Error Handling
- **400 Bad Request**: Invalid input (e.g., mismatched passwords).
- **401 Unauthorized**: Missing/invalid JWT.
- **403 Forbidden**: Action not allowed (e.g., deleting another user's book).
- **404 Not Found**: Resource not found.
- Example error:
  ```json
  {"password": ["Passwords do not match."]}
  ```

## Notes
- Uses SQLite by default; configure PostgreSQL in `settings.py` for production.