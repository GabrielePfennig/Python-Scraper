#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 13:13:51 2023

@author: gabriele
"""

# Attempt create rows 
#----------------------------#Part 1 and 2--------------------------------------
 
from selenium import webdriver
import re
from bs4 import BeautifulSoup
import os
 
# Importing the overview page 
import requests
link_cat = "https://www.chefkoch.de/rezepte/"
 
response = requests.get(link_cat)
 
# Save to a text file (encoding has to be set to utf-8)
with open('/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/overview.html', 'w', encoding="utf-8") as file:
    file.write(response.text)
    
with open('/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/overview.html', 'r', encoding='utf-8') as file:
    # Read the content of the HTML file
    html_content = file.read()
 
# Use BeautifulSoup to analyze HTML
soup = BeautifulSoup(html_content, 'html.parser')
 
# Extract all recipe links with the class 'sg-pill'
links_cat = soup.find_all('a', class_='sg-pill')
 
# Output the desired recipe links
for link_cat in links_cat:
    href_cat = link_cat['href']
   
# Create a list of href values
href_cats = [link_cat['href'] for link_cat in links_cat]
 
href_catsends = []
 
for href_cat in href_cats:
    split_result = href_cat.split('t', 1)
    href_catend = 't' + split_result[1]
    href_catsends.append(href_catend)
    print (href_catsends)
#
base_caturl = "https://www.chefkoch.de/rs/s"
num_pages = 1  # Enter the desired number here  
 
base_caturls = [f"{base_caturl}{page_number}" for page_number in range(num_pages)]
 
category_links = [f"{base_caturl}{href_catend}" for base_caturl in base_caturls for href_catend in href_catsends]
 
for url in category_links:
    response = requests.head(url)
    if response.status_code == 200:
        print(f"URL {url} is available.")
        
    elif response.status_code == 301 :
         print(f"URL {url} is available.")
         
    else:
        print(f"URL {url} is not available. Status code: {response.status_code}")
 
     
# Create a folder to save HTML files
output_folder = "/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/category_pages"
os.makedirs(output_folder, exist_ok=True)
 
 
for url in category_links:
    # Send a request to the URL
    response = requests.get(url)
 
    # Ensure the request was successful (Status code 200)
    if response.status_code == 200 or response.status_code == 301:
        # Extract HTML content
        html_content = response.text
        
        # Derive HTML filename from the URL
        filename = os.path.join(output_folder, f"{url.replace('https://www.chefkoch.de/rezepte/', '').replace('/', '_')}.html")
 
        # Save HTML file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
 
        print(f"HTML from {url} was successfully saved.")
    else:
        print(f"Error retrieving {url}. Status code: {response.status_code}")
 
 
# Folder where the HTML files are saved
output_folder = "/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/category_pages"
 
# Get a list of HTML files in the folder
html_files = [f for f in os.listdir(output_folder) if f.endswith(".html")]
 
# List for recipe links
recipe_links = []
 
# Iterate through all HTML files
for filename in html_files:
    # Path to the HTML file
    file_path = os.path.join(output_folder, filename)
    
    # Open the HTML file and read the content
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Use Beautiful Soup to analyze the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract all links with the class 'ds-recipe-card__link ds-teaser-link' (Links to specific recipes)
    links = soup.select('.ds-recipe-card__link.ds-teaser-link')
   
    # Add recipe links to the list
    for link in links:
        recipe_links.append(link['href'])
 
print(recipe_links)
 
 
##--------------------------#Part 3----------------------------------------------
 
import pandas as pd
import re


# Neue Listen für die aufgespaltenen Daten
split_recipe_names = []
split_preptimes = []
split_difficulties = []
split_rating_avgs = []
split_rating_counts = []
split_servings_list = []
split_quantities_list = []
split_ingredients_list = []
split_calories_list = []
split_proteins_list = []
split_fat_list = []
split_carbohydrates_list = []
split_recipe_links_list = []

for recipe_link in recipe_links:
    response_recipe = requests.get(recipe_link, timeout=120)

    soup_recipe = BeautifulSoup(response_recipe.content, 'html.parser')

    # Sicherstellen, dass der Request erfolgreich war
    if response_recipe.status_code == 200:
        print(f"Request to {recipe_link} successful.")

        # Extrahiere HTML-Inhalt
        html_content_recipe = response_recipe.text

        # Verwende Beautiful Soup zur Analyse des HTML-Inhalts
        soup_recipe = BeautifulSoup(html_content_recipe, 'html.parser')

        # Extrahiere Recipe Name
        recipe_name = soup_recipe.find('h1')
        recipe_name_value = recipe_name.text.strip() if recipe_name else 'N/A'

        # Extrahiere Preptime
        preptime = soup_recipe.find('span', class_='recipe-preptime rds-recipe-meta__badge')
        preptime_value = re.sub(r'[^\x00-\x7F]+', '', preptime.text.strip()) if preptime else 'N/A'

        # Extrahiere Difficulty
        difficulty = soup_recipe.find('span', class_='recipe-difficulty rds-recipe-meta__badge')
        difficulty_value = re.sub(r'[^\x00-\x7F]+', '', difficulty.text.strip()) if difficulty else 'N/A'
        difficulty_value = difficulty_value.strip()

        # Extrahiere Rating Average
        rating_avg = soup_recipe.find('div', class_='ds-rating-avg')
        rating_avg_match = re.search(r'\d+\.\d+', str(rating_avg)) if rating_avg else None
        rating_avg_value = rating_avg_match.group() if rating_avg_match else 'N/A'

        # Extrahiere Rating Count
        rating_count = soup_recipe.find('div', class_='ds-rating-count')
        rating_count_value = re.search(r'(\d+)', rating_count.text.strip()).group() if rating_count else 'N/A'

        # Extrahiere Recipe Servings
        servings = soup_recipe.find('input', class_='ds-input')
        servings_value = servings['value'].strip() if servings else 'N/A'

        # Extrahiere Quantity Elements und Ingredients Elements
        quantity_elements = soup_recipe.find_all('td', class_='td-left')
        ingredients_elements = soup_recipe.find_all('td', class_='td-right')

        # Iteriere durch jede Zutat und Menge
        for quantity_element, ingredient_element in zip(quantity_elements, ingredients_elements):
            # Extrahiere Quantity
            quantity = quantity_element.text.strip() if quantity_element else 'N/A'

            # Extrahiere Ingredients
            ingredients = ingredient_element.text.strip() if ingredient_element else 'N/A'
            
            # Versuche, nutrition_values zu extrahieren
            nutrition_values = soup_recipe.find('div', class_='recipe-nutrition_content ds-box ds-grid')

            # Neue Spaltenwerte initialisieren
            calories_value = 'N/A'
            proteins_value = 'N/A'
            fat_value = 'N/A'
            carbohydrates_value = 'N/A'

            if nutrition_values:
                # Iteriere durch jedes Element in der Ernährungstabelle
                for item in nutrition_values.find_all('div', class_='ds-col-3'):
                    # Extrahiere den Nährstofftyp (z. B. kcal, Eiweiß, Fett, Kohlenhydrate)
                    nutrient_type = item.find('h5').text.strip() if item.find('h5') else None

                    # Extrahiere den Nährstoffwert
                    nutrient_value = item.contents[-1].strip() if item.contents else None

                    # Weise den Werten den entsprechenden Spalten zu
                    if nutrient_type == 'kcal':
                        calories_match = re.search(r'(\d+,\d+|\d+)', nutrient_value)
                        calories_value = calories_match.group(1).replace(',', '.') if calories_match else 'N/A'
                    elif nutrient_type == 'Eiweiß':
                        proteins_match = re.search(r'(\d+,\d+|\d+)', nutrient_value)
                        proteins_value = proteins_match.group(1).replace(',', '.') if proteins_match else 'N/A'
                    elif nutrient_type == 'Fett':
                        fat_match = re.search(r'(\d+,\d+|\d+)', nutrient_value)
                        fat_value = fat_match.group(1).replace(',', '.') if fat_match else 'N/A'
                    elif nutrient_type == 'Kohlenhydr.':
                        carbohydrates_match = re.search(r'(\d+,\d+|\d+)', nutrient_value)
                        carbohydrates_value = carbohydrates_match.group(1).replace(',', '.') if carbohydrates_match else 'N/A'


            # Append Werte zu den Listen
            split_recipe_names.append(recipe_name_value)
            split_preptimes.append(preptime_value)
            split_difficulties.append(difficulty_value)
            split_rating_avgs.append(rating_avg_value)
            split_rating_counts.append(rating_count_value)
            split_servings_list.append(servings_value)
            split_quantities_list.append(quantity)
            split_ingredients_list.append(ingredients)
            split_calories_list.append(calories_value)
            split_proteins_list.append(proteins_value)
            split_fat_list.append(fat_value)
            split_carbohydrates_list.append(carbohydrates_value)
            split_recipe_links_list.append(recipe_link)

# Erstelle DataFrame für die aufgespaltenen Daten
split_recipes_df = pd.DataFrame({
    'Recipe Name': split_recipe_names,
    'Preptime': split_preptimes,
    'Difficulty': split_difficulties,
    'Rating Average': split_rating_avgs,
    'Rating Count': split_rating_counts,
    'Recipe Servings': split_servings_list,
    'Quantities': split_quantities_list,
    'Ingredients': split_ingredients_list,
    'Calories_in_g': split_calories_list,
    'Proteins_in_g': split_proteins_list,
    'Fat_in_g': split_fat_list,
    'Carbohydrates_in_g': split_carbohydrates_list,
    'Link': split_recipe_links_list
})

# Display the DataFrame
print(split_recipes_df)

# Speichere DataFrame als CSV
csv_path = '/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/Split_Recipe_dataset.csv'
split_recipes_df.to_csv(csv_path, index=False)
print(f"DataFrame saved to {csv_path}")






