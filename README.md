# Fashion Store Website&#x20;

## Project Overview

This is a Django-based e-commerce web application that integrates with the Unsplash API to fetch and display images dynamically. The project follows the standard Django structure and includes necessary configurations for API integration.

## Features

- Fetches high-quality images from Unsplash API
- Displays products in a user-friendly format
- Django-based backend with an SQLite database

## Installation

### Prerequisites

Ensure you have the following installed on your system:

- Python (>=3.8)
- Django (>=3.2)
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**:

   ```sh
   git clone <repository_url>
   cd project
   ```

2. **Create and activate a virtual environment**:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   - Create a `.env` file in the root directory.
   - Add the following lines, replacing `your_unsplash_access_key` with your actual API key:
     ```env
     UNSPLASH_ACCESS_KEY=your_unsplash_access_key
     ```

5. **Run database migrations**:

   ```sh
   python manage.py migrate
   ```

6. **Create a superuser**:

   ```sh
   python manage.py createsuperuser
   ```

   Follow the prompts to set up an admin account.

7. **Start the development server**:

   ```sh
   python manage.py runserver
   ```

## Project Structure

```
project/
│-- ecommerce/               # Main Django app
│   │-- __init__.py
│   │-- settings.py          # Project settings
│   │-- urls.py              # URL routing
│   │-- wsgi.py              # WSGI entry point
│   │-- asgi.py              # ASGI entry point
│-- store/                   # Store app for managing products
│   │-- __init__.py
│   │-- models.py            # Database models
│   │-- views.py             # Business logic
│   │-- urls.py              # Store-specific routing
│   │-- templates/           # Store-related HTML templates
│-- static/                  # Static files (CSS, JS, images)
│-- templates/               # Global HTML templates
│-- media/                   # Uploaded media files
│-- db.sqlite3               # SQLite database file
│-- manage.py                # Django management script
│-- requirements.txt         # Dependencies list
│-- .env                     # Environment variables
```

## Usage

- Open `http://127.0.0.1:8000/` in your browser.
- The homepage will display products fetched from Unsplash.

## API Configuration

The Unsplash API is accessed using an API key stored in the `.env` file. Ensure you have signed up at [Unsplash Developers](https://unsplash.com/developers) and obtained an access key.

## Contributing

Feel free to fork this repository and contribute by submitting a pull request.

## License

This project is licensed under the MIT License.

