#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 14:25:00 2023

@author: gabriele
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 12:18:13 2023

@author: gabriele
"""

##VERSUCH NEUE ZEILE JE MENGENANGABE/ZUTAT

##----------------------------#Part 1 and 2--------------------------------------

from selenium import webdriver
import re
from bs4 import BeautifulSoup
import os

# Base URL for category pages
base_url = "https://www.chefkoch.de/rs/s{}/Rezepte.html"

# Counter for category pages
count_cat = 0
checked_urls = []  # List to store checked URLs

# Loop to check category pages until an unavailable page is encountered
while True:
    url = base_url.format(count_cat)
    response = requests.get(url)

    if response.status_code == 200:
        print(f"URL {count_cat} is available.")
        checked_urls.append(url)
        count_cat += 1
    else:
        print(f"URL {count_cat} is not available. Stopping.")
        break

print("Checked URLs:")
for checked_url in checked_urls:
    print(checked_url)

# Extract and check links from the checked URLs
count_rec = 0
count_limit = 15  # Set the limit for the number of recipe links to extract

recipe_links = []

# Loop through each checked URL to extract recipe links
for checked_url in checked_urls:
    response = requests.get(checked_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Select recipe links using BeautifulSoup
    links = soup.select('.ds-recipe-card__link.ds-teaser-link')

    # Loop through each recipe link
    for link in links:
        if count_rec >= count_limit:
            print("Stopping loop. Count_rec reached 200.")
            break

        # Extract the href attribute from the link
        recipe_link = link['href']

        # Check the response status of the recipe link
        recipe_response = requests.get(recipe_link)

        if recipe_response.status_code == 200:
            recipe_links.append(recipe_link)
            count_rec += 1
            print(f"Recipe link {count_rec} is available.")
        else:
            print(f"Recipe link {count_rec} is not available.")

    if count_rec >= count_limit:
        break

print("\nRecipe Links:")
for recipe_link in recipe_links:
    print(recipe_links)


##--------------------------#Part 3----------------------------------------------
import pandas as pd
import re


# Lists for Recipe Data
recipe_names = []
preptimes = []
difficulties = []
calories_list = []
rating_avgs = []
rating_counts = []
servings_list = []
quantities_list = []  # Separate lists for quantities and units
units_list = []  # List to store units same as ingredients list
ingredients_list = []
nutrition_values_list = []

for recipe_link in recipe_links:
    # Anfrage an die Rezeptseite senden
    response_recipe = requests.get(recipe_link, timeout=120)

    soup_recipe = BeautifulSoup(response_recipe.content, 'html.parser')

    # Sicherstellen, dass die Anfrage erfolgreich war (Statuscode 200)
    if response_recipe.status_code == 200 or response.status_code == 301:
        print(f"Anfrage an {recipe_link} erfolgreich.")

        # HTML-Inhalt extrahieren
        html_content_recipe = response_recipe.text

        # Beautiful Soup verwenden, um den HTML-Inhalt zu analysieren
        soup_recipe = BeautifulSoup(html_content_recipe, 'html.parser')

        # Recipe Name
        recipe_name = soup_recipe.find('h1')
        recipe_name_value = recipe_name.text.strip() if recipe_name else 'N/A'

        # Preptime
        preptime = soup_recipe.find('span', class_='recipe-preptime rds-recipe-meta__badge')
        preptime_value = re.sub(r'[^\x00-\x7F]+', '', preptime.text.strip()) if preptime else 'N/A'

        # Difficulty
        difficulty = soup_recipe.find('span', class_='recipe-difficulty rds-recipe-meta__badge')
        difficulty_value = re.sub(r'[^\x00-\x7F]+', '', difficulty.text.strip()) if difficulty else 'N/A'

        # Calories
        calories = soup_recipe.find('span', class_='recipe-kcalories rds-recipe-meta__badge')
        calories_value = re.search(r'\d+', calories.text.strip()).group() if calories else 'N/A'

        # Rating Average
        rating_avg = soup_recipe.find('div', class_='ds-rating-avg')
        rating_avg_match = re.search(r'\d+\.\d+', str(rating_avg)) if rating_avg else None
        rating_avg_value = rating_avg_match.group() if rating_avg_match else 'N/A'

        # Rating Count
        rating_count = soup_recipe.find('div', class_='ds-rating-count')
        rating_count_value = re.search(r'(\d+)', rating_count.text.strip()).group() if rating_count else 'N/A'

        # Recipe Servings
        servings = soup_recipe.find('input', class_='ds-input')
        servings_value = servings['value'].strip() if servings else 'N/A'

        # Quantity
        quantity_elements = soup_recipe.find_all('td', class_='td-left')
        quantities_values = [quantity_element.text.strip() for quantity_element in quantity_elements]

        # Units
        unit_elements = soup_recipe.find_all('td', class_='td-right')  
        units_values = [unit_element.text.strip() for unit_element in unit_elements]

        # Ingredients
        ingredients_elements = soup_recipe.find_all('td', class_='td-right')
        ingredients_values = [ingredient_element.text.strip() for ingredient_element in ingredients_elements]

        # Ensure there's a placeholder for recipes without a clear quantity
        ingredients_value = '\n'.join(ingredients_values) if ingredients_values else 'N/A'

        # Nutrition Values
        nutrition_values = soup_recipe.find('div', class_='recipe-nutrition_content ds-box ds-grid')
        nutrition_values_text = ''

        if nutrition_values:
            # Durchlaufe jedes Element in der Nährwert-Tabelle
            for item in nutrition_values.find_all('div', class_='ds-col-3'):
                # Extrahiere den Nährstofftyp (Z.B., kcal, Kohlenhydr., Eiweiß, Fett)
                nutrient_type = item.find('h5')

                if nutrient_type:
                    nutrient_type = nutrient_type.text.strip()
                else:
                    continue  # Überspringe Elemente ohne 'h5'

                # Extrahiere den Nährstoffwert
                nutrient_value = item.contents[-1].strip()

                # Füge den Nährstofftyp und -wert zum Text hinzu
                nutrition_values_text += f"{nutrient_type}: {nutrient_value}\n"

            # Entferne nicht-druckbare Zeichen
            nutrition_values_text = re.sub(r'[^\x00-\x7F]+', '', nutrition_values_text).strip()

        # Falls keine Nährwertinformationen gefunden wurden oder der Text leer ist, setze 'N/A'
        nutrition_values_text = nutrition_values_text if nutrition_values_text else 'N/A'

        print("Extracted Nutrition Values:", nutrition_values_text)

        # Append values to lists
        recipe_names.append(recipe_name_value)
        preptimes.append(preptime_value)
        difficulties.append(difficulty_value)
        calories_list.append(calories_value)
        rating_avgs.append(rating_avg_value)
        rating_counts.append(rating_count_value)
        servings_list.append(servings_value)
        
        
        #Convert quantities and units lists to strings with new lines
        
        quantities_list.append('\n'.join(quantities_values))
        units_list.append('\n'.join(units_values))
        
        
        ingredients_list.append(ingredients_value)
        nutrition_values_list.append(nutrition_values_text)

# Consolidate in dataframe and save as csv
all_recipes_df = pd.DataFrame({
    'Recipe Name': recipe_names,
    'Preptime': preptimes,
    'Difficulty': difficulties,
    'Calories': calories_list,
    'Rating Average': rating_avgs,
    'Rating Count': rating_counts,
    'Recipe Servings': servings_list,
    'Quantities': quantities_list,
    'Units': units_list,
    'Ingredients': ingredients_list,
    'Nutrition Values': nutrition_values_list
})

# Display the DataFrame
print(all_recipes_df)

# Save DataFrame to CSV
csv_path = '/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/Recipe_dataset.csv'
all_recipes_df.to_csv(csv_path, index=False)
print(f"DataFrame saved to {csv_path}")

