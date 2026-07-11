from pymodbus.client import ModbusSerialClient

class ModbusClient:
    def __init__(self):
        self.client = None
    
    def connect(self, port="COM1", baudrate=115200):
        self.client = ModbusSerialClient(port=port, baudrate=baudrate, timeout=2)
        return self.client.connect()
    
    def is_connected(self):
        return self.client and self.client.is_socket_open()
    
    def read_holding_registers(self, address, count=1, slave=15):
        return self.client.read_holding_registers(address, count, slave=slave)
    
    def write_register(self, address, value, slave=15):
        return self.client.write_register(address, value, slave=slave) 