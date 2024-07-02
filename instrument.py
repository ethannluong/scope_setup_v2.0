import pyvisa
import collections
import json
from typing import TypedDict, Any
from pyvisa.errors import VisaIOError
import functools
import numpy as np
from pathlib import Path

_RM = pyvisa.ResourceManager('@py')

resource_lst = _RM.list_resources()

if len(resource_lst) < 1:
    _RM = pyvisa.ResourceManager()
    resource_lst = _RM.list_resources()


class CommandMap(TypedDict, total=True):
    set_attenuation: str
    set_voltage: str
    set_acquisition: str
    set_cursor: str
    set_positive: str
    set_negative: str
    set_measurement: str
    axis_commands: dict


def closest(lst, target):
    """returns the value closest to the given value in the given list"""
    closest_value = lst[0]
    min_diff = abs(target - closest_value)

    for value in lst:
        diff = abs(target - value)
        if diff < min_diff:
            min_diff = diff
            closest_value = value

    return closest_value


def import_command_maps(filepath: str) -> dict[str, dict[str, Any]]:
    with open(filepath, 'r') as file:
        return json.load(file)


def process_command_maps(maps: dict[str, dict[str, Any]]) -> dict[str, CommandMap]:
    command_maps = {}

    for n, m in sorted(maps.items(), key=lambda p: p[1].get('derived') or ''):

        derived = m.pop('derived', None)
        if not derived:
            if CommandMap.__required_keys__.difference(m):
                raise ValueError(f"invalid structure of loaded command map {n!r}")
            command_maps[n] = m
            continue

        try:
            parent_map = command_maps[derived]
        except KeyError:
            raise ValueError(
                f"loaded command map {n!r}'s parent map is not defined"
            )
        command_maps[n] = collections.ChainMap(m, parent_map)

    return command_maps


