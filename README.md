This project is a FastAPI-based secure API that uses JSON Web Tokens (JWT) for authentication. It includes registration, login, and profile management functionality with SQLite as the database.

## Features

- User registration with unique constraints on username, email, and phone number.
- Secure password hashing using `pbkdf2_sha256`.
- JWT-based login for secure access to protected routes.
- Cookie-based authentication for easy access control.
- Profile endpoint to view authenticated user details.

## Installation

### Prerequisites

- Python 3.7+
- `pip` (Python package manager)
- `virtualenv` (optional, recommended for isolated environments)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Mrterrestrial/FastAPI-JWTAuth
   cd
   ```

2. **Set Up a Virtual Environment (recommended):**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Create an .env File: In the project root directory, create a .env file with the following content:**

    ```bash
    touch .env
    echo "JWT_SECRET_KEY=your_jwt_secret_key" >> .env
    ```

4. **Run the Application:**

    ```bash
    python run.py
    ```

The app will be accessible at http://127.0.0.1:8000

## Project Structure

```bash
    ├── app/
    │   ├── models/
    │   │   └── user_model.py          # User model definition
    │   ├── routes/
    │   │   ├── index.py               # Root route
    │   │   ├── register.py            # Registration route
    │   │   ├── login.py               # Login route with JWT generation
    │   │   └── profile.py             # Profile route with JWT validation
    │   ├── utils/
    │   │   └── db.py                  # Database session utility
    │   └── config/
    │       └── database.py            # Database configuration
    │
    │── app.db                         # Database
    │
    └── run.py                         # Main application entry point
```

## Usage

### Register a User

##### Endpoint: POST /register

- Registers a new user in the system with unique constraints on username, phone number, and email.

Example:

```
curl -X POST "http://127.0.0.1:8000/register" \
-H "Content-Type: application/json" \
-d '{
  "First_name": "John",
  "Last_name": "Doe",
  "Phone_number": "1234567890",
  "Username": "johndoe",
  "Password": "securepassword",
  "Email": "johndoe@example.com"
}'

```

### Log In

##### Endpoint: POST /login

- Logs in an existing user and returns a JWT token set as a cookie.

Example:

```
curl -X POST "http://127.0.0.1:8000/login" \
-H "Content-Type: application/json" \
-d '{
  "Username": "johndoe",
  "Password": "securepassword"
}' \
-v

```

##### Access Profile

Endpoint: GET /me

-  Access the authenticated user's profile using the JWT token in cookies.

Example

```
curl -X GET "http://127.0.0.1:8000/me" \
-H "Cookie: token={your-token}"
```

## License

This project is licensed under the MIT License - see [MIT License](https://opensource.org/licenses/MIT) for details.

## Contributing

Feel free to fork the repository and submit pull requests. For any issues or feature requests, please open an issue on GitHub.