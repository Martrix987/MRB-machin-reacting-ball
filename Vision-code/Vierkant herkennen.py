import cv2
import numpy as np

# Variabele voor het opslaan van de coördinaten van de muisklik
click_coords = None

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

def mouse_callback(event, x, y, flags, param):
    global click_coords
    if event == cv2.EVENT_LBUTTONDOWN:
        click_coords = (x, y)

def main():
    global click_coords
    cap = cv2.VideoCapture(0)  # Open the default camera

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    cv2.namedWindow('Frame')
    cv2.setMouseCallback('Frame', mouse_callback)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        squares = detect_squares(frame)
        if squares:
            square = squares[0]  # Neem de eerste gedetecteerde vierkant
            for i in range(4):
                cv2.line(frame, tuple(square[i][0]), tuple(square[(i + 1) % 4][0]), (0, 255, 0), 2)

            # Set the top-left corner of the square as (0,0)
            top_left = tuple(square[0][0])
            cv2.putText(frame, "0,0", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            if click_coords:
                # Check if the click is inside the square
                rect = cv2.boundingRect(square)
                if rect[0] <= click_coords[0] <= rect[0] + rect[2] and rect[1] <= click_coords[1] <= rect[1] + rect[3]:
                    # Calculate the coordinates within the square
                    local_x = click_coords[0] - top_left[0]
                    local_y = click_coords[1] - top_left[1]
                    cv2.circle(frame, click_coords, 5, (0, 0, 255), -1)
                    cv2.putText(frame, f"({local_x},{local_y})", click_coords, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()