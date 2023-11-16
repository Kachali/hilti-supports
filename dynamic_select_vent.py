from flask import (
    jsonify,
    Blueprint
)
import pandas as pd

dynamic_selector_vent = Blueprint('dynamic_selector_vent', __name__)

with open("static/files/Вентиляция опоры.csv", "r", encoding="Windows-1251") as file:
    data = pd.read_csv(file, delimiter=";")
    data = data.dropna()
    # print(data.columns)

# //---------------------AUTO CHANGE OF DIRECTION______________
@dynamic_selector_vent.route('/support_system/ventilation/<base_material>/direction')
def supp_directiong(base_material):
    directions = data[data["материал_основания"] == base_material]['горизонтальный/вертикальный'].unique()
    directionArray = []
    n = 0
    for direction in directions:
        directionObj = {}
        directionObj['id'] = n
        directionObj['name'] = direction
        directionArray.append(directionObj)
        n = n + 1
    # print(directionArray)
    return jsonify({'directions': directionArray})

# //---------------------AUTO CHANGE OF FASTENING CONSTRUCTION______________
@dynamic_selector_vent.route('/support_system/ventilation/<base_material>/<direction_type>/mounting')
def supp_mounting(base_material, direction_type):
    mountings = data[
        (data["материал_основания"] == base_material)
        &(data["горизонтальный/вертикальный"] == direction_type)
    ]['крепление_к'].unique()
    mountingArray = []
    n = 0
    for mounting in mountings:
        mountingObj = {}
        mountingObj['id'] = n
        mountingObj['name'] = mounting
        mountingArray.append(mountingObj)
        n = n + 1
    # print(mountingArray)
    return jsonify({'fastenings': mountingArray})


# //---------------------AUTO CHANGE OF DUCT TYPE______________
@dynamic_selector_vent.route('/support_system/ventilation/<base_material>/<direction_type>/<mounting>/duct_type')
def duct_type(base_material, direction_type, mounting):
    # print(base_material, direction_type, mounting)
    duct_types = data[
        (data["материал_основания"] == base_material)
        & (data["горизонтальный/вертикальный"] == direction_type)
        & (data['крепление_к'] == mounting)
    ]['тип_воздуховода'].unique()
    # print(duct_types)
    ductArray = []
    n = 0
    for duct in duct_types:
        ductObj = {}
        ductObj['id'] = n
        ductObj['name'] = duct
        ductArray.append(ductObj)
        n = n + 1
    # print(ductArray)

    return jsonify({'duct_types': ductArray})


# //---------------------AUTO CHANGE OF DIAMETERS______________
@dynamic_selector_vent.route('/support_system/ventilation/<base_material>/<direction_type>/<mounting>/<duct_type>/support_diameter')
def supp_diameter(base_material, direction_type, mounting, duct_type):
    supp_diameters = data[
        (data["материал_основания"] == base_material)
        & (data["горизонтальный/вертикальный"] == direction_type)
        & (data['крепление_к'] == mounting)
        & (data['тип_воздуховода'] == duct_type)
    ]['диаметр/ширина'].unique()

    # print(supp_diameters)
    diameterArray = []
    n = 0
    for diameter in supp_diameters:
        diameterObj = {}
        diameterObj['id'] = n
        diameterObj['name'] = int(diameter)
        diameterArray.append(diameterObj)
        n = n + 1
    # print(diameterArray)

    return jsonify({'support_diameters': diameterArray})
