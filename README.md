## IT Services - Django Project
Project Overview
"IT Services" is a Django-based web application that allows users to register, log in, and manage IT-related services. The project includes user authentication, service management, and integration with the Razorpay payment gateway for service subscriptions. The key features include CRUD operations for services, user registration with OTP verification, and payment handling through Razorpay.

## Project Structure
IT-Services/
│
├── it_services/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
|   |__ urls.py
│
├── services/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── templates/
│       ├── index.html
│       ├── buy_service.html
│       ├── create_Service.html
│       ├── delete_Service.html
│       ├── list_Service.html
│       ├── log_in.html
│       ├── payment_Status.html
│       ├── register.html
│       ├── subscribe.html
│       └── update_Service.html
│       └── verify_otp.html
│   
│
├── manage.py
└── README.md

## Features
  User Registration with OTP Verification:
  Users can register with an email address.
  An OTP is sent to the user's email for verification.
  Users are redirected to an OTP confirmation page.
  
## User Authentication:
  Only logged-in users can access the home view and manage services.
  Users are redirected to the login page if not authenticated.
  
## Service Management:
  CRUD operations for services.
  Services have fields like name, price, tax, and active status.
  Only active services are displayed on the home page.
  
## Subscription and Payment Handling:
  Users can subscribe to services by providing an address and making payments via Razorpay.
  Subscription details and payment status are stored in the database.
  
Setup Instructions
## Prerequisites
Python 3.x
Django 4.x
Razorpay API credentials (provided in the project)

Step-by-Step Setup
Clone the repository:
git clone https://github.com/yourusername/IT-Services.git
cd IT-Services

Create a virtual environment and activate it:
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

Install required dependencies:
pip install -r requirements.txt
Set up environment variables: Create a .env file in the root directory and add the following:
SECRET_KEY=your_secret_key
DEBUG=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
RAZORPAY_API_KEY=rzp_test_e664V0FP0zQy7N
RAZORPAY_API_SECRET=QdnuRxUHrPGeiJc9lDTXYPO7

Apply migrations to set up the database:
python manage.py migrate

Create a superuser for accessing the admin panel:
python manage.py createsuperuser

Run the development server:
python manage.py runserver
Access the application: Open your web browser and go to http://127.0.0.1:8000/.

## Project Functionalities
1. Admin Panel Configuration
Access the admin panel at http://127.0.0.1:8000/admin/.
Log in using the superuser credentials created earlier.

2. User Registration and OTP Verification
Visit http://127.0.0.1:8000/register/ to create a new account.
After registration, an OTP is sent to the registered email for verification.

3. Service Management
Once logged in, the user can create, update, delete, and view services.
Services can be marked as active/inactive using a checkbox.

4. Subscription and Payment
Users can subscribe to active services by clicking the "Buy" button.
Payment is handled through Razorpay, and the status is stored in the "Subscription" model.

5. Payment Confirmation Pages
Upon successful payment, the user is redirected to a success page displaying the transaction details.
In case of payment failure, the user is redirected to a failure page.

## Usage
Admin Panel: Manage services, users, and subscriptions.
Home View: Logged-in users can view and subscribe to services.
Razorpay Integration: Secure payment handling for service subscriptions.
Technologies Used
Django 4.x: Web framework for building the application.
Razorpay API: Integrated for handling payments.
Bootstrap 3.4.1: For responsive design and styling.
Contributing
If you'd like to contribute to this project, please fork the repository and create a pull request with your changes.


