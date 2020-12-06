from time import sleep

import clr
from utils.utils import join_path
from PyQt5 import Qt

clr.AddReference(join_path("utils/OpenHardwareMonitorLib.dll"))
sensor_types = ['Voltage', 'Clock', 'Temperature', 'Load', 'Fan', 'Flow',
                'Control', 'Level', 'Factor', 'Power', 'Data', 'SmallData', 'Throughput']
hardware_types = ['Mainboard', 'SuperIO', 'cpu', 'ram', 'gpu', 'gpu', 'Heatmaster', 'hdd', 'hdd']
sub_prop = {
    'cpu': ['temperature', 'power'],
    'gpu': ['temperature', 'power'],
    'ram': [],
    'hdd': ['temperature'],
}

from OpenHardwareMonitor import Hardware

handle = Hardware.Computer()
handle.CPUEnabled = True
handle.RAMEnabled = True
handle.GPUEnabled = True
handle.HDDEnabled = True
handle.Open()


def get_hardware_info(process=False):
    lis = []
    for i in handle.Hardware:
        i.Update()
        for sub in i.SubHardware:
            print(sub)
        if i.Sensors:
            obj = {
                'id': i.Identifier.ToString(),
                'type-idx': i.HardwareType,
                'type': hardware_types[i.HardwareType],
                'name': i.Name,
                'data': []}
            data_lis = []
            for j in i.Sensors:
                data_lis.append({
                    'name': j.Name,
                    'type': sensor_types[j.SensorType],
                    'value': j.Value
                })
                obj['data'] = data_lis
            lis.append(obj)
    if not process:
        return lis
    props = {
        'cpu': [],
        'gpu': [],
        'ram': [],
        'hdd': []
    }
    for item in lis:
        if item['type'] == 'cpu':
            load = 0
            temperature = 0
            power = 0
            for data in item['data']:
                if data['name'] == 'CPU Total' and data['type'] == 'Load':
                    load = data['value']
                elif data['name'] == 'CPU Package' and data['type'] == 'Power':
                    power = data['value']
                elif data['name'] == 'CPU Package' and data['type'] == 'Temperature':
                    temperature = data['value']
            props['cpu'].append({
                'name': item['name'],
                'id': item['id'],
                'load': load,
                'temperature': temperature,
                'power': power
            })
        elif item['type'] == 'gpu':
            load = 0
            temperature = 0
            power = 0
            for data in item['data']:
                if data['name'] == 'GPU Core' and data['type'] == 'Load':
                    load = data['value']
                elif data['name'] == 'GPU Power' and data['type'] == 'Power':
                    power = data['value']
                elif data['name'] == 'GPU Core' and data['type'] == 'Temperature':
                    temperature = data['value']
            props['gpu'].append({
                'name': item['name'],
                'id': item['id'],
                'load': load,
                'temperature': temperature,
                'power': power
            })
        elif item['type'] == 'ram':
            load = 0
            for data in item['data']:
                if data['name'] == 'Memory' and data['type'] == 'Load':
                    load = data['value']
            props['ram'].append({
                'name': item['name'],
                'id': item['id'],
                'load': load,
            })
        elif item['type'] == 'hdd':
            load = 0
            for data in item['data']:
                if data['name'] == 'Used Space' and data['type'] == 'Load':
                    load = data['value']
            props['hdd'].append({
                'name': item['name'],
                'id': item['id'],
                'load': load,
            })
    return props


class ReScan(Qt.QThread):
    def __init__(self, *args):
        super().__init__(*args)

    def run(self):
        handle.Reset()


