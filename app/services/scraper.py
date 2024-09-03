import requests
from bs4 import BeautifulSoup

# def get_html(url):
#     response = requests.get(url)
#     return response.content

def find_bosses(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # boss_names = []

    # for boss in soup.find_all('p', class_='boss-name'):
    #     boss_names.append(boss.text.strip())
    
    # return boss_names

    bosses = {} # key: boss name, value: tier level
    boss_names = []

    header_lis = soup.find_all('li', class_='header-li')
    
    for header_li in header_lis:
        # get tier level first
        tier_level = header_li.find('h2', class_='boss-tier-header').text.strip()

        if tier_level: # if this header-li HAS a tier level
            boss_names = [] # reset
            next_elem = header_li.find_next_sibling()

            # while next element IS NOT the next header-li
            while (next_elem) and ('header-li' not in next_elem.get('class', [])):
                # checking that it's the element we want
                if next_elem.name == 'li' and 'boss-item' in next_elem.get('class', []):
                    boss_name = next_elem.find('p', class_='boss-name').text.strip()
                    boss_names.append(boss_name)

                next_elem = next_elem.find_next_sibling()
            
            bosses[tier_level] = boss_names
    
    return bosses




'''
HTML STRUCTURE ON LEEKDUCK:
<li class="header-li">
    <h2 class="boss-tier-header tier-1">TIER 1</h2>
</li>
<li class="boss-item>
    <div class="boss-border">
        <div class="boss-1">
            <p class="boss-name">STARYU</p>
        </div>
    </div>
</li>
<li class="boss-item>
    <div class="boss-border">
        <div class="boss-1">
            <p class="boss-name">ARON</p>
        </div>
    </div>
</li>
<li class="header-li">
    <h2 class="boss-tier-header tier-3">TIER 3</h2>
</li>
<li class="boss-item>
    <div class="boss-border">
        <div class="boss-1">
            <p class="boss-name">LAPRAS</p>
        </div>
    </div>
</li>
'''
