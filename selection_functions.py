import pandas as pd
import math

diameters_hot_water = [
    "8(11-15)",
    "10(16-19)",
    "15(20-24)",
    "20(25-28)",
    "25(32-35)",
    "32(39-46)",
    "40(48-53)",
    "50(53-58)",
    "50(60-65)",
    "60(67-71)",
    "65(74-80)",
    "70(81-86)",
    "80(88-94)",
    "90(99-105)",
    "100(108-116)",
    "110(120-130)",
    "125(135-143)",
    "140(145-155)",
    "150(162-170)",
    "175(195-205)",
    "200(207-219)",
    "225(248-255)",
    "250(260-274)",
]

steel_pipe_mounting_step = {
    "diameter_hot_water": diameters_hot_water,
    "step_non_isolated": [
        "2.5",
        "2.5",
        "2.5",
        "3",
        "3.5",
        "4",
        "4.5",
        "5",
        "5",
        "5",
        "6",
        "6",
        "6",
        "6",
        "7",
        "7",
        "8",
        "8",
        "8",
        "8",
        "8",
    ],
    "step_isolated": [
        "1.5",
        "1.5",
        "1.5",
        "2",
        "2",
        "2.5",
        "3",
        "3",
        "3",
        "3",
        "4",
        "4",
        "4",
        "4.5",
        "4.5",
        "5",
        "5",
        "6",
        "6",
        "6",
        "6",
        "6",
    ],
}

def vent_support(support):
    base_material = support["parameters"]["base_material"]
    direction_type = support["parameters"]["direction_type"]
    mounting = support["parameters"]["mounting"]
    duct_type = support["parameters"]["duct_type"]
    diameter = int(support["parameters"]["diameter"])
    length = float(support["parameters"]["length"])
    if (
        diameter < 400
        and direction_type == "Горизонтальная"
    ):
        num_of_supports = math.ceil(length / 4) + 1
    else:
        num_of_supports = math.ceil(length / 3) + 1

    # print(base_material, direction_type, mounting, duct_type, diameter, length, num_of_supports)
    with open(
        "static/files/Вентиляция опоры.csv", "r", encoding="Windows-1251"
    ) as file:
        data = pd.read_csv(file, delimiter=";")
        support_num = data.loc[
            (data["материал_основания"] == base_material)
            & (data["горизонтальный/вертикальный"] == direction_type)
            & (data["крепление_к"] == mounting)
            & (data["тип_воздуховода"] == duct_type)
            & (data["диаметр/ширина"] == diameter)
        ]
        # print(support_num)
        try:
            final_number = support_num["номер_опоры"].values[0]
            description = f"{base_material}, {direction_type}, {mounting}, {duct_type}, {diameter}мм, {length}м, по всем вопросам обращаться к специалисту компании HILTI"
            return [final_number, num_of_supports, description]

        except IndexError:
            return False


def hot_water_supports(support):
    base_material = support["parameters"]["base_material"]
    direction_type = support["parameters"]["direction_type"]
    mounting = support["parameters"]["mounting"]
    distance = int(support["parameters"]["distance"])
    pipe_number = int(support["parameters"]["pipe_number"])
    # pipe_type = support['parameters']['pipe_type']
    support_type = support['parameters']['support_type']
    diameter = support["parameters"]["diameter"]
    isolation = support["parameters"]["isolation"]
    length = float(support["parameters"]["length"])
    # print(base_material, direction_type, mounting, distance, pipe_number, support_type, diameter)
    with open("static/files/Трубы с температурным расширением.csv", "r", encoding="Windows-1251") as file:
        data = pd.read_csv(file, delimiter=";")
        # print(data.columns, data.shape)
        support_num = data.loc[
            (data["материал_основания"] == base_material)
            & (data["горизонтальный/вертикальный"] == direction_type)
            & (data["крепление_к"] == mounting)
            & (data["вылет"] == distance)
            & (data["тип_опоры"] == support_type)
            & (data["кол-во_труб"] == pipe_number)
            & (data["все диаметры"] == diameter)
        ]
        # print(support_num)
        try:
            final_number = support_num["номер_опоры"].values[0]
            # print(final_number)
            # print(steel_pipe_mounting_step["diameter_hot_water"][0])
            pipe_index = steel_pipe_mounting_step["diameter_hot_water"].index(diameter)
            if isolation == "Есть":
                step = float(steel_pipe_mounting_step["step_isolated"][pipe_index])
            else:
                step = float(steel_pipe_mounting_step["step_non_isolated"][pipe_index])
            num_of_supports = math.ceil(length / step) + 1
            # print(
            #     f"Длина участка {length}, условный диаметр трубы {diameter[0]}, шаг опор {step}, колиичство опор {num_of_supports}"
            # )
            description = f"{base_material}, {direction_type}, {mounting}, {distance}, изоляция: {isolation}, {diameter}мм, {length}м, по всем вопросам обращаться к специалисту компании HILTI"
            # print(
            #     f"Номер опоры {final_number}, количество опор {num_of_supports}, {description}"
            # )
            return [final_number, num_of_supports, description]

        except IndexError:
            return False


