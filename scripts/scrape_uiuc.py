import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_uiuc():
    url = "https://m-selig.ae.illinois.edu/ads/coord_database.html"
    base_url = "https://m-selig.ae.illinois.edu/ads/"
    
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch UIUC database index.")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    airfoils = []
    
    # The airfoils are in a pre tag or table usually
    # Looking at the site structure, it's a table or list of links
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('coord/') and href.endswith('.dat'):
            name = link.text.strip()
            if not name:
                name = href.split('/')[-1].replace('.dat', '')
            airfoils.append({
                "name": name,
                "url": base_url + href
            })
    
    # Save to JSON
    output_path = "/home/ubuntu/naca-airfoil-kit/uiuc_database.json"
    with open(output_path, 'w') as f:
        json.dump(airfoils, f, indent=4)
    
    print(f"Scraped {len(airfoils)} airfoils and saved to {output_path}")

if __name__ == "__main__":
    scrape_uiuc()
