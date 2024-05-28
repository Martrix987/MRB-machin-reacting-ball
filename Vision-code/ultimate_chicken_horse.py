import serial
import time
import cv2
import numpy as np

port = 'COM14'  # Replace with your actual port
baud_rate = 115200

# Connect to Arduino
def connect_serial(port, baud_rate, retries=50):
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

# Receive data from Arduino
def receive_serial(ser):
    if ser.in_waiting > 0:
        try:
            
            data = ser.readline().decode('utf-8').strip()
            if data:
                print(f"Received: {data}")
        except Exception as e:
            print(f"Error receiving data: {e}")

# Detect squares in the frame
def detect_squares(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    squares = []
    for cnt in contours:
        epsilon = 0.04 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        if len(approx) == 4 and cv2.isContourConvex(approx):
            (x, y, w, h) = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            if 0.9 <= aspect_ratio <= 1.1:  # Check if the contour is close to a square
                squares.append(approx)

    return squares

# Mouse callback function
click_coords = None
def mouse_callback(event, x, y, flags, param):
    global click_coords
    if event == cv2.EVENT_LBUTTONDOWN:
        click_coords = (x, y)

# Main function
def main():
    global click_coords
    ser = connect_serial(port, baud_rate)
    if not ser:
        print("Error: Could not connect to Arduino.")
        return

    cap = cv2.VideoCapture(0)  # Start video capture from webcam

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    cv2.namedWindow('Object Tracking and Square Detection')
    cv2.setMouseCallback('Object Tracking and Square Detection', mouse_callback)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        squares = detect_squares(frame)

        if squares:
            square = squares[0]
            startpoint = square[0][0]

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"]) - startpoint[0]
                cY = int(M["m01"] / M["m00"]) - startpoint[1]
            else:
                cX, cY = 0, 0
            # cv2.circle(frame, (cX, cY), 7, (0, 255, 0), -1)
            # cv2.putText(frame, f'({cX}, {cY})', (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Use the clicked coordinates as destination if available
            if click_coords:
                destX = click_coords[0] - startpoint[0]
                destY = click_coords[1] - startpoint[1]
            else:
                destX, destY = 0, 0  # Default destination if no click detected

            # Send coordinates to Arduino
            message = f"x:{destX}/y:{destY}/x:{cX}/y:{cY}\n"
            ser.write(message.encode())
            # print(f"Sent: {message.strip()}")

        if squares:
            square = squares[0]
            for i in range(4):
                cv2.line(frame, tuple(square[i][0]), tuple(square[(i + 1) % 4][0]), (0, 255, 0), 2)
            top_left = tuple(square[0][0])
            cv2.putText(frame, "0,0", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            if click_coords:
                rect = cv2.boundingRect(square)
                if rect[0] <= click_coords[0] <= rect[0] + rect[2] and rect[1] <= click_coords[1] <= rect[1] + rect[3]:
                    local_x = click_coords[0] - top_left[0]
                    local_y = click_coords[1] - top_left[1]
                    # cursor-mouse-red
                    cv2.circle(frame, click_coords, 5, (0, 0, 255), -1)
                    # cv2.putText(frame, f"({local_x},{local_y})", click_coords, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow('Object Tracking and Square Detection', frame)

        # Receive and print data from Arduino
        # receive_serial(ser)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    ser.close()

if __name__ == "__main__":
    main()
