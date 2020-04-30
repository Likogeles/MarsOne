from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user

from data import db_session, jobs, users, loginform, registerform


# email и пароль для входа:
# scott_chief@mars.org
# 123


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


def main():
    db_session.global_init("db/marsians.sqlite")
    session = db_session.create_session()

    job = jobs.Job()
    job.team_leader = 1
    job.job = "deployment of residential modules 1 and 2"
    job.work_size = 15
    job.collaborators = "2, 3"
    job.is_finished = False

    user1 = users.User()
    user1.name = "Ridley"
    user1.surname = "Scott"
    user1.age = 21
    user1.position = "captain"
    user1.speciality = "research engineer"
    user1.adress = "module_1"
    user1.email = "scott_chief@mars.org"

    session = db_session.create_session()
    session.add(job)
    session.add(user1)
    session.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerform.RegisterForm()
    db_session.global_init("db/marsians.sqlite")
    session = db_session.create_session()

    if form.validate_on_submit():
        if not form.age.data.isdigit():
            return render_template('register.html',
                                   agemassage="Неправильно введён возраст",
                                   form=form)
        if not form.password1.data == form.password2.data:
            return render_template('register.html',
                                   passwordmassage="Пароли не совпадают",
                                   form=form)
        user1 = users.User()
        user1.name = form.name.data
        user1.surname = form.surname.data
        user1.age = int(form.age.data)
        user1.position = form.position.data
        user1.speciality = form.speciality.data
        user1.address = form.address.data
        user1.email = form.email.data
        user1.hashed_password = form.password1.data

        session.add(user1)
        session.commit()

        return redirect("/login")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginform.LoginForm()
    db_session.global_init("db/marsians.sqlite")
    session = db_session.create_session()
    session.commit()

    print("validate: " + str(form.validate_on_submit()))
    if form.validate_on_submit():
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user:
            if user.hashed_password == form.password.data:
                login_user(user, remember=form.remember_me.data)
                return redirect("/works")
            return render_template('login.html',
                                   messagepass="Неправильный пароль",
                                   form=form)
        return render_template('login.html',
                               messageemail="Неправильный email",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
@app.route('/works')
def works():
    db_session.global_init("db/marsians.sqlite")
    session = db_session.create_session()
    jobes = session.query(jobs.Job)
    return render_template('jobs.html', jobs=jobes)


if __name__ == '__main__':
    # main()
    app.run(port=8080, host='127.0.0.1')
