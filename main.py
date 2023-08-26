from flask import Flask, render_template, request, url_for, redirect, flash, abort, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import sqlite3
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap
from datetime import date
from forms import ChooseSystemForm, VentForm, HotWaterForm, SprinklerForm, ColdWaterForm, RadialFanForm, RoofVentForm
import os
import pandas as pd
from selection_functions import vent_support, attach_file
from functions import connection_to_postgress
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from dotenv import load_dotenv
from xlsxwriter.workbook import Workbook
from functools import wraps
import requests
from requests.auth import HTTPBasicAuth
import psycopg2


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
# 'BD_ROOT',
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
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
    name = db.Column(db.String(1000))
    company = db.Column(db.String(1000))
    spec = relationship("Specification", back_populates="author")
    is_authenticated = UserMixin

SYSTEMS = ['hot_water', 'cold_water', 'sprinkler', 'ventilation', 'radial_fans', 'roof_equipment']
SYSTEMS_TRANS = ['Трубопроводы с температурным расширением (отопление, ГВ)',
               'Трубопроводы без температурного расширения (ХВ, канализация)',
                'Спринклерное пожаротушение',
               'Вентиляция',
               "Оборудование на кровле",
                "Обвязка по кровле"]

# addr_from = current_user.email
addr_to = os.environ.get('CONSTRUCTOR_EMAIL')
password = os.environ.get('GMAIL_PASSWORD')
domain_name = os.environ.get('YOUR_DOMAIN_NAME')


# list_of_forms = [HotWaterForm(), ColdWaterForm(), SprinklerForm(), VentForm(), RadialFanForm(), RoofVentForm]
# SPECIFICATIONS = sqlite3.connect('instance/users.db')
# SPEC_DF = pd.read_sql_query("SELECT * FROM specifications", SPECIFICATIONS)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        # print(current_user)
        return redirect(url_for("choose_support_system"))
    else:
        return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Такой пользователь уже зарегистрирован.')
            # return redirect(url_for('login'))
        else:
            new_user = User(
                email=request.form.get('email'),
                name=request.form.get('name'),
                password=request.form.get('password'),
                company=request.form.get('company')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("choose_support_system"))

    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form['password']
        #ищем пользлвателя в базе данных по емэйлу
        user = User.query.filter_by(email=email).first()
        if user:
        #проверяет соответствие введенного пароля и пароля из базы данных
            if user.password == password:
                login_user(user)
                return redirect(url_for('choose_support_system'))
            else:
                flash('Неправильный пароль. Попробуйте еще раз.')
                return redirect(url_for('login'))
        else:
            flash("Такой email не существует. Попробуйте еще раз.")
            return redirect(url_for('login'))

    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["username"]
        email = request.form["email"]
        phone_number = request.form["phone"]
        message = request.form["message"]

        body = f"Имя: {name}.\n" \
               f"Email: {email}.\n" \
               f"Телефон: {phone_number}.\n" \
               f"Сообщение: {message}."
        msg = MIMEText(body)
        msg['Subject'] = 'Обратная связь'
        msg['From'] = f"postmaster@{domain_name}"
        msg['To'] = "shchekalina@gmail.com"

        # with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        #     connection.starttls()
        #     connection.login(user=addr_to, password=password)
        #     connection.sendmail(
        #         from_addr=email,
        #         to_addrs=addr_to,
        #         msg=msg.as_string())
        with smtplib.SMTP('smtp.mailgun.org', port=587) as connection:
            connection.starttls()
            connection.login(user=f'postmaster@{domain_name}',
                             password=os.environ.get('MAILGUN_PASSWORD'))
            connection.sendmail(
                msg['From'],
                msg['To'],
                msg.as_string())

        return render_template("contact.html", logged_in=current_user.is_authenticated, msg_sent=True)
    return render_template("contact.html", logged_in=current_user.is_authenticated, msg_sent=False)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/support_system', methods=["GET", "POST"])
def choose_support_system():
    form = ChooseSystemForm()
    if current_user.id == 1:
        admin = True
    else:
        admin = False
    if form.validate_on_submit():
        system = form.system.data[0]
        return redirect(url_for('choose_system_parameters', sys=system))

    return render_template("support_system.html", logged_in=current_user.is_authenticated, form=form, admin=admin)


