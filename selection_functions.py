import pandas as pd
import math


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
            return [final_number,num_of_supports,description]

        except IndexError:
            return False


def sprinkler_support(support):
    base_material = support['parameters']['base_material']
    direction_type = support['parameters']['direction_type']
    pipe_type = support['parameters']['pipe_type']
    diameter = int(support['parameters']['diameter'])
    length = int(support['parameters']['length'])
    with open('static/files/Спринклеры.csv', 'r', encoding='utf-8') as file:
        data = pd.read_csv(file, delimiter=';')
        # print(data.columns, data.shape)
        support_num = data.loc[(data['крепление_к'] == base_material) & (data['диаметр_трубы'] == diameter)]
        # final_number = support_num['номер_опоры'].values[0]
        try:
            step = support_num.iloc[0]['шаг_опор']
            step_float = float(step.replace(',','.'))
            num_of_supports = math.ceil(length / step_float)
            print(num_of_supports)
            final_number = support_num['номер_опоры'].values[0]
            print(final_number)
            if base_material == 'Профилированный лист':
                proflist_load_less57 = int(support_num.iloc[0]['нагрузка_на_профлист(гофра менее 57мм)'])
                proflist_load_more57 = int(support_num.iloc[0]['нагрузка_на_профлист(гофра более 57мм)'])
                description = f'{base_material},{direction_type},{pipe_type}, {diameter}мм, {length}м, максимальная ' \
                              f'нагрузка на профлист при высоте гофры менее 57мм - {proflist_load_less57}мм, более 57мм - {proflist_load_more57}'
            else:
                description = f'{base_material},{direction_type},{pipe_type}, {diameter}мм, {length}м, по всем вопросам обращаться к специалисту компании HILTI'
            print(f'Номер опоры {final_number}, количество опор {num_of_supports}, {description}')
            return [final_number,num_of_supports,description]

        except IndexError:
            return False
