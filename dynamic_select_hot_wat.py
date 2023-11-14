from flask import (
    jsonify,
    Blueprint
)
import pandas as pd

dynamic_selector_hot_water = Blueprint('dynamic_selector', __name__)

with open("static/files/Трубы с температурным расширением.csv", "r", encoding="Windows-1251") as file:
    data = pd.read_csv(file, delimiter=";")
    data = data.dropna()
    # print(data.columns)


# //---------------------AUTO CHANGE OF DIRECTION______________
@dynamic_selector_hot_water.route('/support_system/hot_water/<base_material>/direction')
def supp_directiong(base_material):
    directions = data[data["материал_основания"] == base_material]['горизонтальный/вертикальный'].unique()
    # print(directions)
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
@dynamic_selector_hot_water.route('/support_system/hot_water/<base_material>/<direction_type>/mounting')
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


# //---------------------AUTO CHANGE OF SUPPORT TYPE______________
@dynamic_selector_hot_water.route('/support_system/hot_water/<base_material>/<direction_type>/<mounting>/support_type')
def supp_type(base_material, direction_type, mounting):
    print(base_material, direction_type, mounting)
    supp_types = data[
        (data["материал_основания"] == base_material)
        & (data["горизонтальный/вертикальный"] == direction_type)
        & (data['крепление_к'] == mounting)
    ]['тип_опоры'].unique()
    print(supp_types)
    supportArray = []
    n = 0
    for support in supp_types:
        supportObj = {}
        supportObj['id'] = n
        supportObj['name'] = support
        supportArray.append(supportObj)
        n = n + 1
    print(supportArray)

    return jsonify({'support_types': supportArray})


# //---------------------AUTO CHANGE OF DIAMETERS______________
@dynamic_selector_hot_water.route('/support_system/hot_water/<base_material>/<direction_type>/<mounting>/<support_type>/support_diameter')
def supp_diameter(base_material, direction_type, mounting, support_type):
    supp_diameters = data[
        (data["материал_основания"] == base_material)
        & (data["горизонтальный/вертикальный"] == direction_type)
        & (data['крепление_к'] == mounting)
        & (data['тип_опоры'] == support_type)
    ]['все диаметры'].unique()

    # print(supp_diameters)
    diameterArray = []
    n = 0
    for diameter in supp_diameters:
        diameterObj = {}
        diameterObj['id'] = n
        diameterObj['name'] = diameter
        diameterArray.append(diameterObj)
        n = n + 1
    # print(diameterArray)

    return jsonify({'support_diameters': diameterArray})


# //---------------------AUTO CHANGE OF DISTANCE______________
@dynamic_selector_hot_water.route('/support_system/hot_water/<base_material>/<direction_type>/<mounting>/<support_type>/<support_diameter>/support_distance')
def supp_distance(base_material, direction_type, mounting, support_type, support_diameter):
    supp_distance = data[
        (data["материал_основания"] == base_material)
        & (data["горизонтальный/вертикальный"] == direction_type)
        & (data['крепление_к'] == mounting)
        & (data['тип_опоры'] == support_type)
        & (data['все диаметры'] == support_diameter)
    ]['вылет'].unique()

    supp_distance.sort()
    # print(supp_distance)
    new_supp_distance = [int(supp) for supp in supp_distance]
    # print(new_supp_distance)
    distanceArray = []
    n = 0
    for distance in new_supp_distance:
        distanceObj = {}
        distanceObj['id'] = n
        distanceObj['name'] = distance
        distanceArray.append(distanceObj)
        n = n + 1
    # print(distanceArray)

    return jsonify({'support_distances': distanceArray})


# --------------------- AUTO CHANGE OF PIPE NUMBER ______________
@dynamic_selector_hot_water.route('/support_system/hot_water/<base_material>/<direction_type>/<mounting>/<support_type>/<support_diameter>/<support_distance>/pipe_number')
def pipe_number(base_material, direction_type, mounting, support_type, support_diameter, support_distance):
    number_of_pipes = data[
        (data["материал_основания"] == base_material)
        &(data["горизонтальный/вертикальный"] == direction_type)
        & (data['крепление_к'] == mounting)
        & (data['тип_опоры'] == support_type)
        & (data['все диаметры'] == support_diameter)
        & (data['вылет'] == int(support_distance))
    ]['кол-во_труб'].unique()
    new_number_of_pipes = [int(number) for number in number_of_pipes]
    # print(new_number_of_pipes)
    pipeNumberArray = []
    n = 0
    for pipeNumber in new_number_of_pipes:
        pipeNumberObj = {}
        pipeNumberObj['id'] = n
        pipeNumberObj['name'] = pipeNumber
        pipeNumberArray.append(pipeNumberObj)
        n = n + 1
    # print(pipeNumberArray)

    return jsonify({'number_of_pipes': pipeNumberArray})