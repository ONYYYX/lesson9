from flask import Flask, render_template, redirect, request, abort, jsonify
from db import db_session
from data.Jobs import Jobs
from data.User import User
from data.Category import Category
from data.Department import Department
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.job import JobForm
from forms.department import DepartmentForm
import jobs_api
from flask import make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_skey_lol_lmao'
db_session.global_init('db/blogs.sqlite')
app.register_blueprint(jobs_api.blueprint)

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
@app.route('/jobs')
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs)
    return render_template('jobs.html', jobs=jobs)


@app.route('/jobs/create',  methods=['GET', 'POST'])
@login_required
def jobs_create():
    form = JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs()
        job.leader_id = form.leader_id.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        for i in map(int, form.category.data.split(',')):
            c = session.query(Category).filter(Category.id == i).first()
            if not c:
                c = Category(id=i, name=f'{i}')
            job.categories.append(c)
        job.is_finished = form.is_finished.data
        user = session.query(User).filter(User.id == job.leader_id).first()
        if user:
            user.jobs.append(job)
            session.merge(current_user)
            session.commit()
            return redirect('/')
    return render_template('jobs_add.html', title='Добавление работы', form=form)


@app.route('/jobs/edit/<int:job_id>', methods=['GET', 'POST'])
@login_required
def jobs_edit(job_id):
    form = JobForm()
    if request.method == "GET":
        session = db_session.create_session()
        if current_user.id == 1:
            job = session.query(Jobs).filter(Jobs.id == job_id).first()
        else:
            job = session.query(Jobs).filter(Jobs.id == job_id, Jobs.leader == current_user).first()
        if job:
            form.job.data = job.job
            form.leader_id.data = job.leader_id
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.category.data = ', '.join(map(lambda x: x.name, job.categories))
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        if current_user.id == 1:
            job = session.query(Jobs).filter(Jobs.id == job_id).first()
        else:
            job = session.query(Jobs).filter(Jobs.id == job_id, Jobs.leader == current_user).first()
        if job:
            job.leader_id = form.leader_id.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            for i in map(int, form.category.data.split(',')):
                c = session.query(Category).filter(Category.id == i).first()
                if not c:
                    c = Category(id=i, name=f'{i}')
                job.categories.append(c)
            job.is_finished = form.is_finished.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs_add.html', title='Редактирование работы', form=form)


@app.route('/jobs/delete/<int:job_id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(job_id):
    session = db_session.create_session()
    if current_user.id == 1:
        job = session.query(Jobs).filter(Jobs.id == job_id).first()
    else:
        job = session.query(Jobs).filter(Jobs.id == job_id, Jobs.leader == current_user).first()
    if job:
        session.delete(job)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments')
def departments_list():
    session = db_session.create_session()
    departments = session.query(Department)
    return render_template('departments.html', departments=departments)


@app.route('/departments/create',  methods=['GET', 'POST'])
@login_required
def departments_create():
    form = DepartmentForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        department = Department()
        department.title = form.title.data
        department.chief_id = form.chief_id.data
        department.email = form.email.data
        department.members = form.members.data
        user = session.query(User).filter(User.id == department.chief_id).first()
        if user:
            user.departments.append(department)
            session.merge(current_user)
            session.commit()
            return redirect('/departments')
    return render_template('departments_add.html', title='Добавление департамента', form=form)


@app.route('/departments/edit/<int:department_id>', methods=['GET', 'POST'])
@login_required
def departments_edit(department_id):
    form = DepartmentForm()
    if request.method == "GET":
        session = db_session.create_session()
        if current_user.id == 1:
            department = session.query(Department).filter(Department.id == department_id).first()
        else:
            department = session.query(Department).filter(
                Department.id == department_id, Department.chief == current_user
            ).first()
        if department:
            form.title.data = department.title
            form.chief_id.data = department.chief_id
            form.email.data = department.email
            form.members.data = department.members
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        if current_user.id == 1:
            department = session.query(Department).filter(Department.id == department_id).first()
        else:
            department = session.query(Department).filter(
                Department.id == department_id, Department.chief == current_user
            ).first()
        if department:
            department.title = form.title.data
            department.chief_id = form.chief_id.data
            department.email = form.email.data
            department.members = form.members.data
            session.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('departments_add.html', title='Редактирование департамента', form=form)


@app.route('/departments/delete/<int:department_id>', methods=['GET', 'POST'])
@login_required
def departments_delete(department_id):
    session = db_session.create_session()
    if current_user.id == 1:
        department = session.query(Department).filter(Department.id == department_id).first()
    else:
        department = session.query(Department).filter(
            Department.id == department_id, Department.chief == current_user
        ).first()
    if department:
        session.delete(department)
        session.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message='Неправильный логин или пароль',
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    app.run()


if __name__ == '__main__':
    main()
