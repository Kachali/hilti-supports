from flask import (
    jsonify,
    Blueprint
)
import pandas as pd

dynamic_selector_sprinkler = Blueprint('dynamic_selector_sprinkler', __name__)

with open("static/files/Спринклеры.csv", "r", encoding="Windows-1251") as file:
    data = pd.read_csv(file, delimiter=";")
    # print(data.columns)

# //---------------------AUTO CHANGE OF DIAMETERS______________
@dynamic_selector_sprinkler.route('/support_system/sprinkler/<base_material>/<direction_type>/support_diameter')
def supp_diameter(base_material, direction_type):
    supp_diameters = data[
        (data["материал_основания"] == base_material)
        & (data["разводка"] == direction_type)
    ]['диаметр_трубы'].unique()

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