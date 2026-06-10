# Civilregistration-project
Here is the complete English translation of your documentation:

# 📚 Civil Registry and Citizen Information Inquiry System with Django

A comprehensive civil registry management system built using the Django web framework. This project demonstrates the implementation of advanced models, an authentication system, quota management, a custom admin panel, and performance optimization for high data volumes.

## 🚀 Features

### User Management and Civil Registry
*   **Registration and Login:** Complete authentication system using Django's built-in `User` model and custom profiles.
*   **Validation:** Verification of phone number format (`+98...`) and National ID code.
*   **User Profile:** Storage of sensitive information including first name, last name, National ID, date of birth, and address.

### Quota Management System
*   **Dynamic Usage Limits:** Ability to set individual search quotas for each user.
*   **Time-Based Controls:** Consumption control within **daily** and **monthly** intervals.
*   **Admin Management:** Dedicated admin panel for administrators to change user consumption limits (global or specific).
*   **Limit Enforcement:** Automatic blocking of searches after the allowed quota is exhausted, with an appropriate notification message.

### Advanced and Optimized Search
*   **Unified Search:** Ability to search across all civil registry fields via a single input field.
*   **Performance Display:** Display of search duration (in seconds) and the number of results to the user.
*   **Logging:** Recording the history of all searches for reporting and token deduction.
*   **High Performance:** Query optimization and use of indexes for fast searching across more than 100,000 records.

### Admin Panel
*   **User Management:** View, edit, and manage civil registry user information.
*   **Consumption Management:** View daily and monthly consumption reports for each user and set new limits.
*   **Search Logs:** Access to search history and analysis of usage patterns.

## 🗄️ Database Models

### User Model (`User`) - Django
Django's default model for managing user accounts, usernames, and passwords.

### User Profile Model (`UserProfile`)

| Field | Description |
| :--- | :--- |
| `user` | One-to-one relationship with the User model |
| `national_code` | National ID (Unique) |
| `first_name` | First Name |
| `last_name` | Last Name |
| `phone_number` | Phone Number (Format: +98...) |
| `birth_date` | Date of Birth |
| `address` | Residential Address |
| `daily_limit` | Daily search limit (Default: 10) |
| `monthly_limit` | Monthly search limit (Default: 300) |

### Admin Consumption Limit Model (`AdminConsumptionLimit`)

| Field | Description |
| :--- | :--- |
| `user` | One-to-one relationship with the target user |
| `custom_daily_limit` | Custom daily limit (0 means using the default) |
| `custom_monthly_limit` | Custom monthly limit (0 means using the default) |

### Search Log Model (`SearchLog`)

| Field | Description |
| :--- | :--- |
| `user` | The user who performed the search |
| `query_text` | The searched text |
| `results_count` | Number of results found |
| `duration` | Search duration (seconds) |
| `timestamp` | Exact time the search was performed |

## 🖥️ Views (Class-Based Views)

### Registration (`RegisterView`)
*   Inherits from `CreateView`.
*   Handles the simultaneous creation of the `User` and `UserProfile` records.
*   Form validation (password match, phone number format).

### Login (`LoginView`)
*   Inherits from `TemplateView`.
*   Handles POST requests for authentication and session creation.

### User Dashboard (`UserDashboardView`)
*   Inherits from `LoginRequiredMixin` and `TemplateView`.
*   Displays current consumption status (daily/monthly).
*   Displays active limits (default or custom admin-defined).

### Search (`SearchView`)
*   Inherits from `LoginRequiredMixin` and `ListView`.
*   **Checking Limits:** Before searching, checks daily and monthly consumption quotas.
*   **Executing Search:** Uses `Q` objects for multi-condition searching across all fields.
*   **Logging:** Creates a record in `SearchLog` for each search.
*   **Duration Calculation:** Precisely measures query execution time to display to the user.

## 🎨 Templates

### `base.html`
The parent template including the header, navigation bar (Navbar), and base CSS styles.

### `register.html`
Registration form with civil registry information fields and password fields.

### `login.html`
Simple login form displaying error or success messages.

### `dashboard.html`
User control page including:
*   Identity information.
*   Progress bars for daily and monthly consumption.
*   Limit status (active/inactive).
*   Link to the search page.

### `search.html`
Search page including:
*   Text input field for search queries.
*   Display of success or error messages (e.g., quota reached).
*   Search results table (Name, National ID, Phone, Address).
*   Display of search duration and result count.

## 🛠️ Technologies Used
*   **Python:** Primary programming language.
*   **Django:** Powerful web framework.
*   **HTML/CSS:** Page structure and styling.
*   **SQLite/PostgreSQL:** Database (configurable).
*   **Django ORM:** Database management without direct SQL coding.
*   **Class-Based Views (CBV):** Modern and modular view architecture.
*   **Django Admin:** Internal management panel.

## 📂 Project Structure
```text
civil_registry/
│
├── civil_registry/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── users/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── tests.py
│   └── templates/
│       └── users/
│           ├── base.html
│           ├── register.html
│           ├── login.html
│           ├── dashboard.html
│           └── search.html
│
├── manage.py
├── populate_data.py  # Script for generating sample data
└── db.sqlite3
```

## ⚙️ Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/civil-registration-project.git
cd civil-registration-project
```

### 2. Create Virtual Environment and Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install django
```

### 3. Database Settings and Migrations
```bash
python manage.py makemigrations users
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Generate Sample Data (Optional but recommended for performance testing)
```bash
python populate_data.py
```

### 6. Run Development Server
```bash
python manage.py runserver
```
Open your browser and visit the following addresses:
*   **Home/Login:** `http://127.0.0.1:8000/`
*   **Admin Panel:** `http://127.0.0.1:8000/admin/`

## 🎯 Learning Objectives
This project was developed with the goal of practicing and mastering advanced topics such as:
*   **User Management:** Implementing custom authentication systems with `OneToOne` relations.
*   **Quota System:** Implementing business logic for time-based limits (daily/monthly).
*   **Database Optimization:** Using `bulk_create` for fast data loading and indexing for fast searches.
*   **Class-Based Views:** Using CBVs for cleaner and more extensible code.
*   **Data Validation:** Implementing validated forms and views.
*   **Logging:** Recording operation history for reporting and monitoring.

## 🔮 Future Improvements
*   **API Implementation:** Developing a REST API with `Django REST Framework` for mobile applications.
*   **Advanced Search (Fuzzy Search):** Adding fuzzy search capabilities to handle typographical errors.
*   **Excel Export:** Ability to download consumption reports and search results in Excel/PDF format.
*   **Testing:** Adding unit tests for views and models.
*   **Deployment:** Preparing the project for production deployment using Nginx and Gunicorn.

## 👨‍💻 Author
This project was designed and developed as an advanced Django training project to learn enterprise web development, scalable database management, and the implementation of security and monitoring systems.