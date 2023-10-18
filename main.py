from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    abort,
    send_from_directory,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import sqlite3
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    current_user,
    logout_user,
)
from flask_bootstrap import Bootstrap
from datetime import date
from forms import (
    ChooseSystemForm,
    VentForm,
    HotWaterForm,
    SprinklerForm,
    ColdWaterForm,
    RadialFanForm,
    RoofVentForm,
)
import os
import pandas as pd
from selection_functions import vent_support, sprinkler_support, hot_water_supports
from functions import connection_to_postgress
# from dotenv import load_dotenv
from functools import wraps
import requests
from requests.auth import HTTPBasicAuth
import psycopg2


# dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
# load_dotenv(dotenv_path)

app = Flask(__name__)
Bootstrap(app)

app.config.from_pyfile('settings.py')
# app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app, engine_options={"pool_pre_ping": True})
login_manager = LoginManager()
login_manager.init_app(app)


##CREATE TABLE IN DB
class Specification(db.Model):
    __tablename__ = "specifications"
    id = db.Column(db.Integer, primary_key=True)
    system = db.Column(db.String(250), nullable=False)
    support_name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    number_of_supports = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Create reference to the User object, the "posts" refers to the posts property in the User class.
    author = relationship("User", back_populates="spec")
    status = db.Column(db.String(250), nullable=False)
    object = db.Column(db.String(250))
    object_address = db.Column(db.String(250))
    send_date = db.Column(db.String(250))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    company = db.Column(db.String(1000))
    spec = relationship("Specification", back_populates="author")
    is_authenticated = UserMixin


class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100))
    message = db.Column(db.String(1500), nullable=False)
    date = db.Column(db.String(250), nullable=False)


