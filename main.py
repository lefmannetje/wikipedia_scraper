
# Imports
import requests
from pprint import pprint
import time
from bs4 import BeautifulSoup
import scraper
import sys
import json

# Just a timer to check how long the scrapper will take to finish
start_time = time.time()

# URL and endpoint definitions
root_url = "https://country-leaders.onrender.com/"
status_url = root_url + "status/"
countries_url = root_url + 'countries/'
cookie_url = root_url + 'cookie/'
leaders_url = root_url + 'leaders/'
leader_url = root_url + 'leader/'

# Create a session
session = requests.Session()

# check if status == 200 otherwise API might be down.
scraper.check_status(session, status_url)

# Get a cookie
cookies = scraper.get_cookie(session, cookie_url)

# Get a list of country-codes; like be, fr, us...
countries = scraper.get_countries(cookies, session, countries_url)

# Create an empty list so we can fill the leaders per country found.
leaders_per_country = {}

# Go through the found `countries` and name each instance `country`
for country in countries:   
    # get leader for `country` instance     
    leaders = scraper.get_leaders(country, cookies, session, leaders_url)
    # Create empty list to put in all leaders per country
    country_leaders = []
    
    # Go through list of `leaders` and make instance `leader`
    for leader in leaders:
        # Grab leader ID so we can find correct wikipedia-url
        leader_id = leader['id']
        # get Wikipedia-url for leader from API
        wiki_url = scraper.get_leader_wiki(leader_id, cookies, leader_url, session)

        # If wiki_url is returned with correct content
        if wiki_url:
            # Go to correct wikipage and find first paragraph with bold word in
            # Each wikipedia page is build up the same so we know this is the correct paragraph
            first_par = scraper.find_first_bold_paragraph(wiki_url, session)
            # Fill in the leader_info dictionaer
            leader_info = {
                'id': leader_id,
                'name': f"{leader['first_name']} {leader['last_name']}",
                'wikipedia_url': wiki_url,
                'first_paragraph': first_par['paragraph_text'] if isinstance(first_par, dict) else first_par
            }
            # Fill in `country_leaders` list with the 'leader_info' dict
            country_leaders.append(leader_info)
    
    # Fill in the `leaders_per_country` with `country` as key and `country_leaders` list as value
    leaders_per_country[country] = country_leaders

# Create a JSON from the dictionair
scraper.create_leaders_json(leaders_per_country)

# Print how long the scrapping took
end_time = time.time()
print("It took ", end_time-start_time, "seconds to scrape Wiki!")

# Read out the JSOn file // Commented out
""" 
leaders_data = scraper.read_leaders_json()
if leaders_data:
    print("Data read from leaders.json:")
    print(json.dumps(leaders_data, indent=2, ensure_ascii=False)) 
"""
