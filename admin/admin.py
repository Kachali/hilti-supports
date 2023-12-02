from flask import (
    abort,
    request,
    render_template,
    Blueprint,
    url_for,
    redirect,
    flash,
    session
)
from flask_login import (
    current_user,
)
import psycopg2
import os
import pandas as pd
from extensions import db
from models import User
admin = Blueprint('admin_page', __name__, template_folder='templates')
#
#

def login_admin():
    session['admin_logged'] = 1

def isLogged():
    return True if session.get('admin_logged') else False

def logout_admin():
    session.pop('admin_logged', None)

@admin.route("/")
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    return render_template('admin/index.html', title='Админ-панель', logged_in=isLogged)

@admin.route("/login", methods=["GET", "POST"])
def login():
    if isLogged():
        return redirect(url_for('.index'))

    if request.method == "POST":
        if request.form.get("user") == 'admin' and request.form["password"] == '12345':
            # проверяет соответствие введенного пароля и пароля из базы данных
            login_admin()
            #точка значит, что страница из этого каталога грузится, а не из главного
            return redirect(url_for(".index"))
        else:
            flash("Неверная пара логин/пароль.", "error")
            return redirect(url_for(".login"))

    return render_template("admin/login.html", title='Админ-панель', logged_in=isLogged)


@admin.route("/logout", methods=["GET", "POST"])
def logout():
    if not isLogged():
        return redirect(url_for(".login"))

    logout_admin()
    return redirect(url_for('.login'))

@admin.route("/users")
def show_users():
    if isLogged():
        all_users = db.session.query(User).all()
        return render_template(
            "admin/users.html", logged_in=isLogged, users=all_users
        )
    else:
        return redirect(url_for(".login"))
#
#
@admin.route("/user_specifications")
def specification_per_user():
    if isLogged():
        user_id = request.args.get("id")
        needed_user = User.query.get(user_id)
        specifications = psycopg2.connect(
            dbname=os.environ.get("DB_NAME"),
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port="5432",
        )
        spec_df = pd.read_sql_query("SELECT * FROM specifications", specifications)
        all_user_spec_df = spec_df.loc[
            (spec_df["author_id"] == needed_user.id)
        ].reset_index(drop=True)
        # print(all_user_spec_df)
        return render_template(
            "admin/user_specifications.html",
            logged_in=isLogged,
            user=needed_user,
            specifications=all_user_spec_df,
            len_of_df=len(all_user_spec_df),
        )
    else:
        return redirect(url_for(".login"))