from __future__ import print_function
import os
import sys
import pcbnew
import numpy as np
import pprint


def inch_to_nanometer(value):
    return (value*25.4)*1e6

def nanometer_to_inch(value):
    return value/(25.4*1.e6)

def get_led_data(param):
    led_num = 1
    array_param_list = [param['array0'], param['array1']]
    led_pos_data = {}
    for array_param in array_param_list:
        x_vals = array_param['step_x']*np.arange(array_param['num_x']) + array_param['x0']
        y_vals = array_param['step_y']*np.arange(array_param['num_y']) + array_param['y0']
        for x in x_vals:
            for y in y_vals:
                ref = 'D{}'.format(led_num)
                led_pos_data[ref] = {'angle': array_param['angle'], 'x': x, 'y': y}
                led_num += 1
    return led_pos_data

def print_module_info(module):
    ref = module.GetReference()
    pos = module.GetPosition()
    x = nanometer_to_inch(pos.x)
    y = nanometer_to_inch(pos.y)
    angle = 0.1*module.GetOrientation()
        
    print('  R: {}'.format(ref))
    print('  X: {}'.format(x))
    print('  Y: {}'.format(y))
    print('  A: {}'.format(angle))
    print()


# ---------------------------------------------------------------------------------------

param = {
        'array0': {
            'num_x': 10, 

            'num_y': 10,
            'x0': 2.5,
            'y0': 2.5,
            'step_x': 1.0,
            'step_y': 1.0,
            'angle': 0,
            },
        'array1': {
            'num_x': 9,
            'num_y': 9,
            'x0': 3.0,
            'y0': 3.0,
            'step_x': 1.0,
            'step_y': 1.0,
            'angle': 0,
            }
        }


filename = sys.argv[1]

print()
print('loading pcb: {}'.format(filename))
print()
pcb = pcbnew.LoadBoard(filename)
print()
print('done')
print()

## Get data for placing LEDs
led_pos_data_dict = get_led_data(param)
if 0:
    print('led_data')
    print()
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(led_pos_data_dict)
    print()

print('modules')
print()

for module in pcb.GetModules():

    ref_str = str(module.GetReference())

    try:
        led_pos_data = led_pos_data_dict[ref_str]
    except KeyError:
        continue

    print_module_info(module)5

    # Move to new position
    pos = module.GetPosition()
    angle = 0.1*module.GetOrientation()
    x_new = led_pos_data['x']
    y_new = led_pos_data['y']
    angle_new = led_pos_data['angle']
    pos.x = int(inch_to_nanometer(x_new))
    pos.y = int(inch_to_nanometer(y_new))
    module.SetPosition(pos)
    module.SetOrientation(10.0*angle_new)

    print_module_info(module)

pathname, basename = os.path.split(filename)
new_basename = 'mod_{}'.format(basename)
new_filename = os.path.join(pathname,new_basename)

pcb.Save(new_filename)

        

