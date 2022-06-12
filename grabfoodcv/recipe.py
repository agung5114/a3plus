import requests
from recipe_scrapers import scrape_html, scrape_me
import re

def scrapeRecipe(url):
    # url = f"https://www.allrecipes.com/recipe/72567/panna-cotta/"
    html = requests.get(url).content

    scraper = scrape_html(html=html, org_url=url)
    # title = scraper.title()
    # total_time=scraper.total_time()
    # yields= scraper.yields()
    ingredients =scraper.ingredients()
    ingredient = []
    for i in ingredients:
        ingredient.append(re.sub (r'([^a-zA-Z ]+?)', '', i))

    instructions = scraper.instructions()
    # links = scraper.links()
    nutrients = scraper.nutrients()

    return {'ingredient':ingredient,'instrunctions':instructions}

pcota =scrapeRecipe('https://www.allrecipes.com/recipe/72567/panna-cotta/')
print(pcota)