SYSTEMS = [
    "hot_water",
    "cold_water",
    "fixed_supports",
    "sprinkler",
    "ventilation",
    "radial_fans",
    "roof_equipment",
]
SYSTEMS_TRANS = [
    "Трубопроводы с температурным расширением (отопление, ГВ)",
    "Трубопроводы без температурного расширения (ХВ, канализация)",
    "Фиксирующие опоры",
    "Спринклерное пожаротушение",
    "Вентиляция",
    "Оборудование на кровле",
    "Обвязка по кровле",
]


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    if current_user.is_authenticated:
        # print(current_user)
        return redirect(url_for("choose_support_system"))
    else:
        return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Такой пользователь уже зарегистрирован.")
            # return redirect(url_for('login'))
        else:
            new_user = User(
                email=request.form.get("email"),
                name=request.form.get("name"),
                password=request.form.get("password"),
                company=request.form.get("company"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("choose_support_system"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form["password"]
        # ищем пользлвателя в базе данных по емэйлу
        user = User.query.filter_by(email=email).first()
        if user:
            # проверяет соответствие введенного пароля и пароля из базы данных
            if user.password == password:
                login_user(user)
                return redirect(url_for("choose_support_system"))
            else:
                flash("Неправильный пароль. Попробуйте еще раз.")
                return redirect(url_for("login"))
        else:
            flash("Такой email не существует. Попробуйте еще раз.")
            return redirect(url_for("login"))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        input_name = request.form["username"]
        input_email = request.form["email"]
        input_phone_number = request.form["phone"]
        input_message = request.form["message"]

        new_comment = Comments(
            name=input_name,
            email=input_email,
            phone=input_phone_number,
            message=input_message,
            date=date.today().strftime("%d/%m/%Y"),
        )
        db.session.add(new_comment)
        db.session.commit()

        return render_template(
            "contact.html", msg_sent=True, logged_in=current_user.is_authenticated
        )
    return render_template(
        "contact.html", msg_sent=False, logged_in=current_user.is_authenticated
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/support_system", methods=["GET", "POST"])
def choose_support_system():
    form = ChooseSystemForm()
    if current_user.id == 1:
        admin = True
    else:
        admin = False
    if form.validate_on_submit():
        system = form.system.data[0]
        return redirect(url_for("choose_system_parameters", sys=system))

    return render_template(
        "support_system.html",
        logged_in=current_user.is_authenticated,
        form=form,
        admin=admin,
    )


@app.route("/support_system/<string:sys>", methods=["GET", "POST"])
def choose_system_parameters(sys):
    translated_system = SYSTEMS_TRANS[SYSTEMS.index(sys)]
    if sys == "ventilation":
        param_form = VentForm()
    elif sys == "sprinkler":
        param_form = SprinklerForm()
    # elif sys == 'radial_fans':
    #     param_form = RadialFanForm()
    elif sys == "hot_water":
        param_form = HotWaterForm()
    else:
        return "Страница в разработке"
    # elif sys == 'cold_water':
    #     param_form = ColdWaterForm()
    # elif sys == 'radial_fans':
    #     param_form = RadialFanForm()
    # else:
    #     param_form = RoofVentForm()

    if request.method == "POST" and param_form.validate_on_submit():
        # name_of_file = f'{current_user.name}_{translated_system}.csv'
        parameters = param_form.data
        parameters.pop("csrf_token")
        parameters.pop("submit")
        choices = {"system": sys, "parameters": parameters}
        if sys == "ventilation":
            current_system = vent_support(choices)

        elif sys == "sprinkler":
            current_system = sprinkler_support(choices)

        elif sys == "hot_water":
            current_system = hot_water_supports(choices)

        # print(f'это {current_system}')
        # Это условие может быть разным в зависимости от системы
        if not current_system:
            flash(
                f"Недопустимые данные. Попробуйте еще раз.\nПри возникновении вопросов, обратитесь к специалисту компании HILTI."
            )
            return redirect(
                url_for(
                    "choose_system_parameters",
                    sys=sys,
                    logged_in=current_user.is_authenticated,
                )
            )
        # Это условие по идее не должно меняться
        else:
            support_name = current_system[0]
            number_of_supports = current_system[1]
            support_description = current_system[2]
            # print(f'{support_name}, {number_of_supports}, {suppo
            # rt_description}')
            flash(f"Опора добавлена.")

        new_specification = Specification(
            system=translated_system,
            support_name=support_name,
            description=support_description,
            number_of_supports=number_of_supports,
            date=date.today().strftime("%d/%m/%Y"),
            author=current_user,
            status="В работе",
        )
        db.session.add(new_specification)
        db.session.commit()

        return redirect(
            url_for(
                "choose_system_parameters",
                logged_in=current_user.is_authenticated,
                form=param_form,
                sys=sys,
            )
        )

    return render_template(
        f"{sys}.html",
        logged_in=current_user.is_authenticated,
        form=param_form,
        system=sys,
    )


@app.route("/backet", methods=["GET", "POST"])
def backet():
    not_empty_systems = []
    specifications = psycopg2.connect(
        dbname="support_user_database",
        host=os.environ.get("DB_HOST"),
        user="support_user_database_user",
        password=os.environ.get("DB_PASSWORD"),
        port="5432",
    )
    spec_df = pd.read_sql_query("SELECT * FROM specifications", specifications)
    for sys in SYSTEMS_TRANS:
        system_df = spec_df.loc[
            (spec_df["system"] == sys)
            & (spec_df["status"] == "В работе")
            & (spec_df["author_id"] == current_user.id)
        ]
        if len(system_df) > 0:
            not_empty_systems.append(sys)
        else:
            continue

    if len(not_empty_systems) == 0:
        flash(f"Корзина пуста. Добавьте опоры.")
        return redirect(
            url_for("choose_support_system", logged_in=current_user.is_authenticated)
        )
    # print(not_empty_systems)

    return render_template(
        "backet.html",
        logged_in=current_user.is_authenticated,
        not_empty_systems=not_empty_systems,
        length_of_systems_list=len(not_empty_systems),
    )


@app.route("/backet/<string:sys>", methods=["GET", "POST"])
def backet_per_system(sys):
    # print(current_user.id)
    system_df = connection_to_postgress(sys, current_user)
    return render_template(
        "backet_per_system.html",
        logged_in=current_user.is_authenticated,
        supp_data=system_df,
        len_of_df=len(system_df),
        current_system=sys,
    )


@app.route("/backet/<string:sys>/delete", methods=["GET", "POST"])
def delete_support(sys):
    support_id = request.args.get("id")
    # print(f'id = {support_id}, {type(support_id)}')
    support_to_delete = Specification.query.get(support_id)
    # print(support_to_delete)
    db.session.delete(support_to_delete)
    db.session.commit()
    return redirect(
        url_for("backet_per_system", sys=sys, logged_in=current_user.is_authenticated)
    )


@app.route("/backet/<string:sys>/send", methods=["GET", "POST"])
def send(sys):
    system_df = connection_to_postgress(sys, current_user)
    if request.method == "POST":
        for n in range(0, len(system_df)):
            # print(system_df.loc[n]['id'])
            line_update = Specification.query.get(int(system_df.loc[n]["id"]))
            line_update.object = request.form.get("objectname")
            line_update.object_address = request.form.get("objectaddress")
            db.session.commit()
            system_df.at[n, "object"] = request.form.get("objectname")
            system_df.at[n, "object_address"] = request.form.get("objectaddress")

        # print(system_df)
        system_to_send_df = system_df.drop(
            columns=["author_id", "id", "status", "send_date"], axis=1
        )
        system_to_send_df.columns = [
            "Система",
            "Наименование опоры",
            "Описание",
            "Количество опор",
            "Дата",
            "Объект",
            "Адрес объекта",
        ]
        filename = (
            f'{request.form.get("objectname")}_{current_user.name}_{sys}_{date.today()}'
        )
        system_to_send_df.to_excel(f"static/files/specifications/{filename}.xlsx")

        return send_from_directory("static", f"files/specifications/{filename}.xlsx")


@app.route("/backet/<string:sys>/delete_all>", methods=["GET", "POST"])
def delete_all(sys):
    system_df = connection_to_postgress(sys, current_user)
    for n in range(0, len(system_df)):
        line_to_update = Specification.query.get(int(system_df.loc[n]["id"]))
        line_to_update.status = "Отправлено"
        line_to_update.send_date = date.today().strftime("%d/%m/%Y")
        db.session.commit()
    # os.remove(name_of_file)
    # os.remove(final_filename + '.xlsx')
    return redirect(
        url_for(
            "choose_support_system", sys=sys, logged_in=current_user.is_authenticated
        )
    )


# декоратор для доступа к странице только админа (id=1)
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function


@app.route("/all_users")
@admin_only
def show_users():
    with app.app_context():
        all_users = db.session.query(User).all()
    return render_template(
        "all_users.html", logged_in=current_user.is_authenticated, users=all_users
    )


@app.route("/user_specifications")
@admin_only
def specification_per_user():
    user_id = request.args.get("id")
    needed_user = User.query.get(user_id)
    specifications = psycopg2.connect(
        dbname="support_user_database",
        host=os.environ.get("DB_HOST"),
        user="support_user_database_user",
        password=os.environ.get("DB_PASSWORD"),
        port="5432",
    )
    spec_df = pd.read_sql_query("SELECT * FROM specifications", specifications)
    all_user_spec_df = spec_df.loc[
        (spec_df["author_id"] == needed_user.id)
    ].reset_index(drop=True)
    # print(all_user_spec_df)
    return render_template(
        "user_specifications.html",
        logged_in=current_user.is_authenticated,
        user=needed_user,
        specifications=all_user_spec_df,
        len_of_df=len(all_user_spec_df),
        admin=True,
    )


with app.app_context():
    db.create_all()
    all_users = db.session.query(User).all()

if __name__ == "__main__":
    app.run()