def sprinkler_support(support):
    base_material = support["parameters"]["base_material"]
    direction_type = support["parameters"]["direction_type"]
    pipe_type = support["parameters"]["pipe_type"]
    diameter = int(support["parameters"]["diameter"])
    length = float(support["parameters"]["length"])
    with open("static/files/Спринклеры.csv", "r", encoding="Windows-1251") as file:
        data = pd.read_csv(file, delimiter=";")
        # print(data.columns, data.shape)
        support_num = data.loc[
            (data["материал_основания"] == base_material) & (data["диаметр_трубы"] == diameter)
        ]
        # final_number = support_num['номер_опоры'].values[0]
        try:
            step = float(support_num.iloc[0]["шаг_опор"])
            num_of_supports = math.ceil(length / step) + 1
            print(num_of_supports)
            final_number = support_num["номер_опоры"].values[0]
            print(final_number)
            if base_material == "Профилированный лист":
                proflist_load_less57 = int(
                    support_num.iloc[0]["нагрузка_на_профлист(гофра менее 57мм)"]
                )
                proflist_load_more57 = int(
                    support_num.iloc[0]["нагрузка_на_профлист(гофра более 57мм)"]
                )
                description = (
                    f"{base_material},{direction_type},{pipe_type}, {diameter}мм, {length}м, максимальная "
                    f"нагрузка на профлист при высоте гофры менее 57мм - {proflist_load_less57}мм, более 57мм - {proflist_load_more57}"
                )
            else:
                description = f"{base_material}, {direction_type}, {pipe_type}, {diameter}мм, {length}м, по всем вопросам обращаться к специалисту компании HILTI"
            # print(
            #     f"Номер опоры {final_number}, количество опор {num_of_supports}, {description}"
            # )
            return [final_number, num_of_supports, description]

        except IndexError:
            return False


def roof_vent_supports(support):
    duct_type = support["parameters"]["duct_type"]
    diameter = int(support["parameters"]["diameter"])
    load = support["parameters"]["load"]
    space = int(support["parameters"]["space"])
    length = float(support["parameters"]["length"])
    # print(duct_type,  diameter, load, space, length)

    with open("static/files/Вентиляция на кровле.csv", "r", encoding="Windows-1251") as file:
        data = pd.read_csv(file, delimiter=";")
        # print(data.columns, data.shape)
        support_num = data.loc[
            (data["Сечение воздуховода"] == duct_type)
            & (data["Ширина/диаметр воздуховода"] == diameter)
            & (data["Нагрузка"] == load)
            & (data["Максимальная высота опоры"] == space)
        ]
        try:
            step = support_num.iloc[0]["Шаг опор"]
            num_of_supports = math.ceil(length / step) + 1
            final_number = support_num["номер_опоры"].values[0]
            description = f"{duct_type}, {diameter}мм, {load.lower()}, максимальная высота опоры {space}мм, длина участка {length}м, по всем вопросам обращаться к специалисту компании HILTI"
            # print(
            #     f"Номер опоры {final_number}, количество опор {num_of_supports}, {description}"
            # )
            return [final_number, num_of_supports, description]

        except IndexError:
            return False