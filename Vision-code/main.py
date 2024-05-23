import serial
import time
import sys

port = 'COM14'  # Replace with your actual port
baud_rate = 115200

def connect_serial(port, baud_rate, retries=10):
    for i in range(retries):
        try:
            ser = serial.Serial(port, baud_rate, timeout=1)
            time.sleep(1)  # Wait for the connection to establish
            print(f"Connected to {port} at {baud_rate} baud rate")
            return ser
        except serial.SerialException as e:
            print(f"Attempt {i+1}: Error connecting to {port}: {e}")
            if i < retries - 1:
                time.sleep(0.1)  # Wait before retrying
            else:
                raise
    return None

def receive_serial(ser):
    if ser.in_waiting > 0:
        try:
            data = ser.readline().decode('utf-8').strip()
            if data:
                print(f"Received: {data}")
        except Exception as e:
            print(f"Error receiving data: {e}")

if __name__ == "__main__":
    ser = connect_serial(port, baud_rate)
    if ser:
        while True:
            # Send data to Arduino
            # First send the coordinates of the objective
            # Second send the coordinates of the ball
            message = "x:15/y:15/x:55/y:55\n"
            ser.write(message.encode())
            print(f"Sent: {message.strip()}")
            time.sleep(1)  # Adjust this delay as needed

            # Receive and print data from Arduino
            receive_serial(ser)
