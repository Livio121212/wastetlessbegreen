import streamlit as st
from PIL import Image, ImageEnhance
import easyocr
import numpy as np
import re

# Initialisierung des EasyOCR-Lesers
reader = easyocr.Reader(['de', 'en'])  # Unterstützung für Deutsch und Englisch

# Hochlade-Widget für die Rechnung
uploaded_file = st.file_uploader("Lade ein Bild der Rechnung hoch", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Bild laden
    image = Image.open(uploaded_file)
    
    # Bild in der Originalversion anzeigen
    st.image(image, caption='Hochgeladenes Bild der Rechnung', use_column_width=True)

    # Bildvorverarbeitung (Graustufen und Kontrastverbesserung)
    image = image.convert("L")  # Konvertiere in Graustufen
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Kontrasterhöhung für bessere OCR-Erkennung

    # Bild als NumPy-Array konvertieren
    image_np = np.array(image)

    # OCR auf das Bild anwenden
    st.write("Extrahiere Text aus der Rechnung...")
    results = reader.readtext(image_np)

    # Funktion zum Zusammenfügen von Zeilen
    def combine_lines(results):
        combined_text = []
        current_line = ""
        
        for i, result in enumerate(results):
            line = result[1].strip()
            # Prüfen, ob die Zeile einen Preis enthält, was darauf hinweist, dass sie abgeschlossen ist
            if re.search(r'\d+,\d{2}', line):
                if current_line:
                    # Wenn bereits ein "current_line" existiert, füge ihn zur Liste hinzu
                    combined_text.append(current_line)
                current_line = line  # Beginne eine neue Zeile
            else:
                # Wenn keine Preisangabe vorhanden ist, füge die Zeile zu "current_line" hinzu
                current_line += " " + line
        
        # Die letzte Zeile hinzufügen
        if current_line:
            combined_text.append(current_line)
        
        return combined_text

    # Kombinierte Zeilen
    combined_text = combine_lines(results)

    # Extrahierten Text Zeile für Zeile anzeigen
    st.write("Kombinierte und Extrahierte Zeilen:")
    for line in combined_text:
        st.write(line)

    # Funktion zum Extrahieren von Artikeln, Mengen und Preisen aus jeder kombinierten Zeile
    def extract_items_from_lines(combined_text):
        items = []
        for line in combined_text:
            # Liste möglicher Regex-Muster für verschiedene Rechnungsformate
            patterns = [
                r'(\d+)\s*x?\s*(.+?)\s+(\d+,\d{2})',          # Menge, Artikelname, Preis/Gesamtpreis
                r'(.+?)\s+(\d+,\d{2})\s+(\d+,\d{2})',        # Artikelname, Einzelpreis, Gesamtpreis
                r'(.+?)\s+(\d+,\d{2})'                       # Artikelname und Preis ohne Gesamtpreis
            ]

            # Durchlaufe die Muster, bis eine Übereinstimmung gefunden wird
            matched = False
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    quantity = 1  # Standardmenge auf 1 setzen
                    item_name = match.group(1).strip()
                    price = None
                    total_price = None

                    # Je nach gefundenem Muster die Details extrahieren
                    if len(match.groups()) == 2:
                        item_name = match.group(1).strip()
                        price = float(match.group(2).replace(',', '.'))
                        total_price = price
                    elif len(match.groups()) == 3:
                        quantity = int(match.group(1)) if match.group(1).isdigit() else 1
                        item_name = match.group(2).strip()
                        price = float(match.group(3).replace(',', '.'))
                        total_price = price
                    
                    items.append({"Menge": quantity, "Artikel": item_name, "Preis": total_price})
                    matched = True
                    break

            # Wenn keine der Regex übereinstimmt, füge die Zeile als unerkannt hinzu
            if not matched:
                st.write(f"Nicht erkanntes Zeilenformat: {line}")

        return items

    # Informationen aus jeder kombinierten Zeile extrahieren
    items = extract_items_from_lines(combined_text)

    # Extrahierte Artikel anzeigen
    if items:
        st.write("Extrahierte Artikel:")
        for item in items:
            st.write(f"Menge: {item['Menge']} - Artikel: {item['Artikel']} - Preis: {item['Preis']} EUR")
    else:
        st.write("Es konnten keine Artikel aus dem Text extrahiert werden.")



