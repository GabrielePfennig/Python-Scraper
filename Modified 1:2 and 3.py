# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 10:03:01 2023

@author: Sebastian Schachtner
"""

----------------------------#Part 1 and 2--------------------------------------

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
with open('/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/overview.html', 'w', encoding="utf-8") as file:
    file.write(response.text)
    
with open('/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/overview.html', 'r', encoding='utf-8') as file:
    # Lese den Inhalt der HTML-Datei
    html_content = file.read()

# Verwende BeautifulSoup, um das HTML zu analysieren
soup = BeautifulSoup(html_content, 'html.parser')

# Alle Rezepte-Links mit der Klasse 'sg-pill' extrahieren
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
#
base_caturl = "https://www.chefkoch.de/rs/s"
num_pages = 5  # Hier die gewünschte Anzahl eintragen  #########Leave #No. of recipe pages as a restrictor or use a loop instead#######

base_caturls = [f"{base_caturl}{page_number}" for page_number in range(num_pages)]

category_links = [f"{base_caturl}{href_catend}" for base_caturl in base_caturls for href_catend in href_catsends]

for url in category_links:
    response = requests.head(url)
    if response.status_code == 200:
        print(f"URL {url} is available.")
    else:
        print(f"URL {url} is not available. Status code: {response.status_code}")

     
# Ordner erstellen, um HTML-Dateien zu speichern
output_folder = "/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/category_pages"
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
output_folder = "/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/category_pages"

# Liste der HTML-Dateien im Ordner abrufen
html_files = [f for f in os.listdir(output_folder) if f.endswith(".html")]

# Liste für die Rezeptlinks erstellen
recipe_links = []

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
   
    # Rezeptlinks in der Liste hinzufügen
    for link in links:
        recipe_links.append(link['href'])

print(recipe_links)

    
 
    
--------------------------#Part 3----------------------------------------------


import pandas as pd

# DataFrame für alle Rezepte erstellen
all_recipes_df = pd.DataFrame(columns=['Recipe Name', 'Preptime', 'Difficulty', 'Calories', 'Rating Average', 'Rating Count', 'Recipe Servings', 'Quantity', 'Ingredients', 'Nutrition Values'])

for recipe_link in recipe_links:
    # Anfrage an die Rezeptseite senden
    response_recipe = requests.get(recipe_link)
    
    # Sicherstellen, dass die Anfrage erfolgreich war (Statuscode 200)
    if response_recipe.status_code == 200:
        print(f"Anfrage an {recipe_link} erfolgreich.")
        
        # HTML-Inhalt extrahieren
        html_content_recipe = response_recipe.text
       
        # Beautiful Soup verwenden, um den HTML-Inhalt zu analysieren
        soup_recipe = BeautifulSoup(html_content_recipe, 'html.parser')
        
        # Recipe Name extrahieren 
        recipe_name = soup_recipe.find('h1', class_='?????')  # Hier die korrekte Klasse einfügen
        recipe_name_value = recipe_name.text.strip() if recipe_name else 'N/A'
        ####HELP###
        
        # Preptime extrahieren
        preptime = soup_recipe.find('span', class_='recipe-preptime rds-recipe-meta_badge')
        preptime_value = preptime.text.strip() if preptime else 'N/A'
        
        # Difficulty extrahieren
        difficulty = soup_recipe.find('span', class_='recipe-difficulty rds-recipe-meta_badge')
        difficulty_value = difficulty.text.strip() if difficulty else 'N/A'
        
        # Calories extrahieren
        calories = soup_recipe.find('span', class_='recipe-kcalories rds-recipe-meta_badge')
        calories_value = calories.text.strip() if calories else 'N/A'
        
        # Rating Average extrahieren
        rating_avg = soup_recipe.find('div', class_='ds-rating-avg')
        rating_avg_value = rating_avg.text.strip() if rating_avg else 'N/A'
      
        # Rating Count extrahieren
        rating_count = soup_recipe.find('div', class_='ds-rating-count')
        rating_count_value = rating_count.text.strip() if rating_count else 'N/A'
        
        # Recipe Servings extrahieren
        servings = soup_recipe.find('input', class_='ds-input')
        servings_value = servings['value'].strip() if servings else 'N/A'
        
        # Quantity extrahieren
        quantity = soup_recipe.find('td', class_='td-left')
        quantity_value = quantity.text.strip() if quantity else 'N/A'
       
        # Ingredients extrahieren
        ingredients = soup_recipe.find('td', class_='td-right')
        ingredients_value = ingredients.text.strip() if ingredients else 'N/A'
        
        # Nutrition Values extrahieren
        nutrition_values = soup_recipe.find('div', class_='ds-col-3')
        nutrition_values_text = nutrition_values.text.strip() if nutrition_values else 'N/A'
        
        # Liste für das aktuelle Rezept erstellen
        current_recipe = [recipe_name_value, preptime_value, difficulty_value, calories_value, rating_avg_value, rating_count_value, servings_value, quantity_value, ingredients_value, nutrition_values_text]
        
        # Das aktuelle Rezept zu DataFrame hinzufügen
        all_recipes_df = all_recipes_df.append(pd.Series(current_recipe, index=all_recipes_df.columns), ignore_index=True)
        
# Das gesamte DataFrame anzeigen
print(all_recipes_df)

# DataFrame in CSV-Datei speichern
csv_recipes = "/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/recipes.csv"
all_recipes_df.to_csv(recipes.csv, index=False)

# Erfolgsmeldung ausgeben
print(f"Das DataFrame wurde erfolgreich in die CSV-Datei '{csv_filename}' gespeichert.")

        
        
     
        
        
        
        
        
    
       
        
       
        
        
        
        
        
        
        
        
        
    
        
        
        
   

        
        
        
        
   
       
       
       
       
       
       
       
       
       











