# Fitness Center Membership Management Using FastApi
  Fitness Center Membership Management web application using FastApi 
# Features Added 

Admin Endpoints (is_admin=True)

1) Add a member
2) Update member details
3) Remove a member
4) View all members
5) View membership records

User Endpoints

1) View membership status
2) Renew membership
3) View payment & renewal history

# Folder Structure
```
└── 📁Fitness_center
    └── 📁app
        └── 📁api
            └── __init__.py
            └── deps.py
            └── 📁v1
                └── __init__.py
                └── admin.py
                └── auth.py
                └── members.py
                └── router.py
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
    └── .gitignore
    └── README.md
    └── requirement.txt
```


# Setup

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

