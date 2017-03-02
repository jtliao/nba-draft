from bs4 import BeautifulSoup
import requests
import re
import json

# All years in which draft has already happened and they have player descriptions
# for year in range(1994, 2017):

player_to_docs = {}

# Just start with years 2005-2016
for year in range(2005, 2017):
# for year in [2016]:
    url = "http://www.draftexpress.com/nba-draft-history/?syear=" + str(year)
    # print(url)

    r = requests.get(url)
    data = r.text

    soup = BeautifulSoup(data, "html.parser")
    # print(soup.prettify())

    profile_urls = []
    for possible_player in soup.find_all(name="a", href=re.compile(r"\/profile\/.+")):
        if (possible_player.parent.name == "td" and "class" in possible_player.parent.attrs
            and "columna-4" in possible_player.parent["class"]):
            # print("HERE")
            profile_urls.append(possible_player["href"])
    print(profile_urls)

    for profile_url in profile_urls:
    # for profile_url in [profile_urls[0]]:
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
        player_to_docs[player_name] = text

with open("player_to_docs.json", "w") as f:
    json.dump(player_to_docs, f)