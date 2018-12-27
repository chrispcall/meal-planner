from bs4 import BeautifulSoup
import requests
import logging
logger = logging.getLogger(__name__)

def ingredients_from_web(url):
    ingredients = []

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    if 'skinnytaste' in url:
        logging.debug('Parsing Skinny Taste Recipe')
        ingredient_tags = soup.find_all(class_='ingredient')
        li_tags = soup.find('div', {'class': 'ingredients'}).find_all('li')
        if ingredient_tags:
            for i in ingredient_tags:
                ingredients.append(''.join(i.findAll(text=True)).replace(',', ''))
        elif li_tags:
            for i in li_tags:
                ingredients.append(''.join(i.findAll(text=True)).replace(',', ''))
    elif 'allrecipes' in url:
        logging.debug('Parsing All Recipes Recipe')
        for i in soup.find_all(class_='recipe-ingred_txt added'):
            ingredients.append(''.join(i.findAll(text=True)).replace(',', ''))
    elif 'foodnetwork' in url:
        logging.debug('Parsing Food Network Recipe')
        for i in soup.find_all(class_='o-Ingredients__a-Ingredient'):
            ingredients.append(''.join(i.findAll(text=True)).replace(',', ''))
    else:
        logging.debug('URL PARSER - No URL found so we will not parse ingredients')
        return ""

    return ",".join(ingredients)

