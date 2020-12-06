import clr
from utils.utils import join_path

clr.AddReference(join_path("utils/OpenHardwareMonitorLib.dll"))
sensor_types = ['Voltage', 'Clock', 'Temperature', 'Load', 'Fan', 'Flow',
                'Control', 'Level', 'Factor', 'Power', 'Data', 'SmallData', 'Throughput']
hardware_types = ['Mainboard', 'SuperIO', 'cpu', 'gpu', 'gpu', 'TBalancer', 'Heatmaster', 'hdd', 'ssd']

from OpenHardwareMonitor import Hardware

handle = Hardware.Computer()
handle.CPUEnabled = True
handle.RAMEnabled = True
handle.GPUEnabled = True
handle.HDDEnabled = True
handle.Open()


def get_hardware_info():
    lis = []
    for i in handle.Hardware:
        i.Update()
        if i.Sensors:
            obj = {
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
    return lis
