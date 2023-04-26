# ToDo List App

This is a simple ToDo List App made with Flask, Marshmallow, and SQLAlchemy, with minimal frontend in basic HTML to interact with it.

## Functionalities

- Create users with Name and password and keep the session active.

- Create tasks linked to each user and display them in your home page.

- Mark tasks as done.

- Delete tasks.

## Installation

- Download the project, create a virtual environment, and install the requirements.

```bash
cd yourPath\ToDoListApp
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

# Starting the app

To create the database run the following commands:

```bash
python build_database.py
```

To start the app, run the following command:

```bash
python app.py
```

# Usage

Open your browser and go to http://127.0.0.1:8000/

You can register a new user, then you will be already logged in and can start trying the task functionalities.
