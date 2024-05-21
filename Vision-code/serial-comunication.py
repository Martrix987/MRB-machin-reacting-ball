import serial
import time
import sys

port = 'COM4'  # Replace with your actual port
baud_rate = 9600

def connect_serial(port, baud_rate, retries=10):
    for i in range(retries):
        try:
            ser = serial.Serial(port, baud_rate, timeout=1)
            time.sleep(2)  # Wait for the connection to establish
            print(f"Connected to {port} at {baud_rate} baud rate")
            return ser
        except serial.SerialException as e:
            print(f"Attempt {i+1}: Error connecting to {port}: {e}")
            if i < retries - 1:
                time.sleep(0.5)  # Wait before retrying
            else:
                raise
    return None

try:
    ser = connect_serial(port, baud_rate)

    while True:
        # Send data to Arduino
        message = "Hello Arduino\n"
        ser.write(message.encode())
        print(f"Sent: {message.strip()}")

        # Wait for a response
        time.sleep(1)
        
        if ser.in_waiting > 0:
            response = ser.readline().decode('utf-8').strip()
            print(f"Arduino: {response}")
        time.sleep(1)
except serial.SerialException as e:
    print(f"Serial exception: {e}")
except KeyboardInterrupt:
    print("Program terminated by user")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
    print("Serial connection closed")