@app.route("/support_system/<string:sys>", methods=["GET", "POST"])
def choose_system_parameters(sys):
    translated_system = SYSTEMS_TRANS[SYSTEMS.index(sys)]
    if sys == 'ventilation':
        param_form = VentForm()
    else:
        return 'Страница в разработке'
    # elif sys == 'sprinkler':
    #     param_form = SprinklerForm()
    # elif sys == 'cold_water':
    #     param_form = ColdWaterForm()
    # elif sys == 'hot_water':
    #     param_form = HotWaterForm()
    # elif sys == 'radial_fans':
    #     param_form = RadialFanForm()
    # else:
    #     param_form = RoofVentForm()

    if request.method == 'POST' and param_form.validate_on_submit():
        # name_of_file = f'{current_user.name}_{translated_system}.csv'
        parameters = param_form.data
        parameters.pop('csrf_token')
        parameters.pop('submit')
        choices = {
            'system': sys,
            'parameters': parameters
        }
        if sys == 'ventilation':
            vent = vent_support(choices)
            #Это условие может быть разным в зависимости от системы
            if not vent:
                flash(f'Недопустимые данные. Попробуйте еще раз.\nПри возникновении вопросов, обратитесь к специалисту компании HILTI.')
                return redirect(url_for('choose_system_parameters', sys=sys, logged_in=current_user.is_authenticated))
            # Это условие по идее не должно меняться
            else:
                support_name = vent[0]
                number_of_supports = vent[1]
                support_description = vent[2]
                name_of_columns = vent[3]
                print(f'{support_name}, {number_of_supports}, {support_description}')
                flash(f'Опора добавлена.')

            new_specification = Specification(
                system=translated_system,
                support_name=support_name,
                description=support_description,
                number_of_supports=number_of_supports,
                date=date.today().strftime("%d/%m/%Y"),
                author=current_user,
                status='В работе'
            )
            db.session.add(new_specification)
            db.session.commit()
        # try:
        #     with open(name_of_file, "r", encoding="utf-8-sig"):
        #         with open(name_of_file, "a", encoding="utf-8-sig") as csv_file:
        #             csv_file.write(f"{translated_system},{support_name},{number_of_supports},{support_description}\n")
        # except FileNotFoundError:
        #     with open(name_of_file, "a", encoding="utf-8-sig") as csv_file:
        #         csv_file.write(f"Система,Номер опоры,Количество опор,{name_of_columns}\n")
        #         csv_file.write(f"{translated_system},{support_name},{number_of_supports},{support_description}\n")
        return redirect(url_for('choose_system_parameters', logged_in=current_user.is_authenticated, form=param_form, sys=sys))

    return render_template(f'{sys}.html', logged_in=current_user.is_authenticated, form=param_form, system=sys)


@app.route("/backet", methods=["GET", "POST"])
def backet():
    # print(spec_df.groupby('system').value_counts())
    # print(spec_df[spec_df['system']=='Вентиляция'])
    not_empty_systems = []
    specifications = psycopg2.connect(dbname="support_user_database", host="dpg-civ600diuiedpv0lrnm0-a.oregon-postgres.render.com", user="support_user_database_user", password="6giJ3AG6hvMP8DoMyvx1LYooCJA35j2u", port="5432")
    spec_df = pd.read_sql_query("SELECT * FROM specifications", specifications)
    for sys in SYSTEMS_TRANS:
        system_df = spec_df.loc[(spec_df['system'] == sys) & (spec_df['status'] == 'В работе') & (spec_df['author_id'] == current_user.id)]
        # dbname = "support_user_database", host = "dpg-civ600diuiedpv0lrnm0-a.oregon-postgres.render.com", user = "support_user_database_user", password = "6giJ3AG6hvMP8DoMyvx1LYooCJA35j2u", port = "5432"
        # specifications = psycopg2.connect('os.environ.get("DATABASE_URL")/users.db')
        # print(system_df)
        if len(system_df) > 0:
            not_empty_systems.append(sys)
        else:
            continue
    # print(not_empty_systems)

    return render_template("backet.html", logged_in=current_user.is_authenticated, not_empty_systems=not_empty_systems,
                       length_of_systems_list=len(not_empty_systems))


