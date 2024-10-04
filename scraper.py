import requests
from bs4 import BeautifulSoup
import time
import json


def check_status(session, status_url):
    try:
        response = session.get(status_url)
        # response = requests.get(status_url)
        if response.status_code == 200:
            print("Success:", response.status_code)
            return True
        else:
            print("Error:", response.status_code)
            return False
    except requests.ConnectionError as e:
        print(f"ConnectionError: {e}")
    finally:
        # Close the session after use
        session.close()

def get_cookie(session, cookie_url):
    response = session.get(cookie_url)
    return response.cookies if response.status_code == 200 else print("Failed to get cookie")

def get_countries(cookies, session, countries_url):
    response = session.get(countries_url, cookies=cookies)
    return response.json() if response.status_code == 200 else []

def get_leaders(country, cookies, session, leaders_url):
    response = session.get(leaders_url, params={'country': country}, cookies=cookies)
    return response.json() if response.status_code == 200 else []

def get_leader_wiki(leader_id, cookies, leader_url, session):
    response = session.get(leader_url, params={'leader_id': leader_id}, cookies=cookies)
    return response.json()['wikipedia_url'] if response.status_code == 200 else None

def find_first_bold_paragraph(wiki_url, session):
    response = session.get(wiki_url)
    if response.status_code != 200:
        return "Failed to fetch Wikipedia page"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    
    for paragraph in paragraphs:
        if paragraph.find('b'):
            return {
                'paragraph_text': paragraph.text.strip(),
            }
    
    return "No paragraph found with bold text."

def create_leaders_json(leaders_per_county):
    # Serialize the dictionary to a JSON string
    json_data = json.dumps(leaders_per_county, ensure_ascii=False, indent=2)
    
    # Write the JSON string to a file
    with open('leaders.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
    
    print("leaders.json file has been created successfully.")

def read_leaders_json():
    try:
        # Open and read the JSON file
        with open('leaders.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("Error: leaders.json file not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON in leaders.json file.")
        return None