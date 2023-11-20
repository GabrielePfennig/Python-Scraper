# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 10:03:01 2023

@author: Sebastian Schachtner
"""

from selenium import webdriver
import re
from bs4 import BeautifulSoup
import os


# importing the overview page 
import requests
link_cat = "https://www.chefkoch.de/rezepte/"

response = requests.get(link_cat)
#print(response)

# Save to a text file (encoding has to be set to utf-8)
with open('C:/Users/Sebastian Schachtner/Documents/01_Studium/02_Master/3rd Semester/06_Webscraping & Textual Analysis in Python/04_Project/overview.html', 'w', encoding="utf-8") as file:
    file.write(response.text)
    
with open('C:/Users/Sebastian Schachtner/Documents/01_Studium/02_Master/3rd Semester/06_Webscraping & Textual Analysis in Python/04_Project/overview.html', 'r', encoding='utf-8') as file:
    # Lese den Inhalt der HTML-Datei
    html_content = file.read()

# Verwende BeautifulSoup, um das HTML zu analysieren
soup = BeautifulSoup(html_content, 'html.parser')

# Alle Links mit der Klasse 'sg-pill' extrahieren
links_cat = soup.find_all('a', class_='sg-pill')

# Die gewünschten Rezepte-Links ausgeben
for link_cat in links_cat:
    href_cat = link_cat['href']
   
# Liste der href-Werte erstellen
href_cats = [link_cat['href'] for link_cat in links_cat]

href_catsends = []

for href_cat in href_cats:
    split_result = href_cat.split('t', 1)
    href_catend = 't' + split_result[1]
    href_catsends.append(href_catend)
    print (href_catsends)
#WAS WIRD HIER GEMACHT: URLs für verschiedene Unterseiten erstellen und überprüfen, ob diese verfügbar sind??
base_caturl = "https://www.chefkoch.de/rs/s"
num_pages = 5  # Hier die gewünschte Anzahl eintragen

base_caturls = [f"{base_caturl}{page_number}" for page_number in range(num_pages)]

category_links = [f"{base_caturl}{href_catend}" for base_caturl in base_caturls for href_catend in href_catsends]

for url in category_links:
    response = requests.head(url)
    if response.status_code == 200:
        print(f"URL {url} is available.")
    else:
        print(f"URL {url} is not available. Status code: {response.status_code}")

     



# Ordner erstellen, um HTML-Dateien bzw. Unterseiten zu speichern
output_folder = "C:/Users/Sebastian Schachtner/Documents/01_Studium/02_Master/3rd Semester/06_Webscraping & Textual Analysis in Python/04_Project/category_pages"
os.makedirs(output_folder, exist_ok=True)


for url in category_links:
    # Anfrage an die URL senden
    response = requests.get(url)

    # Sicherstellen, dass die Anfrage erfolgreich war (Statuscode 200)
    if response.status_code == 200:
        # HTML-Inhalt extrahieren
        html_content = response.text
        
        # HTML-Dateiname aus der URL ableiten
        filename = os.path.join(output_folder, f"{url.replace('https://www.chefkoch.de/rezepte/', '').replace('/', '_')}.html")

        # HTML-Datei speichern
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"HTML von {url} wurde erfolgreich gespeichert.")
    else:
        print(f"Fehler beim Abrufen von {url}. Statuscode: {response.status_code}")



# Ordner, in dem die HTML-Dateien gespeichert sind
output_folder = "C:/Users/Sebastian Schachtner/Documents/01_Studium/02_Master/3rd Semester/06_Webscraping & Textual Analysis in Python/04_Project/category_pages"

# Liste der HTML-Dateien im Ordner abrufen
html_files = [f for f in os.listdir(output_folder) if f.endswith(".html")]

# Durchlaufe alle HTML-Dateien
for filename in html_files:
    # Pfad zur HTML-Datei erstellen
    file_path = os.path.join(output_folder, filename)
    
    # HTML-Datei öffnen und den Inhalt lesen
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Beautiful Soup verwenden, um den HTML-Inhalt zu analysieren
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Alle Links mit der Klasse 'ds-recipe-card__link ds-teaser-link' extrahieren (Links zu den bestimmten Rezepten)
    links = soup.select('.ds-recipe-card__link.ds-teaser-link')

        # Die gewünschten Links in einem String speichern
    recipie_links = f"Links in {filename}:\n"

        #Ausgabe der extrahierten Rezept-Links
    
    for link in links:
        href_rec = link['href']
        recipie_links += f"{href_rec}\n"

            #Hinzufügen einer Trennlinie und Zeilenumbrüche um die einzelnen Rezeptlinks voneinander zu trennen und die Ausgabe übersichtlicher zu gestalten
    
    recipie_links += "\n" + "-"*50 + "\n"
    
    print(recipie_links)

    
