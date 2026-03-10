# -*- coding: utf-8 -*-
import pyautogui
import numpy as np
import cv2

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

def capture_screen(region=None):
    """
    Capture l'écran entier ou une région spécifique.
    region = (x, y, largeur, hauteur)
    """
    screenshot = pyautogui.screenshot(region=region)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

if __name__ == "__main__":
    import config

    zones = {
        "1": ("MINIMAP",        config.MINIMAP_REGION),
        "2": ("ALLY_HP_BARS",   config.ALLY_HP_BARS_REGION),
        "3": ("SELF_HP_BAR",    config.SELF_HP_BAR_REGION),
        "4": ("SELF_MANA_BAR",  config.SELF_MANA_BAR_REGION),
    }

    print("Quelle zone veux-tu visualiser ?")
    for k, (nom, _) in zones.items():
        print(f"  {k} → {nom}")

    choix = input("Ton choix : ").strip()

    if choix not in zones:
        print("Choix invalide.")
        exit()

    nom, region = zones[choix]
    print(f"Affichage de '{nom}' — Appuie sur 'Q' pour quitter")

    while True:
        frame = capture_screen(region=region)
        cv2.imshow(f"Bot Vision - {nom}", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()