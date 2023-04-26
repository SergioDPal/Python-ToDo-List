from config import get_app_config
from flask import redirect, render_template, request, session, url_for
from models import User
from users import check_password_is_correct, create as create_user
from chores import _ChoresDBOperations
from datetime import datetime

app_config = get_app_config()
app = app_config.app


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = {"username": username, "password": password}
        if check_password_is_correct(user):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template("login.html", error="Invalid username or password")
    else:
        return render_template("login.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = {"username": username, "password": password}
        if create_user(user):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template("register.html", error="Username already exists")
    else:
        return render_template("register.html")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/tasks', methods=['POST'])
def new_task():
    if request.method == 'POST':
        date = str(datetime.strptime(request.form["due_date"], '%Y-%m-%d'))

        chore = {"title": request.form["title"], "description": request.form["description"],
                 "due_date": date}

        _ChoresDBOperations().create(chore)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/tasks/<int:task_id>', methods=['POST'])
def update_task(task_id):
    if request.method == 'POST':
        chore = {"completed": request.form["completed"]}
        _ChoresDBOperations().updateCompletedField(task_id, chore)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    if request.method == 'POST':
        _ChoresDBOperations().delete(task_id)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/')
def home():
    users = User.query.all()
    if not users:
        return render_template("register.html")
    
    if not session:
        return render_template("login.html")
    
    
    tasks = _ChoresDBOperations().read_all(User.query.filter_by(
        username=session['username']).first().id)
    return render_template("home.html", users=users, tasks=tasks)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
