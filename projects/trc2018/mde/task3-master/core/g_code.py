# -*- coding: utf-8 -*-

import yaml

with open("g_code_config.yml", 'r') as f:
    _g_code_config = f.read()

# G code data.
gcd = yaml.load(_g_code_config)

def generate_g_code(pos: str, is_from: bool):
    """G code command."""
    if '-' in pos:
        pos_s = pos.split('-', maxsplit=1)
        pos = pos_s[0]
        floor = int(pos_s[1]) - 1
    else:
        floor = 0
    print(pos)
    rotate_angel = gcd['t rotate'][pos]
    r_short: float = gcd['r elongation'][pos]['short']
    r_long: float = gcd['r elongation'][pos]['long']
    
    if pos in gcd['chamber']['up']:
        z_height: float = gcd['chamber']['upper']['height']
        z_low: float = gcd['chamber']['upper']['low']
    elif pos in gcd['chamber']['down']:
        z_height: float = gcd['chamber']['lower']['height']
        z_low: float = gcd['chamber']['lower']['low']

    # Is Cass A or Cass B.
    elif pos == "CassA":
        if is_from:
           z_height: float = gcd['cass']['CassA']['height'] + floor * 6.4 
           z_low: float = gcd['cass']['CassA']['low'] + floor * 6.4	
        else:
           z_height: float = gcd['cass']['CassA']['height'] + floor * 6.4
           z_low: float = gcd['cass']['CassA']['low'] + floor * 6.4	
    elif pos == "CassB":
        if is_from:
           z_height: float = gcd['cass']['CassB']['height'] + floor * 6.4 
           z_low: float = gcd['cass']['CassB']['low'] + floor * 6.4	
        else:
           z_height: float = gcd['cass']['CassB']['height'] + floor * 6.4
           z_low: float = gcd['cass']['CassB']['low'] + floor * 6.4	

    code = ""
    if is_from:
        code += f"P, R {r_short}, T {rotate_angel}, Z {z_low}, V 25;\n"
        code += f"P, R {r_long}, T {rotate_angel}, Z {z_low}, V 100;\n"
        code += f"P, R {r_long}, T {rotate_angel}, Z {z_height}, V 10;\n"
        code += "CO;\n"
        code += f"P, R {r_short}, T {rotate_angel}, Z {z_height}, V 100;\n"
    else:
        code += f"P, R {r_short}, T {rotate_angel}, Z {z_height}, V 25;\n"
        code += f"P, R {r_long}, T {rotate_angel}, Z {z_height}, V 100;\n"
        code += "CC;\n"
        code += f"P, R {r_long}, T {rotate_angel}, Z {z_low}, V 25;\n"
        code += f"P, R {r_short}, T {rotate_angel}, Z {z_low}, V 100;\n"

    return code

