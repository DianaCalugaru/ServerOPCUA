import RPi.GPIO as GPIO
import time
import cv2

def handle_switch(channel, SWITCH_PIN, SwitchValue, camera, camera_variable, face_cascade, out):
    if GPIO.input(SWITCH_PIN) == GPIO.LOW:
        print('Button Pressed')
        SwitchValue.set_value(1)
        start_time = time.time()  # set 'start_time' to the current time
        while (time.time() - start_time) < 5:
            # Capturează un cadru din camera
            ret, frame = camera.read()

            # Verificați dacă cadru a fost capturat corect
            if not ret:
                print("Eroare la capturarea cadrelor.")
                break

            # Detectați fețele în cadrul cadrelor
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                # S-a detectat cel puțin o față
                camera_variable.set_value(1)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    face_image = frame[y:y + h, x:x + w]
                    cv2.imwrite('face.jpg', face_image)
            else:
                # Nu s-a detectat nicio față
                camera_variable.set_value(0)

            # Afizați cadru
            cv2.imshow('Camera', frame)

            # Înregistrați cadru în video
            out.write(frame)

            # Convertiți matricea în șir de caractere
            frame_byte = frame.tobytes()

            # Actualizați valoarea variabilei OPC UA cu șirul de caractere reprezentând frame-ul

            # Așteptați apăsarea tastei 'q' pentru a opri înregistrarea și serverul OPC UA
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                # Oprește înregistrarea video și eliberează resursele
        out.release()
        camera.release()

        # Închideți toate ferestrele deschise
        cv2.destroyAllWindows()

    else:
        SwitchValue.set_value(0)
        out.release()
        camera.release()
        cv2.destroyAllWindows()
