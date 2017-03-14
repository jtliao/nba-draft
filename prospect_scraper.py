from bs4 import BeautifulSoup
import requests
import re
import json

prospect_to_docs = {}

#page of the top 100 prospects
profile_urls = []
for page in range(1, 5):
    url = "http://www.draftexpress.com/rankings/Top-100-Prospects/" + str(page)
    
    r = requests.get(url)
    data = r.text
    
    soup = BeautifulSoup(data, "html.parser")
    
    profile_urls.extend([tag["href"] for tag in soup.find_all(name="a", href=re.compile(r"\/profile\/.+"))])

for profile_url in profile_urls:
    player_name = re.findall(r"\/profile\/([^\/]+)", profile_url)[0]
    player_name = " ".join(re.split(r"-", player_name)[:-1])
    print(player_name)

    full_profile_url = "http://www.draftexpress.com" + str(profile_url)
    profile_r = requests.get(full_profile_url)
    profile_data = profile_r.text

    profile_soup = BeautifulSoup(profile_data, "html.parser")
    # print(profile_soup.prettify())
    # print(profile_soup.get_text())

    text = []
    for p in profile_soup.find_all(name="p"):
        # print(p)
        if p.parent.name == "div" and "item" in p.parent["class"]:
            text.append(p.get_text())
    print(text)

    prospect_to_docs[player_name] = text

with open("prospect_to_docs.json", "w") as f:
    json.dump(prospect_to_docs, f)
    