@app.route("/backet/<string:sys>", methods=["GET", "POST"])
def backet_per_system(sys):
    print(current_user.id)
    # specifications = sqlite3.connect('instance/users.db')
    db_length = connection_to_postgress(sys, current_user)[0]
    system_df = connection_to_postgress(sys, current_user)[1]

    # print(system_df)
    # print(len(system_df))
    if db_length == 0:
        flash(f'Корзина пуста. Добавьте опоры.')
        return redirect(url_for('choose_support_system', logged_in=current_user.is_authenticated))
    # print(system_df.columns)
    # print(system_df.loc[3]['support_name'])

    # name_of_file = f'{current_user.name}_{translated_system}.csv'
    # try:
    #     with open(name_of_file, encoding="utf-8-sig") as csv_file:
    #         df = pd.read_csv(csv_file, delimiter=',')
    #         description_df = df.drop(columns=['Система','Номер опоры','Количество опор'], axis=1)
    #         description_df_columns_number = int(description_df.shape[1])
    #         if len(df) == 0:
    #             flash(f'Корзина пуста. Добавьте опоры.')
    #             return redirect(url_for('choose_support_system', logged_in=current_user.is_authenticated))
    # except FileNotFoundError:
    #     flash(f'Корзина пуста. Добавьте опоры.')
    #     return redirect(url_for('choose_system_parameters', sys=sys, logged_in=current_user.is_authenticated))
    return render_template("backet_per_system.html", logged_in=current_user.is_authenticated, supp_data=system_df,
                           len_of_df=db_length, current_system=sys)


@app.route('/backet/<string:sys>/delete', methods=["GET", "POST"])
def delete_support(sys):
    support_id = request.args.get('id')
    print(f'id = {support_id}, {type(support_id)}')
    support_to_delete = Specification.query.get(support_id)
    print(support_to_delete)
    db.session.delete(support_to_delete)
    db.session.commit()
    return redirect(url_for('backet_per_system', sys=sys, logged_in=current_user.is_authenticated))


@app.route('/backet/<string:sys>/send', methods=["GET", "POST"])
def send(sys):
    specifications = psycopg2.connect(dbname="support_user_database",
                                      host="dpg-civ600diuiedpv0lrnm0-a.oregon-postgres.render.com",
                                      user="support_user_database_user",
                                      password="6giJ3AG6hvMP8DoMyvx1LYooCJA35j2u",
                                      port="5432")
    spec_df = pd.read_sql_query("SELECT * FROM specifications", specifications)
    system_df = spec_df.loc[(spec_df['system'] == sys) & (spec_df['status'] == 'В работе') & (spec_df['author_id'] == current_user.id)].reset_index(drop=True)
    if request.method == 'POST':
        for n in range(0, len(system_df)):
            # print(system_df.loc[n]['id'])
            line_update = Specification.query.get(int(system_df.loc[n]['id']))
            line_update.object = request.form.get("objectname")
            line_update.object_address = request.form.get("objectaddress")
            db.session.commit()
            system_df.at[n, 'object'] = request.form.get("objectname")
            system_df.at[n, 'object_address'] = request.form.get("objectaddress")

        print(system_df)
        system_to_send_df = system_df.drop(columns=['author_id','id','status','send_date'], axis=1)
        filename = f'{request.form.get("objectname")}_{current_user.name}_{sys}_{date.today()}'
        system_to_send_df.to_excel(f'static/files/specifications/{filename}.xlsx')

        return send_from_directory('static', f"files/specifications/{filename}.xlsx")


@app.route('/backet/<string:sys>/delete_all>', methods=["GET", "POST"])
def delete_all(sys):
    specifications = psycopg2.connect(dbname="support_user_database",
                                      host="dpg-civ600diuiedpv0lrnm0-a.oregon-postgres.render.com",
                                      user="support_user_database_user",
                                      password="6giJ3AG6hvMP8DoMyvx1LYooCJA35j2u",
                                      port="5432")
    spec_df = pd.read_sql_query("SELECT * FROM specifications", specifications)
    system_df = spec_df.loc[(spec_df['system'] == sys) & (spec_df['status'] == 'В работе')& (spec_df['author_id'] == current_user.id)].reset_index(drop=True)
    for n in range(0, len(system_df)):
        line_to_update = Specification.query.get(int(system_df.loc[n]['id']))
        line_to_update.status = "Отправлено"
        line_to_update.send_date = date.today().strftime("%d/%m/%Y")
        db.session.commit()
    # os.remove(name_of_file)
    # os.remove(final_filename + '.xlsx')
    return redirect(url_for('choose_support_system', sys=sys, logged_in=current_user.is_authenticated))



#декоратор для доступа к странице только админа (id=1)
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
    return render_template("all_users.html", logged_in=current_user.is_authenticated, users=all_users)

@app.route('/delete_user')
@admin_only
def delete_user():
    user_id = request.args.get('id')
    user_to_delete = User.query.get(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('show_users'))

with app.app_context():
    db.create_all()
    all_users = db.session.query(User).all()

if __name__ == '__main__':
    app.run(debug=True)