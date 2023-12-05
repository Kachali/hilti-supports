from flask import (
    request,
    render_template,
    Blueprint,
    url_for,
    redirect,
    flash,
    session,
    send_from_directory,
)
import psycopg2
import os
import pandas as pd
from datetime import date
from extensions import db
from models import User
admin = Blueprint('admin_page', __name__, template_folder='templates')


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
    return render_template('admin/index.html', title='Админ-панель', logged_in=isLogged())

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

    return render_template("admin/login.html", title='Админ-панель', logged_in=isLogged())


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
            "admin/users.html", logged_in=isLogged(), users=all_users
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
        all_user_spec_df['date'] = pd.to_datetime(all_user_spec_df['date'], dayfirst=True).dt.date
        new_user_spec_df = all_user_spec_df.sort_values(by=['date'], ascending=[False])
        session['data'] = new_user_spec_df.to_json()
        return render_template(
            "admin/user_specifications.html",
            logged_in=isLogged(),
            user=needed_user,
            specifications=new_user_spec_df,
            len_of_df=len(new_user_spec_df),
        )
    else:
        return redirect(url_for(".login"))

@admin.route("/user_specifications/download", methods=["GET", "POST"])
def download_user_spec():
    if isLogged():
        df = session.get('data')
        df = pd.read_json(df)
        user_name = request.args.get("user_name", None)
        user_company = request.args.get("user_company", None)
        user_email = request.args.get("user_email", None)
        if request.method == "POST":
            filename = (f'Спецификации пользователя {user_name}, компания {user_company}, email {user_email}, {date.today()}')
            df.columns = [
                "ID опоры в базе данных",
                "Система",
                "Наименование опоры",
                "Описание",
                "Количество опор",
                "Дата",
                "ID Автора",
                "Статус",
                "Объект",
                "Адрес объекта",
                "Дата отправки"
            ]
            df.to_excel(f"admin/static/files/specifications/{filename}.xlsx", index=False)
            return send_from_directory("admin/static", f"files/specifications/{filename}.xlsx")
    else:
        return redirect(url_for(".login"))