class Instrument:
    def __init__(self):
        self.address = None
        self.is_connected = False
        self.name = ''
        self.my_instrument = None
        self.polarity = None
        self.voltage = None
        self.size = None
        self.waveform = None
        self.ip = None
        self.tr = None
        self.fwhm = None
        self.ip2 = None
        self.command_map = {}

    def setup_helper(self):
        print('connecting')
        running = True
        while running:
            try:
                self.my_instrument = _RM.open_resource(self.address)
                if self.my_instrument is not None:
                    self.is_connected = True
                    print('connected')
                    running = False
            except VisaIOError:
                print('trying again')
                continue

    def setup(self):
        if self.is_connected:
            return
        self.setup_helper()

    @staticmethod
    def _scope_command(fn):

        @functools.wraps(fn)
        def method(self, level=None):
            items = self.command_map.items()
            for key, item in items:
                key = key
            cmd = self.command_map[fn.__name__]
            if 'get' not in fn.__name__:
                if level is not None:
                    self.set_object_voltage(level)
                    cmd = cmd[:-4] + level + cmd[-4:]
                self.my_instrument.write(cmd)
            elif 'get' in fn.__name__:
                return self.my_instrument.query(cmd)

        return method

    def set_map(self, json_file: str, key: str):
        maps = process_command_maps(import_command_maps(json_file))
        self.command_map = maps[key]

    def set_name(self, name: str):
        self.name = name

    def connect(self):
        lst = _RM.list_resources()
        scope_id = ''
        for item in lst:
            try:
                self.address = item
                self.my_instrument = _RM.open_resource(item)
                scope_id = self.my_instrument.query("ID?")
                scope_id = scope_id.split(',')[0]
                scope_id = scope_id.split('/')[-1]
                break

            except VisaIOError:
                pass

        json_file_path = Path(__file__).parent / 'commands.json'
        if not json_file_path.exists():
            json_file_path = json_file_path.parent.parent.parent / 'commands.json'

        self.set_name(scope_id)
        self.set_map(json_file_path, self.name)
        self.set_attenuation()
        self.set_acquisition()
        self.set_cursor()
        self.set_measurement()
        print(self.address, self.name, self.command_map)

    @_scope_command
    def set_attenuation(self): ...

    @_scope_command
    def set_acquisition(self): ...

    @_scope_command
    def set_cursor(self): ...

    @_scope_command
    def set_measurement(self): ...

    @_scope_command
    def set_positive(self): ...

    @_scope_command
    def set_negative(self): ...

    @_scope_command
    def set_voltage(self, level): ...

    @_scope_command
    def set_encoding(self): ...

    @_scope_command
    def get_measure1(self): ...

    @_scope_command
    def get_measure2(self): ...

    @_scope_command
    def get_measure3(self): ...

    def get_fwhm(self):
        axes_commands = self.command_map['axis_commands']
        self.my_instrument.write(axes_commands['header'])
        self.my_instrument.write(axes_commands['source'])
        self.my_instrument.write(axes_commands['encoding'])
        self.my_instrument.write(axes_commands['width'])
        self.my_instrument.write(axes_commands['start'])
        self.my_instrument.write(axes_commands['stop'])
        record_length = int(self.my_instrument.query(axes_commands['record']))
        self.my_instrument.write(axes_commands['stop'].format(record_length))

        xinc = float(self.my_instrument.query(axes_commands['xinc']))
        xzero = float(self.my_instrument.query(axes_commands['xzero']))
        pt_off = float(self.my_instrument.query(axes_commands['pt_off']))

        ymult = float(self.my_instrument.query(axes_commands['ymult']))
        yzero = float(self.my_instrument.query(axes_commands['yzero']))
        yoff = float(self.my_instrument.query(axes_commands['yoff']))

        self.my_instrument.write(axes_commands['curve'])

        rawData = self.my_instrument.read_binary_values(datatype='b', is_big_endian=False, container=np.ndarray, header_fmt='ieee', expect_termination=True)
        dataLen = len(rawData)

        t0 = (-pt_off * xinc) + xzero
        xvalues = np.ndarray(dataLen, float)
        yvalues = np.ndarray(dataLen, float)
        for i in range(0, dataLen):
            xvalues[i] = t0 + xinc * i  # Create timestamp for the data point
            yvalues[i] = float(rawData[i] - yoff) * ymult + yzero  # Convert raw ADC value into a floating point value

        max_ip = max(yvalues)
        min_ip = min(yvalues)

        begin = []
        end = []
        begx = []
        endx = []

        if max(yvalues) > abs(min(yvalues)):
            target = max_ip / 2

            ip_index = np.where(yvalues == max(yvalues))[0][0]

            for i in range(0, dataLen):
                if i < ip_index:
                    begin.append(yvalues[i])
                    begx.append(xvalues[i])
                else:
                    end.append(yvalues[i])
                    endx.append(xvalues[i])

            pos1 = begin.index(closest(begin, target))
            pos2 = end.index(closest(end, target))

            fwhm = endx[pos2] - begx[pos1]
            fwhm = abs(round(fwhm * 1E12))
        else:
            target = min_ip / 2

            ip_index = np.where(yvalues == min(yvalues))[0][0]

            for i in range(0, dataLen):
                if i > ip_index:
                    begin.append(yvalues[i])
                    begx.append(xvalues[i])
                else:
                    end.append(yvalues[i])
                    endx.append(xvalues[i])

            pos2 = begin.index(closest(begin, target))
            pos1 = end.index(closest(end, target))

            fwhm = begx[pos2] - endx[pos1]
            fwhm = abs(round(fwhm * 1E12))

        return fwhm

    def set_size(self, size: str):
        self.size = size

    def set_object_voltage(self, level: str):
        volt_dict = {
            "500": "125",
            "1000": "250",
            "2000": "500",
            "5000": "750",
            "10000": "1000"
        }
        self.voltage = volt_dict[level]

    def set_object_polarity(self, polarity: str):
        self.polarity = polarity

    def set_polarity_helper(self, polarity: str):
        if polarity == "positive":
            self.set_positive()
            self.polarity = polarity
        elif polarity == "negative":
            self.set_negative()
            self.polarity = polarity

    def get_measurements(self):
        min_ip = float(self.get_measure1())
        self.ip = round(float(self.get_measure3()) * 10, 3)
        self.tr = round(float(self.get_measure2()) * 1e+12, 3)
        self.fwhm = round(float(self.get_fwhm()), 3)
        self.ip2 = round((abs(min_ip) / self.ip) * 1e+3, 3)
