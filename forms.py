from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

base_materials = [
    "Железобетон",
    "Металлоконструкции (швеллер с наклоном)",
    "Металлоконструкции (швеллер без наклона)",
    "Металлоконструкции (двутавр)",
    "Металлоконструкции (прямоуг. труба в обжим)",
    "Кирпич",
    "Ребристые плиты перекрытия",
    "Профилированный лист",
]
base_materials_vent = [
    "Железобетон/кирпич",
    "Металлоконструкции (швеллер)",
    "Металлоконструкции (двутавр)",
    "Металлоконструкции (прямоуг. труба)",
    "Профлист",
]

base_materials_hot_water = [
    "Железобетон",
    "Металлоконструкции (швеллер)",
    "Металлоконструкции (двутавр)",
    "Металлоконструкции (прямоуг. труба)",
    "Кирпич",
    "Профлист",
    "Ячеистый железобетон",
    "Ребристая плита",
]
distance_hot_water_horizontal = [
    "300",
    "600",
    "1000",
    "3000",
    "6000",
]

distance_hot_water_vertical = [
    "50",
    "100",
    "150",
    "200",
    "250",
    "300",
    "400"
]
direction = [
    "Горизонтальная/потолок",
    "Горизонтальная/пол",
    "Горизонтальная/стена",
    "Вертикальная/потолок",
    "Вертикальная/стена",
]
heating_type = ["Отопление", "Горячее водоснабжение", "Другое"]
cold_water_type = ["Холодное водоснабжение", "Канализация"]
pipe_type = [
    "Стальная труба",
    "Пластиковая труба",
    "Чугунная труба",
    "Нержавеющая сталь",
]
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


class ChooseSystemForm(FlaskForm):
    system = SelectMultipleField(
        "Тип крепления:",
        choices=[
            ("ventilation", "Вентиляция"),
            ("hot_water", "Крепление трубопроводов (рядовые опоры)"),
            # ("hot_water", "Трубопроводы с температурным расширением (отопление, ГВ)"),
        # (
            #     "cold_water",
            #     "Трубопроводы без температурного расширения (ХВ, канализация)",
            # ),
            ("sprinkler", "Спринклерное пожаротушение"),
            ("fixed_supports", "Фиксирующие опоры"),
            ("radial_fans", "Оборудование на кровле"),
            ("roof_equipment", "Обвязка по кровле"),
        ],
    )
    submit = SubmitField(label="Выбрать")


class VentForm(FlaskForm):
    base_material = SelectField("Крепление к:", choices=base_materials_vent)
    direction_type = SelectField("Тип разводки:", choices=["Горизонтальный", "Вертикальный"])
    mounting = SelectField("Крепеление к:", choices=["Потолок", "Стена"])
    duct_type = SelectField("Тип воздуховода:", choices=["Круглый", "Прямоугольный"])
    # through_fastening = SelectField('Возможно ли крепление насквозь:', choices=['нет','да'])
    diameter = StringField(label="Диаметр/ширина воздуховода, мм", validators=[DataRequired()])
    # height = StringField(label='Высота воздуховода, мм')
    length = StringField(label="Длина трассы, м", validators=[DataRequired()])
    submit = SubmitField(label="Выбрать")


class HotWaterForm(FlaskForm):
    base_material = SelectField("Базовый материал:", choices=base_materials_hot_water, validate_choice=False)
    direction_type = SelectField(
        "Тип разводки:",
        # choices=["Горизонтальный", "Вертикальный"]
        validate_choice=False
    )
    mounting = SelectField(
        "Конструкция для крепления:",
        validate_choice=False
        # choices=["Потолок", "Стена", "Пол", "Колонна", "Балка", "Плита по профлисту"],
    )
    # system = SelectField('Система:', choices=heating_type)
    # pipe_type = SelectField('Тип трубы:', choices=pipe_type)
    # system_type = StringField(label='Принадлежность к системе (Т1, T2)')
    support_type = SelectField('Тип опоры:',
                               # choices=['Рядовая опора', 'Подвижная опора'])
                               # , 'Крепление регистров отопления']
                               validate_choice=False
                               )
    diameter = SelectField(
        label="Условный диаметр трубы (диапазон диаметров), мм:",
        validate_choice=False
        # choices=diameters_hot_water,
    )
    distance = SelectField("Вылет:",
                           validate_choice=False
                           # choices=distance_hot_water_horizontal
                           )
    pipe_number = SelectField('Кол-во труб:',
                              validate_choice=False
                              # choices=['1']
                              # ,'2', '3', '4']
                              )
    isolation = SelectField(label="Наличие изоляции:", choices=["Есть", "Нет"], validate_choice=False)
    length = StringField(label="Длина трассы, м:", validators=[DataRequired()])
    submit = SubmitField(label="Добавить")


class ColdWaterForm(FlaskForm):
    base_material = SelectField("Крепление к:", choices=base_materials)
    direction_type = SelectField("Тип разводки:", choices=direction)
    system = SelectField("Система:", choices=cold_water_type)
    pipe_type = SelectField("Тип трубы:", choices=pipe_type)
    system_type = StringField(label="Принадлежность к системе (К1, В2)")
    diameter = StringField(label="Диаметр трубы, мм", validators=[DataRequired()])
    length = StringField(label="Длина трассы, м", validators=[DataRequired()])
    submit = SubmitField(label="Добавить")


class SprinklerForm(FlaskForm):
    base_material = SelectField("Крепление к:", choices=base_materials)
    direction_type = SelectField("Тип разводки:", choices=["Горизонтальная/потолок"])
    pipe_type = SelectField("Тип трубы:", choices=["Стальная труба"])
    diameter = StringField(label="Диаметр трубы, мм", validators=[DataRequired()])
    length = StringField(label="Длина трассы, м", validators=[DataRequired()])
    submit = SubmitField(label="Добавить")


class FixedSupportForm(FlaskForm):
    pass


class RadialFanForm(FlaskForm):
    # roof_material = StringField(label='Тип кровли')
    # city = StringField(label='Город строительства', validators=[DataRequired()])
    wind_zone = SelectField("Ветровой район:", choices=["I", "II"])
    snow_zone = SelectField("Снеговой район:", choices=["III"])
    manufactured_by = SelectField(
        "Производитель:", choices=["ВЕЗА", "VKT", "НЗВЗ", "KORF", "NED"]
    )
    height = StringField(label="Высотная отметка кровли (не более 60м), м")
    fan_length = StringField(label="Длина установки, мм", validators=[DataRequired()])
    fan_width = StringField(label="Ширина установки, мм", validators=[DataRequired()])
    fan_height = StringField(label="Высота установки, мм", validators=[DataRequired()])
    fan_weight = StringField(label="Вес оборудования, кг", validators=[DataRequired()])
    space = SelectField(
        label="Расстояние от кровли до оборудования, мм", choices=["75", "500"]
    )
    submit = SubmitField(label="Добавить")


class RoofVentForm(FlaskForm):
    roof_material = StringField(label="Тип кровли:")
    city = StringField(label="Город строительства:", validators=[DataRequired()])
    height = StringField(
        label="Высотная отметка кровли, м", validators=[DataRequired()]
    )
    duct_type = SelectField("Тип воздуховода:", choices=["Круглый", "Прямоугольный"])
    diameter = StringField(
        label="Диаметр/ширина воздуховода, мм", validators=[DataRequired()]
    )
    length = StringField(label="Длина трассы, м", validators=[DataRequired()])
    space = StringField(
        label="Расстояние от кровли до воздуховода, мм", validators=[DataRequired()]
    )
    submit = SubmitField(label="Добавить")
