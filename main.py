import concurrent.futures
import scraper
import time
import requests
import json

# URL and endpoint definitions
root_url = "https://country-leaders.onrender.com/"
status_url = root_url + "status/"
countries_url = root_url + 'countries/'
cookie_url = root_url + 'cookie/'
leaders_url = root_url + 'leaders/'
leader_url = root_url + 'leader/'

# Create a session
session = requests.Session()

scraper.check_status(session, status_url)
cookies = scraper.get_cookie(session, cookie_url)
countries = scraper.get_countries(cookies, session, countries_url)

leaders_per_country = {}

# Define a function to process each country (to be used in parallel)
def process_country(country):
    country_leaders = []
    
    leaders = scraper.get_leaders(country, cookies, session, leaders_url)
    
    for leader in leaders:
        leader_id = leader['id']
        wiki_url = scraper.get_leader_wiki(leader_id, cookies, leader_url, session)
        
        if wiki_url:
            first_par = scraper.find_first_bold_paragraph(wiki_url, session)
            leader_info = {
                'id': leader_id,
                'name': f"{leader['first_name']} {leader['last_name']}",
                'wikipedia_url': wiki_url,
                'first_paragraph': first_par['paragraph_text'] if isinstance(first_par, dict) else first_par
            }
            country_leaders.append(leader_info)
    
    return country, country_leaders

# Use ThreadPoolExecutor to fetch leaders in parallel for each country
start_time = time.time()
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(process_country, countries)

# Combine results into the leaders_per_country dictionary
for country, leaders in results:
    leaders_per_country[country] = leaders

scraper.create_leaders_json(leaders_per_country)

end_time = time.time()
print("It took ", end_time-start_time, "seconds to scrape Wiki!")

# Read and display the data
leaders_data = scraper.read_leaders_json()
if leaders_data:
    print("Data read from leaders.json:")
    print(json.dumps(leaders_data, indent=2, ensure_ascii=False))
