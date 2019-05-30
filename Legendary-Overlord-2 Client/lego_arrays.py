def set_dimmer_level(dimmer, level):
    return set_dimmer_levels([dimmer], [level])


def set_dimmer_levels(dimmers, levels):
    data = [1, len(dimmers)]
    for dimmer in dimmers:
        data.append(dimmer)
    data.append(0)
    data.append(len(levels))
    for level in levels:
        data.append(level)
    data.insert(0, len(data))
    return data


def set_dimmer_data(dimmers, all_data):
    if type(dimmers) != list:
        dimmers = [dimmers]
    data = [1, len(dimmers)]
    for dimmer in dimmers:
        data.append(dimmer)
    data.append(1)
    data.append(len(all_data))
    for datum in all_data:
        data.append(datum)
    data.insert(0, len(data))
    return data


def set_dimmer_function(dimmer, func):
    return set_dimmer_functions([dimmer], [func])


def set_dimmer_functions(dimmers, functions):
    data = [1, len(dimmers)]
    for dimmer in dimmers:
        data.append(dimmer)
    data.append(2)
    data.append(len(functions))
    for func in functions:
        data.append(func)
    data.insert(0, len(data))
    return data


def set_dimmer_property(dimmers, prop, values):
    if type(dimmers) != list:
        dimmers = [dimmers]
    if type(values) != list:
        values = [values]

    data = [1, len(dimmers)]

    for dimmer in dimmers:
        data.append(dimmer)

    data.append(3)
    data.append(property_name_to_id(prop))
    data.append(len(values))
    for value in values:
        data.append(value)
    data.insert(0, len(data))
    return data


def get_dimmer_property(dimmers, prop):
    if type(dimmers) != list:
        dimmers = [dimmers]

    data = [2, 3, property_name_to_id(prop), len(dimmers)]

    for dimmer in dimmers:
        data.append(dimmer)

    data.insert(0, len(data))
    return data


def property_name_to_id(prop):
    prop = str.lower(prop)
    if prop == 'pin':
        return 0
    elif prop == 'enabled':
        return 1
    elif prop == 'bipolar':
        return 2
    elif prop == 'inverse':
        return 3
    elif prop == 'method':
        return 4
