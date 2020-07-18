import urllib.request
import xml.etree.ElementTree as et
import re
from recipe_scrapers import scrape_me
import json

with urllib.request.urlopen('https://www.bbc.co.uk/food/sitemap.xml') as url:
    data = url.read()

xml = et.fromstring(data)
nmspc = {"doc": "http://www.sitemaps.org/schemas/sitemap/0.9",
         "image": "http://www.google.com/schemas/sitemap-image/1.1"}

data = {'recipes': []}
recipes_counter = 0
for url in xml.findall('doc:url', namespaces=nmspc):
    loc = url.find('doc:loc', namespaces=nmspc).text
    if re.search("^https://www.bbc.co.uk/food/recipes/+", loc) and not re.search("^https://www.bbc.co.uk/food/recipes/a-z/+", loc):
        scraper = scrape_me(loc)
        recipes_counter = recipes_counter + 1
        print("{}. recipe downloaded: {}".format(recipes_counter, scraper.title()))
        print(loc)
        data['recipes'].append({
            'title': scraper.title(),
            'yields': scraper.yields(),
            'ingredients': scraper.ingredients(),
            'instruction': scraper.instructions(),
            'url': loc
        })

        with open('recipes.json', 'w') as outfile:
            json.dump(data, outfile)
