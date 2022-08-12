from earth_api import EarthAPI
import re

# get degress, minutes, seconds from string
def get_degress_minutes_seconds(desc_string):
    # get degress
    degress = desc_string.split('°')[0][2:]
    # get minutes
    minutes = desc_string.split('°')[1].split('′')[0]
    # get seconds
    seconds = desc_string.split('°')[1].split('′')[1].split('″')[0]
    return degress, minutes, seconds

# convert degress, minutes, seconds to decimal degree
def convert_degress_minutes_seconds_to_decimal_degree(degress, minutes, seconds):
    decimal_degree = float(degress) + float(minutes) / 60 + float(seconds) / 3600
    return decimal_degree

def consturct_ring(lat_array, lon_array):
    ring = []
    for i in range(len(lat_array)):
        ring.append([lon_array[i], lat_array[i]])
    ring.append([lon_array[0], lat_array[0]])
    return ring 

# get location from string
def get_location_from_string(desc_string):
    # split string by '、' and '，'
    sections = re.split('，|、', desc_string)

    lat_array = []
    lon_array = []

    for s in sections:
        if '北纬' in s:
            degress, minutes, seconds = get_degress_minutes_seconds(s)
            lat = convert_degress_minutes_seconds_to_decimal_degree(degress, minutes, seconds)
            lat_array.append(lat)
        if '东经' in s:
            degress, minutes, seconds = get_degress_minutes_seconds(s)
            lon = convert_degress_minutes_seconds_to_decimal_degree(degress, minutes, seconds) 
            lon_array.append(lon)
    return consturct_ring(lat_array, lon_array)


def generate_drawings_from_string(name, desc_string):
    ring = get_location_from_string(desc_string)
    drawing = {
        "visible": True,
        "title":name,
        "geometry":{
            "rings":[
                    ring 
            ],
            "spatialReference":{
                "wkid":4326
            }
        }
    }
    return drawing

def get_variable_name(variable):
    loc = globals()
    for k,v in loc.items():
        if loc[k] ==variable:
            return k

if __name__ == '__main__':
    a1 = "北纬25°15′26″、东经120°29′20″，北纬24°50′30″、东经120°05′45″，北纬25°04′32″、东经119°51′22″，北纬25°28′12″、东经120°14′30″四点连线。"
    a2 = "北纬26°07′00″、东经121°57′00″，北纬25°30′00″、东经121°57′00″，北纬25°30′00″、东经121°28′00″，北纬26°07′00″、东经121°28′00″四点连线。"
    a3 = "北纬25°34′00″、东经122°50′00″，北纬25°03′00″、东经122°50′00″，北纬25°03′00″、东经122°11′00″，北纬25°34′00″、东经122°11′00″四点连线。"
    a4 = "北纬22°56′00″、东经122°40′00″，北纬23°38′00″、东经122°51′00″，北纬23°38′00″、东经123°23′00″，北纬22°56′00″、东经123°09′00″四点连线。"
    a5 = "北纬21°14′00″、东经121°33′00″，北纬21°33′00″、东经121°18′00″，北纬21°07′00″、东经120°43′00″，北纬20°48′00″、东经120°59′00″四点连线。"
    a6 = "北纬22°43′00″、东经119°14′00″，北纬22°10′00″、东经119°06′00″，北纬21°33′00″、东经120°29′00″，北纬22°09′00″、东经120°32′00″四点连线。"

    area_array = [a1, a2, a3, a4, a5, a6]

    earth_api = EarthAPI()
    for area in area_array:
        d = generate_drawings_from_string(get_variable_name(area), area)
        earth_api.add_drawing(d)

