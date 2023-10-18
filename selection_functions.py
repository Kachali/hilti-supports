import pandas as pd
import math

diameters_hot_water = [
    "8 (11-15)",
    "10 (16-19)",
    "15 (20-24)",
    "20 (25-28)",
    "25 (32-35)",
    "32 (39-46)",
    "40 (48-53)",
    "50 (53-58)",
    "50 (60-65)",
    "60 (67-71)",
    "65 (74-80)",
    "70 (81-86)",
    "80 (88-94)",
    "90 (99-105)",
    "100 (108-116)",
    "110 (120-130)",
    "125 (135-143)",
    "140 (145-155)",
    "150 (162-170)",
    "175 (195-205)",
    "200 (207-219)",
    "225 (248-255)",
    "250 (260-274)",
]

steel_pipe_mounting_step = {
    "diameter_hot_water": [
        "8",
        "10",
        "15",
        "20",
        "25",
        "32",
        "40",
        "50",
        "60",
        "65",
        "70",
        "80",
        "90",
        "100",
        "110",
        "125",
        "140",
        "150",
        "175",
        "200",
        "225",
        "250",
    ],
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
    duct_type = support["parameters"]["duct_type"]
    diameter = int(support["parameters"]["diameter"])
    length = int(support["parameters"]["length"])
    if (
        diameter < 400
        and direction_type == "Горизонтальная/потолок"
        or direction_type == "Горизонтальная/стена"
        or direction_type == "Горизонтальная/пол"
    ):
        num_of_supports = math.ceil(length / 4)
    else:
        num_of_supports = math.ceil(length / 3)

    # print(base_material, direction_type, duct_type, diameter, num_of_supports)
    with open(
        "static/files/Вентиляция опоры csv2.csv", "r", encoding="Windows-1251"
    ) as file:
        data = pd.read_csv(file, delimiter=";")
        # print(data.columns, data.shape)
        # print(data.head)
        if duct_type == "Прямоугольный" and diameter % 200 != 0:
            new_diameter = (diameter - diameter % 200) + 200
            # print(f'Введенный диаметр {diameter}, округленный диаметр {new_diameter}')
            support_num = data.loc[
                (data["крепление_к"] == base_material)
                & (data["разводка"] == direction_type)
                & (data["тип_воздуховода"] == duct_type)
                & (data["диаметр/ширина"] == new_diameter)
            ]

        else:
            support_num = data.loc[
                (data["крепление_к"] == base_material)
                & (data["разводка"] == direction_type)
                & (data["тип_воздуховода"] == duct_type)
                & (data["диаметр/ширина"] == diameter)
            ]

        try:
            final_number = support_num["номер_опоры"].values[0]
            # print(final_number)
            if (
                direction_type == "Горизонтальная/стена"
                or direction_type == "Вертикальная/стена"
            ):
                space = int(
                    support_num.iloc[0]["расстояние_от_стены_до_оси_воздуховода"]
                )
                description = f"{base_material},{direction_type},{duct_type}, {diameter}мм, {length}м, максимальное расстояние от стены до оси воздуховода {space}мм"
            else:
                description = f"{base_material},{direction_type},{duct_type}, {diameter}мм, {length}м, по всем вопросам обращаться к специалисту компании HILTI"
            return [final_number, num_of_supports, description]

        except IndexError:
            return False


def sprinkler_support(support):
    base_material = support["parameters"]["base_material"]
    direction_type = support["parameters"]["direction_type"]
    pipe_type = support["parameters"]["pipe_type"]
    diameter = int(support["parameters"]["diameter"])
    length = int(support["parameters"]["length"])
    with open("static/files/Спринклеры.csv", "r", encoding="utf-8") as file:
        data = pd.read_csv(file, delimiter=";")
        # print(data.columns, data.shape)
        support_num = data.loc[
            (data["крепление_к"] == base_material) & (data["диаметр_трубы"] == diameter)
        ]
        # final_number = support_num['номер_опоры'].values[0]
        try:
            step = support_num.iloc[0]["шаг_опор"]
            step_float = float(step.replace(",", "."))
            num_of_supports = math.ceil(length / step_float)
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
                description = f"{base_material},{direction_type},{pipe_type}, {diameter}мм, {length}м, по всем вопросам обращаться к специалисту компании HILTI"
            print(
                f"Номер опоры {final_number}, количество опор {num_of_supports}, {description}"
            )
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
    nominal_diameter = diameter.split(" ")[0]
    diameter_diapason = diameter.split(" ")[1].replace("(", "").replace(")", "")
    isolation = support["parameters"]["isolation"]
    length = int(support["parameters"]["length"])
    # print(base_material, direction_type, mounting, distance, pipe_number, support_type)
    with open("static/files/Трубы с температурным расширением.csv", "r", encoding="Windows-1251") as file:
        data = pd.read_csv(file, delimiter=";")
        print(data.columns, data.shape)
        support_num = data.loc[
            (data["материал_основания"] == base_material)
            & (data["горизонтальный/вертикальный"] == direction_type)
            & (data["крепление_к"] == mounting)
            & (data["вылет"] == distance)
            & (data["тип_опоры"] == support_type)
            & (data["кол-во_труб"] == pipe_number)
            & (data["диапазон_диаметров"] == diameter_diapason)
        ]
        print(support_num)
        try:
            final_number = support_num["номер_опоры"].values[0]
            print(final_number)
            pipe_index = steel_pipe_mounting_step["diameter_hot_water"].index(
                nominal_diameter
            )
            if isolation == "Да":
                step = float(steel_pipe_mounting_step["step_isolated"][pipe_index])
            else:
                step = float(steel_pipe_mounting_step["step_non_isolated"][pipe_index])
            num_of_supports = math.ceil(length / step)
            print(
                f"Длина участка {length}, условный диаметр трубы {diameter[0]}, шаг опор {step}, колиичство опор {num_of_supports}"
            )
            description = f"{base_material}, {direction_type}, {mounting}, {distance}, изоляция: {isolation}, {diameter}мм, {length}м, по всем вопросам обращаться к специалисту компании HILTI"
            print(
                f"Номер опоры {final_number}, количество опор {num_of_supports}, {description}"
            )
            return [final_number, num_of_supports, description]

        except IndexError:
            return False
