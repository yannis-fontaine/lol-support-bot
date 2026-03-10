# -*- coding: utf-8 -*-
import cv2
import numpy as np
from screen_capture import capture_screen
import config

ALLY_REGIONS = [
    config.ALLY_1_HP_BAR_REGION,
    config.ALLY_2_HP_BAR_REGION,
    config.ALLY_3_HP_BAR_REGION,
    config.ALLY_4_HP_BAR_REGION,
]

def get_hp_percentage(image):
    """
    Calcule le % de vie d'une barre individuelle.
    Même logique que pour notre propre barre de vie.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    vert_bas  = np.array([35, 50, 30])
    vert_haut = np.array([85, 255, 255])
    masque = cv2.inRange(hsv, vert_bas, vert_haut)

    colonnes_vertes = np.sum(np.any(masque > 0, axis=0))
    largeur_totale  = image.shape[1]

    pct = round((colonnes_vertes / largeur_totale) * 100, 1)
    return -1 if pct == 0 else pct

def get_all_allies_hp():
    """
    Retourne les % de vie des 4 alliés.
    -1 = mort
    """
    pourcentages = []
    for region in ALLY_REGIONS:
        image = capture_screen(region=region)
        pct = get_hp_percentage(image)
        pourcentages.append(pct)
    return pourcentages

def get_hp_status(pct):
    """
    Convertit un % en statut lisible pour le bot.
    """
    if pct == -1:   return "MORT"
    if pct >= 90:   return "FULL"
    if pct >= 65:   return "OK"
    if pct >= 40:   return "MOYEN"
    if pct >= 25:   return "DANGER"
    return "CRITIQUE"


if __name__ == "__main__":
    print("Démarrage ! Ctrl+C pour quitter\n")
    while True:
        pourcentages = get_all_allies_hp()

        affichage = "  |  ".join([
            f"Allié {i+1}: {get_hp_status(pct)} ({pct}%)"
            for i, pct in enumerate(pourcentages)
        ])
        print(f"\r{affichage}", end="")