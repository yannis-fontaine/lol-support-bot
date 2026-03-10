# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pytesseract
import re

# Chemin vers Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    """
    Isole uniquement le texte blanc (les chiffres)
    en ignorant le fond vert.
    """
    # Agrandit x3
    image = cv2.resize(image, None, fx=3, fy=3, 
                       interpolation=cv2.INTER_CUBIC)
    
    # Convertit en HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Isole les pixels blancs/très clairs uniquement
    # (faible saturation + haute valeur = blanc)
    blanc_bas  = np.array([0,   0, 180])
    blanc_haut = np.array([180, 40, 255])
    
    masque = cv2.inRange(hsv, blanc_bas, blanc_haut)
    
    # Légère dilatation pour reconnecter les pixels du "/"
    kernel = np.ones((2, 2), np.uint8)
    masque = cv2.dilate(masque, kernel, iterations=1)
    
    return masque
    
    return thresh

def read_bar_value(image):
    """
    Lit une valeur de type '374 / 734' dans une image.
    Ne lit que la partie centrale pour ignorer le +regen à droite.
    """
    # Garde uniquement les 40% centraux de la largeur
    h, w = image.shape[:2]
    marge_gauche = int(w * 0.30)
    marge_droite = int(w * 0.70)
    image = image[:, marge_gauche:marge_droite]

    processed = preprocess_image(image)
    
    config_tesseract = '--psm 7 -c tessedit_char_whitelist=0123456789/'
    texte = pytesseract.image_to_string(processed, config=config_tesseract)
    texte = texte.strip()
    
    match = re.search(r'(\d+)\s*/\s*(\d+)', texte)
    
    if match:
        actuel = int(match.group(1))
        maximum = int(match.group(2))
        return actuel, maximum
    
    return None, None
    
def get_percentage(actuel, maximum):
    if actuel is None or maximum is None or maximum == 0:
        return None
    return round((actuel / maximum) * 100, 1)


if __name__ == "__main__":
    import time
    from screen_capture import capture_screen
    import config

    while True:
        hp_img   = capture_screen(region=config.SELF_HP_BAR_REGION)
        mana_img = capture_screen(region=config.SELF_MANA_BAR_REGION)

        hp_act,   hp_max   = read_bar_value(hp_img)
        mana_act, mana_max = read_bar_value(mana_img)

        hp_pct   = get_percentage(hp_act,   hp_max)
        mana_pct = get_percentage(mana_act, mana_max)

        print(f"\rHP : {hp_act}/{hp_max} ({hp_pct}%)  |  "
              f"Mana : {mana_act}/{mana_max} ({mana_pct}%)", end="")
        
        time.sleep(0.5)