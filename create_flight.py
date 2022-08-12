from time import sleep
import tkinter as tk
from earth_api import EarthAPI

earth = EarthAPI()
camera_array = []

# create a root window
root = tk.Tk()
root.title("earth flight")
root.geometry("300x200")

flight_template = {
    "camera": {
        "position": {
            "x": -92,
            "y": 41,
            "z": 11000000,
            "spatialReference": {
                "wkid": 4326
            }
        },
        "heading": 2.3335941892764884E-17,
        "tilt": 6.144145559063083E-15,
        "roll": 0
    },
    "duration": 2
}

point_drawing_template = {
  "visible": True,
  "title": "addPoint",
  "geometry": {
      "x": -100,
      "y": 40,
      "spatialReference": {"wkid": 4326}
      },
   "symbol": {
       "type": "picture-marker",
       "url":"https://static.arcgis.com/images/Symbols/Shapes/BlackStarLargeB.png",
       "size": "64px"
      },
   "labelSymbol":{
        "type":"text",
        "color": [76,115,0,255],
        "size":12
    }
}

line_drawing_template = {
  "visible": True,
  "title": "addLine",
  "geometry": {
         "paths": [
             [
                -118,
                34
              ],
             [
                -100,
                40
              ],
             [
                -82,
                34
              ]
          ],
        "spatialReference": {"wkid": 4326}
       },
  "symbol": {
         "type": "simple-line",
         "color": "#33cc33",
         "width": "2px"
        }
 }



DEFAULT_DURATION = 2

def save_camera():
    global earth
    global camera_array
    code, camera = earth.get_camera()
    camera_array.append(camera)

button = tk.Button(root, text="save camera", command=save_camera)
button.pack()


def play():
    global earth
    global camera_array
    for ca in camera_array:
        flight = flight_template.copy()
        flight['camera'] = ca
        earth.set_flight(flight)
        sleep(DEFAULT_DURATION)

button2 = tk.Button(root, text="play", command=play)
button2.pack()

def generate_line_drawing(point_array):
    paths = [point_array]
    line = line_drawing_template.copy()
    line['geometry']['paths'] = paths
    line['geometry']["spatialReference"] = {"wkid": 4326}
    return line


def display():
    global earth
    global camera_array
    point_array = []
    for ca in camera_array:
        point_drawing = point_drawing_template.copy()
        point_drawing['geometry'] = ca['position']
        point_drawing['geometry']["spatialReference"] = {"wkid": 4326}
        point_array.append([
            ca['position']['x'],
            ca['position']['y'], 
            ca['position']['z']])
        earth.add_drawing(point_drawing)
        sleep(DEFAULT_DURATION)

    line_drawing = generate_line_drawing(point_array)
    earth.add_drawing(line_drawing)

button3 = tk.Button(root, text="display", command=display)
button3.pack()

# end
root.mainloop()