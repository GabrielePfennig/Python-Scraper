#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 13:33:12 2023

@author: gabriele
"""

from selenium import webdriver
import re
from bs4 import BeautifulSoup
import os

# Importing the overview page
import requests

link_cat = "https://www.chefkoch.de/rezepte/"

response = requests.get(link_cat)

# Save to a text file (encoding has to be set to utf-8)
with open("overview.html", "w", encoding="utf-8") as file:
    file.write(response.text)

with open("overview.html", "r", encoding="utf-8") as file:
    # Read the content of the HTML file
    html_content = file.read()

# Use BeautifulSoup to analyze HTML
soup = BeautifulSoup(html_content, "html.parser")

# Extract all recipe links with the class 'sg-pill'
links_cat = soup.find_all("a", class_="sg-pill")

# Output the desired recipe links
for link_cat in links_cat:
    href_cat = link_cat["href"]

# Create a list of href values
href_cats = [link_cat["href"] for link_cat in links_cat]

href_catsends = []

for href_cat in href_cats:
    split_result = href_cat.split("t", 1)
    href_catend = "t" + split_result[1]
    href_catsends.append(href_catend)
    print(href_catsends)
#
base_caturl = "https://www.chefkoch.de/rs/s"
num_pages = 1  # Enter the desired number here

base_caturls = [f"{base_caturl}{page_number}" for page_number in range(num_pages)]

category_links = [
    f"{base_caturl}{href_catend}"
    for base_caturl in base_caturls
    for href_catend in href_catsends
]

for url in category_links:
    response = requests.head(url)
    if response.status_code == 200:
        print(f"URL {url} is available.")

    elif response.status_code == 301:
        print(f"URL {url} is available.")

    else:
        print(f"URL {url} is not available. Status code: {response.status_code}")


# Create a folder to save HTML files
output_folder = (
    "/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/category_pages"
)
os.makedirs(output_folder, exist_ok=True)


for url in category_links:
    # Send a request to the URL
    response = requests.get(url)

    # Ensure the request was successful (Status code 200)
    if response.status_code == 200 or response.status_code == 301:
        # Extract HTML content
        html_content = response.text

        # Derive HTML filename from the URL
        filename = os.path.join(
            output_folder,
            f"{url.replace('https://www.chefkoch.de/rezepte/', '').replace('/', '_')}.html",
        )

        # Save HTML file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"HTML from {url} was successfully saved.")
    else:
        print(f"Error retrieving {url}. Status code: {response.status_code}")


# Folder where the HTML files are saved
output_folder = (
    "/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/category_pages"
)

# Get a list of HTML files in the folder
html_files = [f for f in os.listdir(output_folder) if f.endswith(".html")]

# List for recipe links
recipe_links = []

# Iterate through all HTML files
for filename in html_files:
    # Path to the HTML file
    file_path = os.path.join(output_folder, filename)

    # Open the HTML file and read the content
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Use Beautiful Soup to analyze the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract all links with the class 'ds-recipe-card__link ds-teaser-link' (Links to specific recipes)
    links = soup.select(".ds-recipe-card__link.ds-teaser-link")

    # Add recipe links to the list
    for link in links:
        recipe_links.append(link["href"])

print(recipe_links)

import pandas as pd
import re
from fractions import Fraction
import tqdm

def parse_quantity_and_unit(input_string):
    # Define a mapping for Unicode fractions to their corresponding floats
    fraction_mapping = {
        "¼": 0.25,
        "½": 0.5,
        "¾": 0.75,
        "⅓": 1 / 3,
        "⅔": 2 / 3,
        "⅕": 1 / 5,
        "⅖": 2 / 5,
        "⅗": 3 / 5,
        "⅘": 4 / 5,
        "⅙": 1 / 6,
        "⅚": 5 / 6,
        "⅛": 1 / 8,
        "⅜": 3 / 8,
        "⅝": 5 / 8,
        "⅞": 7 / 8,
        "⅐": 1 / 9,
        "⅑": 1 / 10,
        "⅒": 1 / 11,
        "⅟": 1 / 12,
    }

    # Define a regular expression pattern to match quantity and unit
    pattern = re.compile(
        r"(?P<whole>\d+)?\s*(?P<unicode_fraction>[\u00BC-\u00BE\u2150-\u215E])?\s*(?P<unit>[\w.\s@+-]*)"
    )

    # Use the regular expression to find matches in the input string
    match = pattern.match(input_string)

    # If there is a match, extract the whole, unicode_fraction, and unit
    if match:
        whole = match.group("whole")
        unicode_fraction = match.group("unicode_fraction")
        unit = match.group("unit")
        # print (input_string, whole, unicode_fraction, unit)

        # Calculate the total quantity
        quantity = 0
        if whole and unicode_fraction:
            # If there's a whole number, convert it to float
            quantity += float(whole) + fraction_mapping.get(unicode_fraction, 0)
        elif unicode_fraction:
            # If there's a Unicode fraction, use the mapping
            quantity = fraction_mapping.get(unicode_fraction, 0)

        elif whole:
            quantity += float(whole)
        else:
            # If there's no fraction or whole number, set quantity to None
            quantity = "etwas"

        return quantity, unit
    else:
        return "etwas", None


# Listen für Rezeptdaten
recipe_names = []
preptimes = []
difficulties = []
rating_avgs = []
rating_counts = []
servings_list = []
quantities_list = []
ingredients_list = []
calories_list = []
proteins_list = []
fat_list = []
carbohydrates_list = []
recipe_links_list = []
units = []
menu_types = []
dietary_preferences = []
meat_fishs = []

for recipe_link in tqdm.tqdm(recipe_links):
    # Send a request to the recipe page
    response_recipe = requests.get(recipe_link, timeout=120)
    soup_recipe = BeautifulSoup(response_recipe.content, "html.parser")
    # Ensure the request was successful (Status code 200)
    if response_recipe.status_code == 200 or response.status_code == 301:
        # print(f"Request to {recipe_link} successful.")
        # Extract HTML content
        html_content_recipe = response_recipe.text
        # Use Beautiful Soup to analyze the HTML content
        soup_recipe = BeautifulSoup(html_content_recipe, "html.parser")
        tags_html = soup_recipe.select(".ds-tag.bi-tags")
        tags = [tag.decode_contents().strip().replace("\n", "") for tag in tags_html]
        # print(tags)
        dietary_pref = [
            i
            for i in [
                "Vegetarisch",
                "Vegan",
                "ketogen",
                "Paleo",
                "Low Carb",
                "kalorienarm",
                "fettarm",
                "Trennkost",
                "Vollwert",
            ]
            if i in tags
        ]
        dietary_pref = dietary_pref[0] if len(dietary_pref) else "N/A"
        menu_type = [
            i
            for i in [
                "Dessert",
                "Hauptspeise",
                "Frühstück",
                "Beilage",
                "Salat",
                "Suppen",
                "Vorspeise",
                "Getränk",
                "Snack",
            ]
            if i in tags
        ]
        menu_type = menu_type[0] if len(menu_type) else "N/A"
        meat_fish = [
            i
            for i in [
                "Geflügel",
                "Lamm oder Ziege",
                "Innereien",
                "Rind",
                "Schwein",
                "Wild",
                "Krustentier oder Fisch",
                "Fisch",
            ]
            if i in tags
        ]
        meat_fish = meat_fish[0] if len(meat_fish) else "N/A"
        # Recipe Name
        recipe_name = soup_recipe.find("h1")
        recipe_name_value = recipe_name.text.strip() if recipe_name else "N/A"
        # Preptime
        preptime = soup_recipe.find(
            "span", class_="recipe-preptime rds-recipe-meta__badge"
        )
        preptime_value = (
            re.sub(r"[^\x00-\x7F]+", "", preptime.text.strip()) if preptime else "N/A"
        )
        # Difficulty
        difficulty = soup_recipe.find(
            "span", class_="recipe-difficulty rds-recipe-meta__badge"
        )
        difficulty_value = (
            re.sub(r"[^\x00-\x7F]+", "", difficulty.text.strip())
            if difficulty
            else "N/A"
        )
        difficulty_value = difficulty_value.strip()
        # Rating Average
        rating_avg = soup_recipe.find("div", class_="ds-rating-avg")
        rating_avg_match = (
            re.search(r"\d+\.\d+", str(rating_avg)) if rating_avg else None
        )
        rating_avg_value = rating_avg_match.group() if rating_avg_match else "N/A"
        # Rating Count
        rating_count = soup_recipe.find("div", class_="ds-rating-count")
        rating_count_value = (
            re.search(r"(\d+)", rating_count.text.strip()).group()
            if rating_count
            else "N/A"
        )
        # Recipe Servings
        servings = soup_recipe.find("input", class_="ds-input")
        servings_value = servings["value"].strip() if servings else "N/A"
        # Quantity
        quantity_elements = soup_recipe.find_all("td", class_="td-left")
        quantities_values = [
            quantity_element.text.strip() for quantity_element in quantity_elements
        ]
        # Ingredients
        ingredients_elements = soup_recipe.find_all("td", class_="td-right")
        ingredients_values = [
            ingredient_element.text.strip()
            for ingredient_element in ingredients_elements
        ]
        # Ensure there's a placeholder for recipes without a clear quantity
        ingredients_value = (
            "\n".join(ingredients_values) if ingredients_values else "N/A"
        )
        # Nutrition Values
        nutrition_values = soup_recipe.find(
            "div", class_="recipe-nutrition_content ds-box ds-grid"
        )
        nutrition_values_text = ""
        # Neue Spaltenwerte initialisieren
        calories_value = "N/A"
        proteins_value = "N/A"
        fat_value = "N/A"
        carbohydrates_value = "N/A"
        if nutrition_values:
            # Iteriere durch jedes Element in der Ernährungstabelle
            for item in nutrition_values.find_all("div", class_="ds-col-3"):
                # Extrahiere den Nährstofftyp (z. B. kcal, Eiweiß, Fett, Kohlenhydrate)
                nutrient_type = (
                    item.find("h5").text.strip() if item.find("h5") else None
                )
                # Extrahiere den Nährstoffwert
                nutrient_value = item.contents[-1].strip() if item.contents else None
                # Weise den Werten den entsprechenden Spalten zu
                if nutrient_type == "kcal":
                    calories_match = re.search(r"(\d+,\d+|\d+)", nutrient_value)
                    calories_value = (
                        calories_match.group(1).replace(",", ".")
                        if calories_match
                        else "N/A"
                    )
                elif nutrient_type == "Eiweiß":
                    proteins_match = re.search(r"(\d+,\d+|\d+)", nutrient_value)
                    proteins_value = (
                        proteins_match.group(1).replace(",", ".")
                        if proteins_match
                        else "N/A"
                    )
                elif nutrient_type == "Fett":
                    fat_match = re.search(r"(\d+,\d+|\d+)", nutrient_value)
                    fat_value = (
                        fat_match.group(1).replace(",", ".") if fat_match else "N/A"
                    )
                elif nutrient_type == "Kohlenhydr.":
                    carbohydrates_match = re.search(r"(\d+,\d+|\d+)", nutrient_value)
                    carbohydrates_value = (
                        carbohydrates_match.group(1).replace(",", ".")
                        if carbohydrates_match
                        else "N/A"
                    )

        # Append Werte zu den Listen
        for ingredient, quantity in zip(ingredients_values, quantities_values):
            recipe_names.append(recipe_name_value)
            preptimes.append(preptime_value)
            difficulties.append(difficulty_value)
            rating_avgs.append(rating_avg_value)
            rating_counts.append(rating_count_value)
            servings_list.append(servings_value)
            menu_types.append(menu_type)
            meat_fishs.append(meat_fish)
            dietary_preferences.append(dietary_pref)
            # print (ingredient,quantity)
            count, unit = parse_quantity_and_unit(quantity)

            # print(f"input {quantity} output {count}, {unit}")
            quantities_list.append(count)
            units.append(unit)
            ingredients_list.append(ingredient)
            # print ("ingredients", ingredients_values)
            # print("quantities", quantities_values)
            calories_list.append(calories_value)
            proteins_list.append(proteins_value)
            fat_list.append(fat_value)
            carbohydrates_list.append(carbohydrates_value)
            recipe_links_list.append(recipe_link)
# Erstelle DataFrame
all_recipes_df = pd.DataFrame(
    {
        "Recipe Name": recipe_names,
        "Preptime": preptimes,
        "Difficulty": difficulties,
        "Rating Average_out_of_5": rating_avgs,
        "Rating Count": rating_counts,
        "Recipe Servings": servings_list,
        "Quantities": quantities_list,
        "Units": units,
        "Ingredients": ingredients_list,
        "Calories_in_g": calories_list,
        "Proteins_in_g": proteins_list,
        "Fat_in_g": fat_list,
        "Carbohydrates_in_g": carbohydrates_list,
        "Menu Type": menu_types,
        "Dietary Preference": dietary_preferences,
        "Meat/Fish": meat_fishs,
        "Link": recipe_links_list,
    }
)

# Display the DataFrame
print(all_recipes_df)
# Speichere DataFrame als CSV
csv_path = '/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/Recipe_dataset.csv'
all_recipes_df.to_csv(csv_path, index=False)
print(f"DataFrame saved to {csv_path}")
