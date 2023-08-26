import pandas as pd
import math
from email import encoders
from email.mime.base import MIMEBase
import mimetypes
import os
from requests.auth import HTTPBasicAuth
import sqlite3
from flask import request
import requests

def vent_support(support):
    base_material = support['parameters']['base_material']
    direction_type = support['parameters']['direction_type']
    duct_type = support['parameters']['duct_type']
    diameter = int(support['parameters']['diameter'])
    length = int(support['parameters']['length'])
    if diameter < 400 and direction_type == 'Горизонтальная/потолок' or direction_type == 'Горизонтальная/стена' or direction_type == 'Горизонтальная/пол':
        num_of_supports = math.ceil(length/4)
    else:
        num_of_supports = math.ceil(length / 3)

    # print(base_material, direction_type, duct_type, diameter, num_of_supports)
    with open('static/files/Вентиляция опоры csv2.csv', 'r', encoding='Windows-1251') as file:
        data = pd.read_csv(file, delimiter=';')
        # print(data.columns, data.shape)
        # print(data.head)
        if duct_type == 'Прямоугольный' and diameter % 200 != 0:
            new_diameter = (diameter - diameter % 200) + 200
            # print(f'Введенный диаметр {diameter}, округленный диаметр {new_diameter}')
            support_num = data.loc[(data['крепление_к'] == base_material) & (data['разводка'] == direction_type) & (
                        data['тип_воздуховода'] == duct_type) & (data['диаметр/ширина'] == new_diameter)]

        else:
            support_num = data.loc[(data['крепление_к'] == base_material) & (data['разводка'] == direction_type) & (data['тип_воздуховода'] == duct_type) & (data['диаметр/ширина'] == diameter)]

        try:
            final_number = support_num['номер_опоры'].values[0]
            # print(final_number)
            if direction_type == 'Горизонтальная/стена' or direction_type == 'Вертикальная/стена':
                space = int(support_num.iloc[0]['расстояние_от_стены_до_оси_воздуховода'])
                description = f'{base_material},{direction_type},{duct_type}, {diameter}мм, {length}м, максимальное расстояние от стены до оси воздуховода {space}мм'
            else:
                description = f'{base_material},{direction_type},{duct_type}, {diameter}мм, {length}м, по всем вопросам обращаться к специалисту компании HILTI'
            name_of_columns = f'Базовый материал,Тип разводки,Тип воздуховода,Диаметр/ширина,Длина,Примечание'
            return [final_number,num_of_supports,description,name_of_columns]

        except IndexError:
            return False


def attach_file(msg, filepath):  # Функция по добавлению конкретного файла к сообщению
    filename = os.path.basename(filepath)  # Получаем только имя файла
    ctype, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
    if ctype is None or encoding is not None:  # Если тип файла не определяется
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    with open(filepath, 'rb') as fp:
        file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
        file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
        fp.close()
        encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
    file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
    msg.attach(file)


def sheety_send(sys):
    specifications = sqlite3.connect('instance/users.db')
    spec_df = pd.read_sql_query("SELECT * FROM specifications", specifications)
    system_df = spec_df.loc[(spec_df['system'] == sys) & (spec_df['status'] == 'В работе')].reset_index(drop=True)
    sheety_endpoint = os.environ.get('SHEETY_ENDPOINT')
    sheety_user = os.environ.get('SHEETY_USER')
    sheety_password = os.environ.get('SHEETY_PASSWORD')
    sheet_headers = HTTPBasicAuth(username=sheety_user, password=sheety_password)
    for n in range(0, len(system_df)):
        print(system_df.loc[n]['id'])
        sheet_params = {
            "клиенту": {
                "system": sys,
                "supportname": system_df.loc[n]['support_name'],
                "description": system_df.loc[n]['description'],
                "numberofsupports": system_df.loc[n]['number_of_supports'],
                "date": system_df.loc[n]['date'],
                "status": "Отправлено",
                "object": request.form.get("objectname"),
                "address": request.form.get("objectaddress")
                }
        }
        response_sheet = requests.post(url=sheety_endpoint, json=sheet_params, auth=sheet_headers)
    # print(response_sheet.text)

def send_smtp():
    # # добавляем к имени название объекта и переводим в формат xlsx
    # name_of_file = f'{current_user.name}_{translated_system}.csv'
    # final_filename = f'{object_name}_{current_user.name}_{translated_system}'
    # pd.read_csv(name_of_file, sep=",", encoding="utf8").to_excel(final_filename + '.xlsx', index=None)
    # filepath = final_filename + '.xlsx'  # Имя файла в абсолютном или относительном формате
    # recipients = [current_user.email, addr_to]
    # mail_coding = "windows-1251"
    # msg = MIMEMultipart()  # Создаем сообщение
    # msg['From'] = Header(current_user.email, mail_coding)  # Адресат
    # msg['To'] = Header(", ".join(recipients), mail_coding)  # Получатель
    # msg['Subject'] = Header('Спецификация HILTI', mail_coding)  # Тема сообщения
    # body = f"Спецификация на cистемy: {translated_system.lower()}.\n" \
    #        f"Объект: {object_name}.\n" \
    #        f"Адрес объекта: {object_address}.\n" \
    #        f"Проектировщик: {current_user.name}.\n" \
    #        f"Компания: {current_user.company}."
    #
    # msg.attach(MIMEText(body, 'plain', mail_coding))
    # attach_file(msg, filepath)
    #
    # with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    #     connection.starttls()
    #     connection.login(user=addr_to, password=password)
    #     connection.send_message(msg)
    #
    # os.remove(name_of_file)
    # os.remove(final_filename + '.xlsx')
    pass