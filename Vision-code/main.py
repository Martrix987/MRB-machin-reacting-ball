import serial

# Define the serial port and baud rate
port = 'COM3'  # Replace with the appropriate port name
baud_rate = 9600

# Create a serial object
ser = serial.Serial(port, baud_rate)

# Open the serial port
ser.open()

# Check if the serial port is open
if ser.is_open:
    print('Serial communication established.')

# Read data from the serial port
while True:
    data = ser.readline().decode().strip()
    print('Received data:', data)

# Close the serial port
ser.close()