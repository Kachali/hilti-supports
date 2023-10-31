from flask import (
    jsonify,
    Blueprint
)
import pandas as pd

dynamic_selector_hot_water = Blueprint('dynamic_selector', __name__)

with open("static/files/Трубы с температурным расширением.csv", "r", encoding="Windows-1251") as file:
    data = pd.read_csv(file, delimiter=";")
    # print(data.columns)


@dynamic_selector_hot_water.route('/support_system/hot_water/<direction_type>/mounting')
def supp_mounting(direction_type):
    mountings = data[data["горизонтальный/вертикальный"] == direction_type]['крепление_к'].unique()
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


@dynamic_selector_hot_water.route('/support_system/hot_water/<direction_type>/<mounting>/support_type')
def supp_type(mounting, direction_type):
    supp_types = data[
        (data["горизонтальный/вертикальный"] == direction_type)
        & (data['крепление_к'] == mounting)
    ]['тип_опоры'].unique()
    # print(supp_types)
    supportArray = []
    n = 0
    for support in supp_types:
        supportObj = {}
        supportObj['id'] = n
        supportObj['name'] = support
        supportArray.append(supportObj)
        n = n + 1
    # print(supportArray)

    return jsonify({'support_types': supportArray})

