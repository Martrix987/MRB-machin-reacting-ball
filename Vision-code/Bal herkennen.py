import cv2
import numpy as np

# Start de videostream van de webcam
cap = cv2.VideoCapture(0)  # Hier 0 staat voor de index van de webcam. Als je meerdere webcams hebt, kun je een andere index gebruiken.

while True:
    # Lees frames van de videostream
    ret, frame = cap.read()
    if not ret:
        break

    # Converteer het frame naar het HSV-kleurschema
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definieer het groene kleurbereik in HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    # Maak een masker met pixels binnen het groene kleurbereik
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Vind contouren van het groene object
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Als er contouren zijn gevonden
    if contours:
        # Zoek de grootste contour (het groene object)
        largest_contour = max(contours, key=cv2.contourArea)

        # Bepaal het midden van de contour
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        # Teken een cirkel op het midden van het groene object
        cv2.circle(frame, (cX, cY), 7, (0, 255, 0), -1)

        # Toon de coördinaten
        cv2.putText(frame, f'({cX}, {cY})', (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Toon het frame met de gemarkeerde contour en coördinaten
    cv2.imshow('Object tracking', frame)

    # Stop de loop als 'q' wordt ingedrukt
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop de videostream en sluit alle vensters
cap.release()
cv2.destroyAllWindows()
