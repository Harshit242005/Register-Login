# Django Authentication App

## Overview

This Django application provides a basic authentication system, including user registration, login, OTP login, a home page accessible to logged-in users, and logout functionality.

### Features

- **User Registration**: Allows new users to register by providing their username, email, and password.
- **User Login**: Allows registered users to log in using their credentials.
- **OTP Login**: Provides a secure login option where users can log in via a One-Time Password (OTP) sent to their email.
- **Home Page**: A protected page that is only accessible to authenticated users, displaying a welcome message.
- **Logout**: Allows users to log out of the application.

## Getting Started

Follow these steps to get the application running on your local machine.

### Prerequisites

Ensure you have Python and WSL installed on your system. This app was developed using Python 3.10.

### WSL Installation and Setup

To install and set up WSL on a Windows 10 or later system, follow these steps:

1. **Enable WSL**:
   - Open PowerShell as Administrator and run:
     ```
     dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
     ```
2. **Enable Virtual Machine Feature**:
   - In the same PowerShell window, run:
     ```
     dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
     ```
3. **Download Linux Kernel Update Package**:
   - Download and install the latest WSL Linux kernel update package for your machine from the official Microsoft website.

4. **Set WSL 2 as Default**:
   - Open PowerShell as Administrator and run:
     ```
     wsl --set-default-version 2
     ```
5. **Install Your Preferred Linux Distribution**:
   - Open the Microsoft Store and select your preferred Linux distribution (e.g., Ubuntu).
   - Click "Get" to install it.

6. **Set Up a New User Account and Password**:
   - Once installed, launch the Linux distribution and set up a new user account and password when prompted.

7. **Update and Upgrade Your Linux Distribution** (Optional but recommended):
   - Update your package lists and upgrade the packages:
     ```
     sudo apt update && sudo apt upgrade
     ```

### Installation

1. **Create a Virtual Environment**:
It's recommended to create a virtual environment to isolate the project dependencies.
```
python -m venv venv
```


2. **Activate the Virtual Environment**:

- On Windows:
  ```
  .\venv\Scripts\activate
  ```

- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

3. **Install Dependencies**:
Install the required dependencies using `pip`.
```
pip install -r requirements.txt
```

4. **Install and Start Redis**:

This step is only necessary if you are using features in your application that require Redis.

- **Install Redis**:
  - **On macOS** (using Homebrew):
  ```
  brew install redis
  ```


  - **On Linux**:
  ```
  sudo apt-get install redis-server
  ```


- **Start the Redis server**:
  Run the Redis server using the following command:
  ```
  redis-server
  ```
  OR
  ```
  brew services start redis
  ```

- **Check Redis Started or not**:
  ```
  redis-cli ping
  ```

5. **PostgreSQL Installation and Configuration**:

  This guide provides steps for installing and configuring PostgreSQL for your Django application.

- **1. Install PostgreSQL**

  - On macOS:
    - Update Homebrew:
    ```
    brew update
    ```
    - Install PostgreSQL:
    ```
    brew install postgresql
    ```
    - Start PostgreSQL service:
    ```
    brew services start postgresql
    ```

  - On Ubuntu:

    - Update package lists:
    ```
    sudo apt update
    ```
    - Install PostgreSQL and its contrib package:
    ```
    sudo apt install postgresql postgresql-contrib
    ```

- **2. Create a New PostgreSQL Database and User**:
  - Access the PostgreSQL Terminal:

    - On Linux:
    ```
    sudo -u postgres psql
    ```
    
    - On macOS:
    ```
    psql postgres
    ```

- **3. Create a New Database**:

  - Run the SQL command:
  ```
  CREATE DATABASE mydatabase;
  ```

- **4. Create a New User**:

  - Run the SQL command:
  ```
  CREATE USER myuser WITH PASSWORD 'mypassword';
  ```

- **5. Set Default Encoding, Transaction Isolation, and Time Zone**:

  - Run the SQL commands:
  ```
  ALTER ROLE myuser SET client_encoding TO 'utf8';
  ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
  ALTER ROLE myuser SET timezone TO 'UTC';
  ```

- **6. Grant Privileges**:

  - Run the SQL command:
  ```
  GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
  ```

- **7.Exit PostgreSQL Terminal**:

  - Type and execute:
  ```
  \q
  ```


5. **Database Migrations**:
Set up the database by running migrations.
```
python manage.py makemigrations authentication
python manage.py makemigrations
python manage.py migrate
```


6. **Start the Development Server**:
Run the Django development server.
```
python manage.py runserver
```


7. **Access the Application**:
The application will be available at `http://127.0.0.1:8000/`.

### Usage

- Access the registration page at `http://127.0.0.1:8000/api/register/step1` to create a new user.
- Log in through `http://127.0.0.1:8000/api/login/`.
- Once logged in, you will be redirected to the home page.
- Use the logout button on the home page to log out of the application.