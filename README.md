# Fitness Center Membership Management Using FastApi
  Fitness Center Membership Management web application using FastApi 
  
# Features Added 

* User Authentication with JWT
* Implemented protected routes and role-based access control(Admin/User)

Admin Endpoints (To make an admin, go to the database and change 0 to 1)

1) Add a member
2) Update member details
3) Remove a member
4) View all members
5) View membership records

User Endpoints

1) View membership status
2) Renew membership
3) View payment & renewal history

Swagger : ``` http://127.0.0.1:8000/docs ```
 
# Folder Structure
```
└── 📁Fitness_center
    └── 📁app
        └── __init__.py
        └── 📁api
            └── __init__.py
            └── deps.py
            └── 📁v1
                └── __init__.py
                └── admin.py
                └── auth.py
                └── members.py
                └── router.py
        └── config.py
        └── 📁core
            └── __init__.py
            └── config.py
            └── security.py
        └── database.py
        └── init_db.py
        └── main.py
        └── 📁models
            └── __init__.py
            └── member.py
            └── user.py
        └── 📁schema
            └── __init__.py
            └── member.py
            └── user.py
        └── 📁tests
            └── __init__.py
            └── conftest.py
            └── test_auth.py
            └── test_member.py
            └── test_membership.py
    └── .env
    └── .gitignore
    └── README.md
    └── requirement.txt
    └── test_fitness_center.db
```


#  To Setup

1. To clone the repository:

```bash
https://github.com/rajatk3566/Fitness_Center_fastapi.git
```

2. To create a virtual environment and activate:

```bash
python -m venv env
source .env/bin/activate
```

3. To Install dependencies:

```bash
pip install -r requirements.txt
```


6. To run the application:

```bash
uvicorn app.main:app -reload
```


# Test Suite for Fitness Center Membership Management (FastAPI)

## Overview
This test suite ensures the correctness of the Fitness Center Membership Management system built with FastAPI. It covers authentication, database interactions, and API responses.

# To Setup 

1) Install dependencies
 ```bash
pip install -r requirements.txt
```
2) To run all Tests

```bash
pytest
```




