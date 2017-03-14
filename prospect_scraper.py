from bs4 import BeautifulSoup
import requests
import re
import json

prospect_to_docs = {}

#page of the top 100 prospects
profile_urls = set()
url = "http://www.draftexpress.com/rankings/Top-100-Prospects/#list"
    
r = requests.get(url)
data = r.text
    
soup = BeautifulSoup(data, "html.parser")
    
profile_urls = {tag["href"] for tag in soup.find_all(name="a", href=re.compile(r"\/profile\/.+")) 
                if "/stats" not in tag["href"] and "/videos" not in tag["href"]}

for profile_url in profile_urls:
    player_name = re.findall(r"\/profile\/([^\/]+)", profile_url)[0]
    player_name = " ".join(re.split(r"-", player_name)[:-1])
    print(player_name)

    full_profile_url = "http://www.draftexpress.com" + str(profile_url)
    profile_r = requests.get(full_profile_url)
    profile_data = profile_r.text

    profile_soup = BeautifulSoup(profile_data, "html.parser")

    text = []
    for a in profile_soup.find_all(class_="article-content"):    
        cleaned = re.sub(r'<.+>', '', a.get_text())
        cleaned = re.sub(r'<div>.+<\/div>', '', cleaned)
        text.append(cleaned)
        #if a.parent.name == "div" and "item" in p.parent["class"]:
        #    text.append(a.get_text())

    prospect_to_docs[player_name] = text

with open("prospect_to_docs.json", "w") as f:
    json.dump(prospect_to_docs, f)
    
    