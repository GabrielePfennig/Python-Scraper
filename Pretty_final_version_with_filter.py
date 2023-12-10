# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 12:10:30 2023

@author: Sebastian Schachtner
"""

import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse

url = "https://www.chefkoch.de/rezepte/"

# Fetch the HTML content of the website
response = requests.get(url)
html_content = response.text

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all 'a' tags with 'href' attribute in the specified div
href_elements = soup.select('ul#recipe-tag-list a.sg-pill')

# Extract the 'href' values
href_values = [element['href'] for element in href_elements]

# Iterate over pages and construct URLs
checked_urls = []  # List to store checked URLs

for href_value in href_values[:5]:
    for count_cat_inner in range(1):  # You can adjust the range of pages within the cathegories as needed for a full check insert 'len(href_values)'
        cathe_base_url = 'https://www.chefkoch.de' + href_value.replace('0', '{}', 1)
        url = cathe_base_url.format(count_cat_inner)
        
        response = requests.get(url, allow_redirects=False)  # Disable automatic redirection
        redirected_url = response.headers.get('Location', '')  # Use get method to avoid KeyError
        original_parts = urlparse(url)
        redirected_parts = urlparse(redirected_url)
            
        # Compare the parts up to the third "/"
        original_path = original_parts.path.split('/')
        redirected_path = redirected_parts.path.split('/')

        if response.status_code == 301 and original_path[:3] != redirected_path[:3]:
            print(f"URL {url} is redirected.")
            break
        
        elif response.status_code == 301:
            print(f"URL {url} is redirected and available.")
            
        elif response.status_code == 200:
            print(f"URL {url} is available.")
            checked_urls.append(url)
        else:
            print(f"URL {url} is not available. Stopping.")
            break

# Print the checked URLs
for checked_url in checked_urls:
    print(checked_url)


count_limit = 1  # Set the limit for the number of recipe links to extract from each page in checked_urls
recipe_links = []  # List to store recipe links

# Create a directory to store the text files
recipe_pages_directory = 'C:/Users/Sebastian Schachtner/Documents/01_Studium/02_Master/3rd Semester/06_Webscraping & Textual Analysis in Python'
os.makedirs(recipe_pages_directory, exist_ok=True)

# Loop through each checked URL to extract recipe links and save text content to files
for checked_url in checked_urls:
    response = requests.get(checked_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Select recipe links using BeautifulSoup
    links = soup.select('.ds-recipe-card__link.ds-teaser-link')
    count_rec = 0

    # Loop through each recipe link
    for link in links:
        if count_rec >= count_limit:
            print(f"Stopping loop. Count_rec reached {count_limit}.")
            break

        # Extract the href attribute from the link
        recipe_link = link['href']

        # Check if the recipe link is not already in the set
        if recipe_link not in recipe_links:
            # Check the response status of the recipe link
            recipe_response = requests.get(recipe_link)

            if recipe_response.status_code == 200 or recipe_response.status_code == 301:
                recipe_links.append(recipe_link)
                count_rec += 1

                # Save text content to files
                filename = os.path.join(recipe_pages_directory, f'recipe_{len(recipe_links)}.txt')
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(recipe_response.text)
                print(f"Recipe link {recipe_link} is available. Text content saved to {filename}")
            else:
                print(f"Recipe link {recipe_link} is not available.")

        if count_rec >= count_limit:
            break

print("\nRecipe Links:")
for recipe_link in recipe_links:
    print(recipe_link)


import pandas as pd
import re


def extract_quantity_and_unit(input_string):
    # Define a regular expression pattern to match quantity and unit
    pattern = re.compile(r"(?P<quantity>\d*\.?\d+)\s*(?P<unit>\w*)")

    # Use the regular expression to find matches in the input string
    match = pattern.match(input_string)

    # If there is a match, extract the quantity and unit
    if match:
        quantity = match.group("quantity")
        unit = match.group("unit")
        return quantity, unit
    else:
        return "etwas", None


# Initializing lists for the recipes data
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
for recipe_link in recipe_links:
    # Send a request to the recipe page
    response_recipe = requests.get(recipe_link, timeout=120)
    soup_recipe = BeautifulSoup(response_recipe.content, "html.parser")
    # Ensure the request was successful (Status code 200)
    if response_recipe.status_code == 200 or response.status_code == 301:
        print(f"Request to {recipe_link} successful.")
        # Extract HTML content
        html_content_recipe = response_recipe.text
        # Use Beautiful Soup to analyze the HTML content
        soup_recipe = BeautifulSoup(html_content_recipe, "html.parser")
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
        # Initialize new column values
        calories_value = "N/A"
        proteins_value = "N/A"
        fat_value = "N/A"
        carbohydrates_value = "N/A"
        if nutrition_values:
            # Iterating through each element in the nutrition table
            for item in nutrition_values.find_all("div", class_="ds-col-3"):
                # Extrahiere den Nährstofftyp (z. B. kcal, Eiweiß, Fett, Kohlenhydrate)
                nutrient_type = (
                    item.find("h5").text.strip() if item.find("h5") else None
                )
                # Extract the nutritional value
                nutrient_value = item.contents[-1].strip() if item.contents else None
                # Assign the values to the corresponding columns
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

        # Append values to the lists
        for ingredient, quantity in zip(ingredients_values, quantities_values):
            recipe_names.append(recipe_name_value)
            preptimes.append(preptime_value)
            difficulties.append(difficulty_value)
            rating_avgs.append(rating_avg_value)
            rating_counts.append(rating_count_value)
            servings_list.append(servings_value)
            count, unit = extract_quantity_and_unit(quantity)
            quantities_list.append(count)
            units.append(unit)
            ingredients_list.append(ingredient)
            calories_list.append(calories_value)
            proteins_list.append(proteins_value)
            fat_list.append(fat_value)
            carbohydrates_list.append(carbohydrates_value)
            recipe_links_list.append(recipe_link)
# Create the dataframe
all_recipes_df = pd.DataFrame(
    {
        "Recipe Name": recipe_names,
        "Preptime_in_min": preptimes,
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
        "Link": recipe_links_list,
    }
)

# Display the DataFrame
print(all_recipes_df.head())
# Save the dataframe as a CSV file
csv_path='C:/Users/craco/Outputs Web Scraping/Recipe_dataset.csv'

#Initiate the corresponding_recipes dataframe
corresponding_recipes=[]

#Ask the user which ingredients he wants to use
Requested_ingredients=input("Which ingredients do you have?")

##Turn the Requested_ingredients string into a list
Requested_ingredients_list = Requested_ingredients.split(",")

#Set up a filter that selects only recipes containing the specified ingredients
filtered_df = (
    all_recipes_df.groupby("Recipe Name")["Ingredients"]
    .apply(lambda x: all(ingredient in set(x) for ingredient in Requested_ingredients_list))
    .reset_index()
)

filtered_df = filtered_df[filtered_df["Ingredients"]]

#Apply the filter to the dataset, and print the 10 first rows of the new dataset
new_df = all_recipes_df.set_index("Recipe Name")
corresponding_recipes = new_df.loc[filtered_df["Recipe Name"]].reset_index()
corresponding_recipes.head(10)

##Save the filtered dataframe as a CSV file
corresponding_recipes.to_csv(csv_path, index=False)
print(f"Filtered dataFrame saved to {csv_path}")