s = [{'type-idx': 2, 'type': 'cpu', 'name': 'AMD Ryzen 7 4800H with Radeon Graphics',
      'data': [{'name': 'CPU Core #1', 'type': 'Load', 'value': 13.79311},
               {'name': 'CPU Core #2', 'type': 'Load', 'value': 8.620691},
               {'name': 'CPU Core #3', 'type': 'Load', 'value': 6.034482},
               {'name': 'CPU Core #4', 'type': 'Load', 'value': 6.034482},
               {'name': 'CPU Core #5', 'type': 'Load', 'value': 11.2069},
               {'name': 'CPU Core #6', 'type': 'Load', 'value': 10.34483},
               {'name': 'CPU Core #7', 'type': 'Load', 'value': 11.2069},
               {'name': 'CPU Core #8', 'type': 'Load', 'value': 15.51724},
               {'name': 'CPU Total', 'type': 'Load', 'value': 10.34483},
               {'name': 'CPU Package', 'type': 'Power', 'value': 13.85985},
               {'name': 'Bus Speed', 'type': 'Clock', 'value': 99.81716},
               {'name': 'CPU Core #1', 'type': 'Power', 'value': 0.8862876},
               {'name': 'CPU Core #2', 'type': 'Power', 'value': 0.449138},
               {'name': 'CPU Core #3', 'type': 'Power', 'value': 0.4518236},
               {'name': 'CPU Core #4', 'type': 'Power', 'value': 0.6302993},
               {'name': 'CPU Core #5', 'type': 'Power', 'value': 1.056057},
               {'name': 'CPU Core #6', 'type': 'Power', 'value': 0.8702093},
               {'name': 'CPU Core #7', 'type': 'Power', 'value': 0.8351391},
               {'name': 'CPU Core #8', 'type': 'Power', 'value': 1.620165},
               {'name': 'CPU Package', 'type': 'Temperature', 'value': 61.5},
               {'name': 'CPU Core #1', 'type': 'Clock', 'value': 4292.138},
               {'name': 'CPU Core #2', 'type': 'Clock', 'value': 4292.138},
               {'name': 'CPU Core #3', 'type': 'Clock', 'value': 1907.617},
               {'name': 'CPU Core #4', 'type': 'Clock', 'value': 1907.617},
               {'name': 'CPU Core #5', 'type': 'Clock', 'value': 1397.44},
               {'name': 'CPU Core #6', 'type': 'Clock', 'value': 1397.44},
               {'name': 'CPU Core #7', 'type': 'Clock', 'value': 1397.44},
               {'name': 'CPU Core #8', 'type': 'Clock', 'value': 1397.44},
               {'name': 'CPU Cores', 'type': 'Power', 'value': 6.799119}]},
     {'type-idx': 3, 'type': 'ram', 'name': 'Generic Memory',
      'data': [{'name': 'Memory', 'type': 'Load', 'value': 41.47804},
               {'name': 'Used Memory', 'type': 'Data', 'value': 6.3955},
               {'name': 'Available Memory', 'type': 'Data', 'value': 9.023502}]},
     {'type-idx': 5, 'type': 'gpu', 'name': 'AMD Radeon Graphics',
      'data': [{'name': 'GPU Core', 'type': 'Clock', 'value': 400.0},
               {'name': 'GPU Memory', 'type': 'Clock', 'value': 1600.0},
               {'name': 'GPU Core', 'type': 'Voltage', 'value': 0.001},
               {'name': 'GPU Core', 'type': 'Load', 'value': 3.0}]},
     {'type-idx': 4, 'type': 'gpu', 'name': 'NVIDIA GeForce RTX 2060',
      'data': [{'name': 'GPU Core', 'type': 'Temperature', 'value': 42.0},
               {'name': 'GPU Core', 'type': 'Clock', 'value': 1005.0},
               {'name': 'GPU Memory', 'type': 'Clock', 'value': 5500.99},
               {'name': 'GPU Shader', 'type': 'Clock', 'value': 0.0},
               {'name': 'GPU Core', 'type': 'Load', 'value': 14.0},
               {'name': 'GPU Frame Buffer', 'type': 'Load', 'value': 2.0},
               {'name': 'GPU Video Engine', 'type': 'Load', 'value': 0.0},
               {'name': 'GPU Bus Interface', 'type': 'Load', 'value': 8.0},
               {'name': 'GPU Memory Total', 'type': 'SmallData', 'value': 6144.0},
               {'name': 'GPU Memory Used', 'type': 'SmallData', 'value': 414.418},
               {'name': 'GPU Memory Free', 'type': 'SmallData', 'value': 5729.582},
               {'name': 'GPU Memory', 'type': 'Load', 'value': 6.745084},
               {'name': 'GPU Power', 'type': 'Power', 'value': 24.381},
               {'name': 'GPU PCIE Rx', 'type': 'Throughput', 'value': 24.41406},
               {'name': 'GPU PCIE Tx', 'type': 'Throughput', 'value': 991.2109}]},
     {'type-idx': 8, 'type': 'hdd', 'name': 'Generic Hard Disk',
      'data': [{'name': 'Used Space', 'type': 'Load', 'value': 28.84753}]},
     {'type-idx': 8, 'type': 'hdd', 'name': 'Generic Hard Disk',
      'data': [{'name': 'Used Space', 'type': 'Load', 'value': 36.64888}]}]
