import pandas as pd
import math
from email import encoders
from email.mime.base import MIMEBase
import mimetypes
import os

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
    with open('static/Вентиляция опоры csv2.csv', 'rb', encoding='КОИ8-R') as file:
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