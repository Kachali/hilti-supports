from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

base_materials = ['Железобетон', 'Металлоконструкции (швеллер с наклоном)', 'Металлоконструкции (швеллер без наклона)',
                  'Металлоконструкции (двутавр)','Металлоконструкции (прямоуг. труба в обжим)', "Кирпич", 'Ребристые плиты перекрытия', 'Профилированный лист']
direction = ['Горизонтальная/потолок', 'Горизонтальная/пол', 'Горизонтальная/стена', 'Вертикальная/потолок', 'Вертикальная/стена']
duct_type = ['Круглый', 'Прямоугольный']
heating_type = ['Отопление', 'Горячее водоснабжение', 'Другое']
cold_water_type = ['Холодное водоснабжение','Канализация']
pipe_type = ['Стальная труба', 'Пластиковая труба', 'Чугунная труба', 'Нержавеющая сталь']

class ChooseSystemForm(FlaskForm):
    system = SelectMultipleField(u'Тип крепления:',
                                   choices=[('hot_water','Трубопроводы с температурным расширением (отопление, ГВ)'),
                                            ('cold_water','Трубопроводы без температурного расширения (ХВ, канализация)'),
                                            ('sprinkler','Спринклерное пожаротушение'),
                                            ('ventilation','Вентиляция'),
                                            ('radial_fans', "Оборудование на кровле"),
                                            ('roof_equipment', "Обвязка по кровле"),
                                            ],
                                 )
    submit = SubmitField(label="Выбрать")

class VentForm(FlaskForm):
    base_material = SelectField('Крепление к:', choices=base_materials)
    direction_type = SelectField('Тип разводки:', choices=direction)
    duct_type = SelectField('Тип воздуховода:', choices=duct_type)
    # through_fastening = SelectField('Возможно ли крепление насквозь:', choices=['нет','да'])
    diameter = StringField(label='Диаметр/ширина воздуховода, мм')
    # height = StringField(label='Высота воздуховода, мм')
    length = StringField(label='Длина трассы, м', validators=[DataRequired()])
    submit = SubmitField(label="Выбрать")

class HotWaterForm(FlaskForm):
    base_material = SelectField('Крепление к:', choices=base_materials)
    direction_type = SelectField('Тип разводки:', choices=direction)
    system = SelectField('Система:', choices=heating_type)
    pipe_type = SelectField('Тип трубы:', choices=pipe_type)
    system_type = StringField(label='Принадлежность к системе (Т1, T2)')
    temperature = StringField(label='Температура в системе, °C', validators=[DataRequired()])
    diameter = StringField(label='Диаметр трубы, мм', validators=[DataRequired()])
    length = StringField(label='Длина трассы, м', validators=[DataRequired()])
    submit = SubmitField(label="Добавить")


class ColdWaterForm(FlaskForm):
    base_material = SelectField('Крепление к:', choices=base_materials)
    direction_type = SelectField('Тип разводки:', choices=direction)
    system = SelectField('Система:', choices=cold_water_type)
    pipe_type = SelectField('Тип трубы:', choices=pipe_type)
    system_type = StringField(label='Принадлежность к системе (К1, В2)')
    diameter = StringField(label='Диаметр трубы, мм', validators=[DataRequired()])
    length = StringField(label='Длина трассы, м', validators=[DataRequired()])
    submit = SubmitField(label="Добавить")

class SprinklerForm(FlaskForm):
    base_material = SelectField('Крепление к:', choices=base_materials)
    direction_type = SelectField('Тип разводки:', choices=['Горизонтальная/потолок'])
    pipe_type = SelectField('Тип трубы:', choices=['Стальная труба'])
    diameter = StringField(label='Диаметр трубы, мм', validators=[DataRequired()])
    length = StringField(label='Длина трассы, м', validators=[DataRequired()])
    submit = SubmitField(label="Добавить")

class RadialFanForm(FlaskForm):
    roof_material = StringField(label='Тип кровли')
    city = StringField(label='Город строительства', validators=[DataRequired()])
    height = StringField(label='Высотная отметка кровли, м', validators=[DataRequired()])
    fan_length = StringField(label='Длина установки, мм', validators=[DataRequired()])
    fan_width = StringField(label='Ширина установки, мм', validators=[DataRequired()])
    fan_height = StringField(label='Высота установки, мм', validators=[DataRequired()])
    fan_weight = StringField(label='Вес оборудования, кг', validators=[DataRequired()])
    space = StringField(label='Расстояние от кровли до оборудования, мм', validators=[DataRequired()])
    submit = SubmitField(label="Добавить")

class RoofVentForm(FlaskForm):
    roof_material = StringField(label='Тип кровли:')
    city = StringField(label='Город строительства:', validators=[DataRequired()])
    height = StringField(label='Высотная отметка кровли, м', validators=[DataRequired()])
    duct_type = SelectField('Тип воздуховода:', choices=duct_type)
    diameter = StringField(label='Диаметр/ширина воздуховода, мм', validators=[DataRequired()])
    length = StringField(label='Длина трассы, м', validators=[DataRequired()])
    space = StringField(label='Расстояние от кровли до воздуховода, мм', validators=[DataRequired()])
    submit = SubmitField(label="Добавить")

