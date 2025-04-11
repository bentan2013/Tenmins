import time
import tkinter as tk
from copy import deepcopy
from earth_api import EarthAPI

class EarthViewer:
    DEFAULT_DURATION = 2
    BASE_TEMPLATES = {
        'flight': {
            "camera": None,
            "duration": DEFAULT_DURATION
        },
        'point': {
            "visible": True,
            "title": "addPoint",
            "geometry": {"spatialReference": {"wkid": 4326}},
            "symbol": {
                "type": "picture-marker",
                "url": "https://static.arcgis.com/images/Symbols/Shapes/BlackStarLargeB.png",
                "size": "64px"
            }
        },
        'line': {
            "visible": True,
            "title": "addLine",
            "geometry": {
                "paths": [],
                "spatialReference": {"wkid": 4326}
            },
            "symbol": {
                "type": "simple-line",
                "color": "#33cc33",
                "width": "2px"
            }
        }
    }

    def __init__(self):
        self.earth = EarthAPI(**{"version":"1.16"})
        self.cameras = []
        self.root = self._create_ui()
        
    def _create_ui(self):
        root = tk.Tk()
        root.title("Earth Flight Control")
        root.geometry("300x300")  # 调整窗口高度

        # 相机控制行
        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)
        # ... 原有的roll控件 ...
        tk.Label(control_frame, text="Roll:").pack(side=tk.LEFT)
        self.roll_entry = tk.Entry(control_frame, width=8)
        self.roll_entry.pack(side=tk.LEFT, padx=5)
        
        set_btn = tk.Button(control_frame, text="Set Camera", command=self.set_camera)
        set_btn.pack(side=tk.LEFT)


        # 功能按钮区域
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        
        main_controls = [
            ("Save Camera", self.save_camera),
            ("Save Flight", self.save_flight),
            ("Play Flight", self.play_flight),
            ("Display Flight", self.display_path)
        ]
        
        for text, command in main_controls:
            btn = tk.Button(btn_frame, text=text, command=command)
            btn.pack(pady=2, fill=tk.X)

        # 加载飞行路径控件
        load_frame = tk.Frame(root)
        load_frame.pack(pady=5)
        
        self.load_entry = tk.Entry(load_frame, width=20)
        self.load_entry.pack(side=tk.LEFT, padx=5)
        
        load_btn = tk.Button(load_frame, text="Load Flight", command=self.load_flight)
        load_btn.pack(side=tk.LEFT)

        return root

    def save_flight(self):
        if not self.cameras:
            messagebox.showwarning("Warning", "No camera data to save!")
            return

        filename = f"flight_{uuid.uuid4().hex[:8]}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(self.cameras, f, indent=2)
            messagebox.showinfo("Saved", f"Flight path saved to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {str(e)}")

    def load_flight(self):
        filename = self.load_entry.get().strip()
        if not filename:
            messagebox.showwarning("Warning", "Please enter a filename")
            return

        try:
            with open(filename, 'r') as f:
                self.cameras = json.load(f)
            messagebox.showinfo("Loaded", f"Successfully loaded {len(self.cameras)} cameras")
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {filename}")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format")
        except Exception as e:
            messagebox.showerror("Error", f"Load failed: {str(e)}")

    def set_camera(self):
        try:
            # 获取用户输入的roll值
            new_roll = float(self.roll_entry.get())
            
            # 获取当前相机参数
            code, camera = self.earth.get_camera()
            if code != 200:
                return
                
            # 更新roll值
            camera['roll'] = new_roll
            
            # 设置新参数
            self.earth.set_camera(camera)
            
        except ValueError:
            # 处理无效输入
            self.roll_entry.delete(0, tk.END)
            self.roll_entry.insert(0, "Invalid Number")

    def _create_drawing(self, dtype, geometry):
        template = deepcopy(self.BASE_TEMPLATES[dtype])
        template['geometry'].update(geometry)
        return template

    def save_camera(self):
        code, camera = self.earth.get_camera()
        if code == 200:
            self.cameras.append(deepcopy(camera))

    def play_flight(self):
        for camera in self.cameras:
            flight = self.BASE_TEMPLATES['flight'].copy() 
            flight['camera'] = camera
            self.earth.set_flight(flight)
            time.sleep(self.DEFAULT_DURATION)

    def display_path(self):
        points = []
        for camera in self.cameras:
            # 提取三维坐标
            pos = camera['position']
            point_geo = {
                'x': pos['x'],
                'y': pos['y'],
                'z': pos['z']  # 新增z坐标
            }

            point = self._create_drawing('point', point_geo)
            self.earth.add_drawing(point)
            points.append([pos['x'], pos['y'], pos['z']])  # 三维坐标点
            time.sleep(self.DEFAULT_DURATION)

        line = self._create_drawing('line', {'paths': [points]})
        self.earth.add_drawing(line)

if __name__ == "__main__":
    viewer = EarthViewer()
    viewer.root.mainloop()
