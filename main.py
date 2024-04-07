from pymodbus.client.sync import ModbusSerialClient
import serial.tools.list_ports

# Function to scan for Modbus devices
def scan_modbus_devices():
    modbus_devices = []

    # Get a list of serial ports
    ports = serial.tools.list_ports.comports()

    # Iterate over each port
    for port in ports:
        try:
            # Create a Modbus serial client for the port
            client = ModbusSerialClient(method='rtu', port=port.device, baudrate=9600)
            
            # Attempt to connect to the Modbus device
            if client.connect():
                # If connected, add the device information to the list
                modbus_devices.append({'port': port.device, 'description': port.description})
                client.close()
        except Exception as e:
            print(f"Error scanning port {port.device}: {e}")

    return modbus_devices

# Main function
def main():
    # Scan for Modbus devices
    modbus_devices = scan_modbus_devices()

    # Print the list of Modbus devices found
    if modbus_devices:
        print("Modbus devices found:")
        for device in modbus_devices:
            print(f"Port: {device['port']}, Description: {device['description']}")
    else:
        print("No Modbus devices found.")

if __name__ == "__main__":
    main()
