def find_port():
    """Doesn't work on Windows anymore"""
    if platform == 'win32':
        ports = list(serial.tools.list_ports.comports())
        if len(ports) == 1: return str(ports[0][0])
        else: return str(None)
    if platform == 'darwin':
        ports = list(glob.glob('/dev/tty.usbmodem*'))
        if len(ports) == 1: return str(ports[0])
        else: return str(None)
