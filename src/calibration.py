import pyautogui
import numpy as np
import cv2

# -*- coding: utf-8 -*-

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

def capture_screen(region=None):
    screenshot = pyautogui.screenshot(region=region)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

def calibrate_zone(nom):
    print(f"\n--- Calibration : {nom} ---")
    print(f"Positionne ta souris sur le coin HAUT-GAUCHE de '{nom}'")
    print("Appuie sur ENTRÉE quand tu es prêt.")
    input()
    x1, y1 = pyautogui.position()
    print(f"✅ Coin haut-gauche : ({x1}, {y1})")

    print(f"Positionne ta souris sur le coin BAS-DROITE de '{nom}'")
    print("Appuie sur ENTRÉE quand tu es prêt.")
    input()
    x2, y2 = pyautogui.position()
    print(f"✅ Coin bas-droite : ({x2}, {y2})")

    region = (x1, y1, x2 - x1, y2 - y1)

    print(f"\nVérification visuelle — Appuie sur 'Q' pour valider, 'R' pour recommencer")
    while True:
        frame = capture_screen(region=region)
        cv2.imshow(f"Calibration - {nom}", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            print(f"✅ '{nom}' validé !")
            return region
        elif key == ord('r'):
            cv2.destroyAllWindows()
            print("🔄 On recommence...")
            return calibrate_zone(nom)

# Définition des zones à calibrer
ZONES = [
    ("MINIMAP",         "la minimap"),
    ("ALLY_HP_BARS",    "les barres de vie alliés (encadre les 5 portraits à gauche)"),
    ("SELF_HP_BAR",     "ta propre barre de vie"),
    ("SELF_MANA_BAR",   "ta propre barre de mana"),
]

print("=== Outil de calibration LoL Support Bot ===")
print(f"Résolution détectée : {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
print(f"\n{len(ZONES)} zones à calibrer : {', '.join([z[0] for z in ZONES])}")

# Vérifie si un config.py existe déjà
try:
    import config
    print("\n⚠️  Un config.py existe déjà.")
    print("Veux-tu recalibrer toutes les zones ? (o/n)")
    reponse = input().strip().lower()
    if reponse != 'o':
        print("Calibration annulée.")
        exit()
except ImportError:
    pass

resultats = {}

# Calibration de chaque zone
for cle, description in ZONES:
    print(f"\n{'='*40}")
    print(f"Zone suivante : {description.upper()}")
    print(f"{'='*40}")
    resultats[cle] = calibrate_zone(description)

# Sauvegarde dans config.py
with open("config.py", "w") as f:
    f.write("# ================================================\n")
    f.write("# config.py — Généré automatiquement par calibration.py\n")
    f.write("# ================================================\n\n")
    f.write(f"SCREEN_WIDTH = {SCREEN_WIDTH}\n")
    f.write(f"SCREEN_HEIGHT = {SCREEN_HEIGHT}\n\n")
    f.write("# Zones de capture (x, y, largeur, hauteur)\n")
    for cle, region in resultats.items():
        f.write(f"{cle}_REGION = {region}\n")

print("\n✅ config.py généré avec succès !")
print("Voici son contenu :\n")
with open("config.py", "r") as f:
    print(f.read())