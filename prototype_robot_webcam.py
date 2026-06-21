import cv2
import time
import urllib.request
from pathlib import Path


import serial
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision




# =========================================================
# 1. RÉGLAGES
# =========================================================


PORT_ARDUINO = "COM3"  # change COM3 par le port de ton Arduino
VITESSE_SERIAL = 9600


CAMERA_ID = 0


ANGLE_MIN = 0
ANGLE_MAX = 180


# Plus grand = mouvement plus doux
LISSAGE = 0.18


# Envoie les ordres toutes les X secondes
DELAI_ENVOI = 0.04




# =========================================================
# 2. MODÈLE MEDIAPIPE
# =========================================================


MODEL_PATH = "hand_landmarker.task"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"


if not Path(MODEL_PATH).exists():
    print("Téléchargement du modèle mains...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Modèle téléchargé.")


base_options = python.BaseOptions(model_asset_path=MODEL_PATH)


options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)


detecteur_mains = vision.HandLandmarker.create_from_options(options)




# =========================================================
# 3. CONNEXION ARDUINO
# =========================================================


try:
    arduino = serial.Serial(PORT_ARDUINO, VITESSE_SERIAL, timeout=1)
    time.sleep(2)
    print("Arduino connecté sur", PORT_ARDUINO)


except Exception as e:
    print("Erreur : impossible de connecter l'Arduino.")
    print("Vérifie le port COM.")
    print(e)
    exit()




# =========================================================
# 4. FONCTIONS
# =========================================================


def convertir_y_en_angle(y, hauteur):
    """
    y = position verticale du doigt dans l'image.


    En OpenCV :
    y = 0 en haut
    y = hauteur en bas


    Ici :
    doigt en haut -> angle 180
    doigt en bas  -> angle 0
    """
    ratio = 1 - (y / hauteur)
    angle = int(ANGLE_MIN + ratio * (ANGLE_MAX - ANGLE_MIN))
    return max(ANGLE_MIN, min(ANGLE_MAX, angle))




def lisser_angle(angle_actuel, angle_cible):
    return int(angle_actuel + (angle_cible - angle_actuel) * LISSAGE)




def envoyer_angles(a1, a2, a3):
    commande = f"{a1},{a2},{a3}\n"
    arduino.write(commande.encode())




def doigt_leve(points, tip, pip):
    return points[tip][1] < points[pip][1]




def main_ouverte(points):
    index = doigt_leve(points, 8, 6)
    majeur = doigt_leve(points, 12, 10)
    annulaire = doigt_leve(points, 16, 14)
    auriculaire = doigt_leve(points, 20, 18)


    return index and majeur and annulaire and auriculaire




# =========================================================
# 5. WEBCAM
# =========================================================


webcam = cv2.VideoCapture(CAMERA_ID)


angle1 = 90
angle2 = 90
angle3 = 90


dernier_envoi = time.time()


print("Programme lancé.")
print("Index = moteur 1")
print("Majeur = moteur 2")
print("Pouce = moteur 3")
print("Main ouverte = pause")
print("Q = quitter")




# =========================================================
# 6. BOUCLE PRINCIPALE
# =========================================================


while True:
    succes, frame = webcam.read()


    if not succes:
        print("Erreur webcam.")
        break


    frame = cv2.resize(frame, (640, 480))
    frame = cv2.flip(frame, 1)


    hauteur, largeur, _ = frame.shape


    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    image_mediapipe = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=image_rgb
    )


    resultats = detecteur_mains.detect(image_mediapipe)


    if resultats.hand_landmarks:
        landmarks = resultats.hand_landmarks[0]


        points = []


        for lm in landmarks:
            x = int(lm.x * largeur)
            y = int(lm.y * hauteur)
            points.append((x, y))


        # Points importants
        pouce = points[4]
        index = points[8]
        majeur = points[12]


        # Dessin sur l'écran
        cv2.circle(frame, index, 12, (255, 0, 0), -1)
        cv2.circle(frame, majeur, 12, (0, 255, 255), -1)
        cv2.circle(frame, pouce, 12, (0, 255, 0), -1)


        cv2.putText(frame, "Index = M1", (index[0] + 10, index[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)


        cv2.putText(frame, "Majeur = M2", (majeur[0] + 10, majeur[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)


        cv2.putText(frame, "Pouce = M3", (pouce[0] + 10, pouce[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


        if main_ouverte(points):
            cv2.putText(frame, "PAUSE - main ouverte", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


        else:
            # Convertir les positions des doigts en angles
            cible1 = convertir_y_en_angle(index[1], hauteur)
            cible2 = convertir_y_en_angle(majeur[1], hauteur)
            cible3 = convertir_y_en_angle(pouce[1], hauteur)


            # Lissage pour éviter les mouvements brusques
            angle1 = lisser_angle(angle1, cible1)
            angle2 = lisser_angle(angle2, cible2)
            angle3 = lisser_angle(angle3, cible3)


            maintenant = time.time()


            if maintenant - dernier_envoi > DELAI_ENVOI:
                envoyer_angles(angle1, angle2, angle3)
                dernier_envoi = maintenant


            cv2.putText(frame, "CONTROLE ACTIF", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    else:
        cv2.putText(frame, "Montre ta main", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    # Affichage angles
    cv2.putText(frame, f"M1: {angle1}", (20, 420),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)


    cv2.putText(frame, f"M2: {angle2}", (20, 450),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)


    cv2.putText(frame, f"M3: {angle3}", (20, 480),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)


    cv2.imshow("Controle bras robot avec la main", frame)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break




webcam.release()
detecteur_mains.close()
arduino.close()
cv2.destroyAllWindows()


print("Programme fermé.")
