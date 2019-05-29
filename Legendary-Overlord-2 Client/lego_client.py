import lego_serial
import lego_arrays

print('Welcome to the Legendary Overlord 2 PC interface!')

ser = ''


def segment_string(string, delimiter, type='RAW'):
    """Takes a string and separates it into pieces at 'delimiter' characters. Returns a list of pieces."""
    segment_list = []
    current_seg = ''
    for char in string:
        if char == delimiter:
            segment_list.append(current_seg)
            current_seg = ''
        else:
            current_seg = current_seg + char
    if current_seg != '':
        segment_list.append(current_seg)
    if type != 'RAW':
        if type == 'NUM':
            newList = []
            for entry in segment_list:
                newList.append(int(entry))
            segment_list = newList
        elif type == 'BOOL':
            newList = []
            for entry in segment_list:
                if str.lower(entry) == 'false':
                    newList.append(False)
                else:
                    newList.append(True)
            segment_list = newList
        elif type == 'BOOLN':
            newList = []
            for entry in segment_list:
                if str.lower(entry) == 'false':
                    newList.append(0)
                else:
                    newList.append(1)
            segment_list = newList
    return segment_list


port_given = False


def interpret_input(line_in):
    global port_given
    global ser
    try:
        line_in = str.lower(line_in)
        params = segment_string(line_in, ' ')
        if len(params) > 0:
            cmd = params[0]
            params.pop(0)
        else:
            cmd = 'none'
        if cmd == 'help' or cmd == '?':
            if len(params) == 0:
                return 'Type "help [cmd]" for more information about an entry.\r\n' \
                       'The following commands are currently available:\r\n\r\n' \
                      'Connect - Attempt connection to device\r\n' \
                      'Dimmer - Dimmer channels on LegO 2\r\n' \
                      'Disconnect - End the serial connection to the device\r\n' \
                      'Exit/Quit - Close the program\r\n' \
                      'Help - Display this menu\r\n' \
                      'Port - Set the serial port to use\r\n'
            else:
                info = params[0]
                if info == 'dimmer':
                    return 'Help for Dimmer command:\r\n\r\n' \
                           'Usage - Dimmer [indices] [set,get] [level,property,function,data] (args)\r\n' \
                          'Contacts the Lighting Master Control portion of LegO 2\r\n'
                elif info == 'port':
                    return 'Help for Port command:\r\n\r\n' \
                           'Usage - Port [port name str]\r\n'
                elif info == 'connect':
                    return 'Help for Connect command:\r\n\r\n' \
                           'Usage - Connect [OPTIONAL - port name str]\r\n' \
                           'Open the serial connection on the specified port.'
                else:
                    return 'No additional help is available for this command.\r\n'
        elif cmd == 'dimmer':
            if not port_given:
                return 'The serial connection has not been initialized.'
            else:
                targetDimmers = segment_string(params[0], ',', type='NUM')
                if params[1] == 'set':
                    if params[2] == 'level':
                        levels = segment_string(params[3], ',', type='NUM')
                        ser.send_data(lego_arrays.set_dimmer_levels(targetDimmers, levels))
                    elif params[2] == 'pin':
                        values = segment_string(params[3], ',', type='NUM')
                        ser.send_data(lego_arrays.set_dimmer_property(targetDimmers, 'pin', values))
                    elif params[2] == 'enabled':
                        values = segment_string(params[3], ',', type='BOOLN')
                        ser.send_data(lego_arrays.set_dimmer_property(targetDimmers, 'enabled', values))
                    elif params[2] == 'bipolar':
                        values = segment_string(params[3], ',', type='BOOLN')
                        ser.send_data(lego_arrays.set_dimmer_property(targetDimmers, 'bipolar', values))
                    elif params[2] == 'inverse':
                        values = segment_string(params[3], ',', type='BOOLN')
                        ser.send_data(lego_arrays.set_dimmer_property(targetDimmers, 'inverse', values))
                    elif params[2] == 'method':
                        values = segment_string(params[3], ',', type='NUM')
                        ser.send_data(lego_arrays.set_dimmer_property(targetDimmers, 'method', values))
                    elif params[2] == 'function':
                        values = segment_string(params[3], ',', type='NUM')
                        ser.send_data(lego_arrays.set_dimmer_functions(targetDimmers, values))
                    elif params[2] == 'data':
                        data = segment_string(params[3], ',', type='NUM')
                        ser.send_data(lego_arrays.set_dimmer_data(targetDimmers, data))
                    else:
                        return 'Unknown target. See "help Dimmer"'
                else:
                    return 'Unknown operation. See "help Dimmer"'
        elif cmd == 'exit' or cmd == 'quit':
            return 'exit'
        elif cmd == 'port':
            port_given = True
            ser = lego_serial.LegoSerial(params[0])
        elif cmd == 'connect':
            if len(params) > 0:
                port_given = True
                ser = lego_serial.LegoSerial(params[0])
                ser.open_serial()
            elif not port_given:
                    return 'You must specify a port before connecting. Use PORT [port name]'
            else:
                ser.open_serial()
        elif cmd == 'disconnect':
            ser.close_serial()
        else:
            return 'Unknown command. Type "help" for a help dialogue.'
    except (OSError, IndexError):
        return 'Given ' + str(len(params)) + ' parameters. More expected by command.'
        pass
    except ValueError:
        return 'Parameter(s) of the incorrect data type.'
        pass
