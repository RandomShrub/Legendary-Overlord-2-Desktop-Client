from tkinter import *
import glob
import serial
import lego_serial as ls
import lego_command_line as lcl

ser = ls.LegoSerial('none')

port_list = []

def serial_ports():
    """ Lists serial port names

        This was made by Stackoverflow user Thomas (https://stackoverflow.com/users/300783/thomas)

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def update_port_list():
    global port_menu
    global port_list
    port_menu.delete(0, 256)
    port_list = serial_ports()
    if ser.ser.is_open:
        port_list.insert(0, selected_port.get())
    port_list.sort()
    for port in port_list:
        port_menu.add_radiobutton(label=port, command=port_changed, value=port, variable=selected_port)


def attempt_connect():
    connectionStatus.set('Status: Connecting...')
    ser.ser.port = selected_port.get()
    ser.open_serial()
    if ser.ser.is_open:
        connectionStatus.set('Status: Checking connection...')
        if ser.get_response([1, 0], sendDelay=2) == [1, 6]:
            connectionStatus.set('Status: Connected!')
        else:
            connectionStatus.set('Status: Unknown device.')
    else:
        connectionStatus.set('Status: Connection failed!')


def disconnect_serial():
    if ser.ser.is_open:
        ser.close_serial()
        connectionStatus.set('Status: Disconnected')


def port_changed():
    disconnect_serial()
    print(selected_port.get())


def open_terminal():

    cmd_ln = lcl.CommandLine()

    def term_send_line():
        reply = cmd_ln.interpret_input(entry.get())

        if reply == 'exit':
            term.destroy()

        lines = history_str.get().count('\n') + 1
        if lines >= 10:
            history_str.set('')

        if len(history_str.get()) == 0:
            history_str.set(history_str.get() + reply)
        else:
            history_str.set(history_str.get() + '\r\n' + reply)
        entry.set('')

    term = Toplevel(root)

    term.title('LegO 2 Terminal')

    history_str = StringVar()
    history_str.set('')
    entry = StringVar()

    history_box = Label(term, textvariable=history_str, anchor=NW, bg='white', fg='black', justify=LEFT, relief=SUNKEN)
    entry_box = Entry(term, textvariable=entry)
    submit_button = Button(term, text='Send', command=term_send_line)

    history_box.config(height=20)
    entry_box.config(width=100)

    history_box.grid(row=0, column=0, sticky=N+S+E+W, columnspan=2, padx=2)
    entry_box.grid(row=1, column=0, padx=2, sticky=E+W)
    submit_button.grid(row=1, column=1, padx=2, sticky=E)

    term.mainloop()


def activate_dimmer():
    global active_dimmer
    try:
        index_int = int(index_text.get())
    except ValueError:
        index_int = -1
        index_text.set(0)
        pass

    if 0 <= index_int <= 255:
        active_dimmer = index_int
        dimmerStatus.set('Active Dimmer: ' + str(active_dimmer))


def save_dimmer():
    print('Saving, todo')


def blink_test():
    print('Blink test, todo')


port_list = serial_ports()

active_dimmer = -1

root = Tk()


root.title('Legendary Overlord 2 Configurator')

selected_port = StringVar()
selected_port.set(port_list[0])

connectionStatus = StringVar()
connectionStatus.set('Status: Not connected')

dimmerStatus = StringVar()
dimmerStatus.set('No active dimmer')

enabled_var = IntVar()
bipolar_var = IntVar()
inverse_var = IntVar()

method_text = StringVar()
pin_text = StringVar()

# Top menu bar construction

menu = Menu(root)
root.config(menu=menu)

serial_menu = Menu(menu, tearoff=0)
port_menu = Menu(serial_menu, tearoff=0)
tools_menu = Menu(menu, tearoff=0)

menu.add_cascade(label='Device', menu=serial_menu)
serial_menu.add_command(label='Connect', command=attempt_connect)
serial_menu.add_command(label='Disconnect', command=disconnect_serial)
serial_menu.add_separator()

serial_menu.add_command(label='Refresh', command=update_port_list)
serial_menu.add_cascade(label='Port', menu=port_menu)
update_port_list()

menu.add_cascade(label='Tools', menu=tools_menu)
tools_menu.add_command(label='Terminal', command=open_terminal)

# End menu bar. Begin main elements

index_text = StringVar()
dimmer_text = StringVar()


edit_dimmers_label = Label(root, text='Edit Dimmers', relief=SUNKEN)
dim_id_label = Label(root, text='Dimmer')
pin_label = Label(root, text='Pin')
method_label = Label(root, text='Method')


index_spinner = Spinbox(root, from_=0, to=127, width=8, textvariable=index_text)
pin_spinner = Spinbox(root, from_=0, to=53, width=8, textvariable=pin_text)
method_spinner = Spinbox(root, from_=0, to=15, width=8, textvariable=method_text)

activate_button = Button(root, text='Activate', command=activate_dimmer)

save_button = Button(root, text='Save', command=save_dimmer)

test_button = Button(root, text='Blink', command=blink_test)

enabled_cb = Checkbutton(root, text='Enabled', variable=enabled_var)
bipolar_cb = Checkbutton(root, text='Bipolar', variable=bipolar_var)
inverse_cb = Checkbutton(root, text='Inverse', variable=inverse_var)

edit_dimmers_label.grid(row=0, columnspan=4, sticky=W+E+S)

dim_id_label.grid(row=1, padx=5, pady=5, sticky=NW)
index_spinner.grid(row=2, padx=5, pady=5, sticky=NW)
activate_button.grid(row=3, padx=5, pady=5, sticky=W+E+S)

enabled_cb.grid(row=1, column=3, pady=5, sticky=NW)
bipolar_cb.grid(row=2, column=3, pady=5, sticky=NW)
inverse_cb.grid(row=3, column=3, pady=5, sticky=NW)

pin_label.grid(row=1, column=1, padx=5, pady=5, sticky=NW)
pin_spinner.grid(row=2, column=1, padx=5, pady=5, sticky=NW)
save_button.grid(row=3, column=1, padx=5, pady=5, sticky=W+E+S)

method_label.grid(row=1, column=2, padx=5, pady=5, sticky=NW)
method_spinner.grid(row=2, column=2, padx=5, pady=5, sticky=NW)
test_button.grid(row=3, column=2, padx=5, pady=5, sticky=W+E+S)


# Status bar

connection_status = Label(root, textvariable=connectionStatus, bd=1, relief=SUNKEN, anchor=W)
port_status = Label(root, textvariable=selected_port, bd=1, relief=SUNKEN, anchor=W)
dimmer_status = Label(root, width=15, textvariable=dimmerStatus, bd=1, relief=SUNKEN, anchor=W)

connection_status.grid(row=4, columnspan=2, sticky=W+E+S)
port_status.grid(row=4, column=2, columnspan=2, sticky=W+E+S)
dimmer_status.grid(row=4, column=3, columnspan=1, sticky=W+E+S)


root.mainloop()
