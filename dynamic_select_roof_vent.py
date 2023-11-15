from flask import (
    jsonify,
    Blueprint
)
import pandas as pd

dynamic_selector_roof_vent = Blueprint('dynamic_selector_roof_vent', __name__)

with open("static/files/Вентиляция на кровле.csv", "r", encoding="Windows-1251") as file:
    data = pd.read_csv(file, delimiter=";")
    data = data.dropna()
    # print(data.columns)


# //---------------------AUTO CHANGE OF DIAMETER______________
@dynamic_selector_roof_vent.route('/support_system/roof_vent/<duct_type>/diameter')
def supp_diameter(duct_type):
    diameters = data[data["Сечение воздуховода"] == duct_type]['Ширина/диаметр воздуховода'].unique()
    # print(diameters)
    diameterArray = []
    n = 0
    for diameter in diameters:
        diameterObj = {}
        diameterObj['id'] = n
        diameterObj['name'] = int(diameter)
        diameterArray.append(diameterObj)
        n = n + 1
    # print(diameterArray)
    return jsonify({'diameters': diameterArray})

# //---------------------AUTO CHANGE OF HEIGHT______________
@dynamic_selector_roof_vent.route('/support_system/roof_vent/<duct_type>/<diameter>/<load>/height')
def supp_height(duct_type, diameter, load):
    heights = data[
        (data["Сечение воздуховода"] == duct_type)
        & (data["Ширина/диаметр воздуховода"] == int(diameter))
        & (data["Нагрузка"] == load)
    ]['Максимальная высота опоры'].unique()
    heightArray = []
    n = 0
    for height in heights:
        heightObj = {}
        heightObj['id'] = n
        heightObj['name'] = int(height)
        heightArray.append(heightObj)
        n = n + 1
    # print(heightArray)
    return jsonify({'heights': heightArray})