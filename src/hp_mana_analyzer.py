# -*- coding: utf-8 -*-
import cv2
import numpy as np

COULEURS = {
    "hp":   (np.array([35, 50, 30]),   np.array([85, 255, 255])),
    "mana": (np.array([100, 50, 50]),  np.array([130, 255, 255])),
}

def get_bar_percentage(image, type_barre="hp"):
    bas, haut = COULEURS[type_barre]
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    masque = cv2.inRange(hsv, bas, haut)
    largeur_totale = masque.shape[1]
    colonnes_colorees = np.sum(np.any(masque > 0, axis=0))
    pourcentage = (colonnes_colorees / largeur_totale) * 100

    # Correction du décalage de calibration (+2% max)
    pourcentage = min(pourcentage * 1.02, 100.0)
    return round(pourcentage, 1)


if __name__ == "__main__":
    from screen_capture import capture_screen
    import config

    print("Test en direct — Appuie sur 'Q' pour quitter")

    while True:
        hp_img   = capture_screen(region=config.SELF_HP_BAR_REGION)
        mana_img = capture_screen(region=config.SELF_MANA_BAR_REGION)

        hp_pct   = get_bar_percentage(hp_img,   "hp")
        mana_pct = get_bar_percentage(mana_img, "mana")

        print(f"\rHP : {hp_pct}%  |  Mana : {mana_pct}%", end="")