from bs4 import BeautifulSoup
import requests
import re
import json
import sys

# All years in which draft has already happened and they have player descriptions
# for year in range(1994, 2017):


# sys.stdout = open("out.text", "w")


player_to_docs = {}
player_to_position = {}

invalid_names = []
blank_descriptions = []


# Just start with years 2005-2016
for year in range(2005, 2017):
# for year in [2016]:
#     url = "http://www.draftexpress.com/nba-draft-history/?syear=" + str(year)
    url = "http://www.draftexpress.com/nba-mock-history/" + str(year) + "/all/all/"

    r = requests.get(url)
    data = r.text

    soup = BeautifulSoup(data, "html.parser")
    # print(soup.prettify())

    profile_urls = []
    for possible_player in soup.find_all(name="a", href=re.compile(r"\/profile\/.+")):
        if (possible_player.parent.name == "td" and "class" in possible_player.parent.attrs
            and "key" in possible_player.parent["class"] and "text" in possible_player.parent["class"]):
            # print("HERE")
            profile_urls.append(possible_player["href"])


    for profile_url in profile_urls:
    # for profile_url in [profile_urls[0]]:
        player_name = re.findall(r"\/profile\/([^\/]+)", profile_url)[0]

        split_player_name = re.split(r"-", player_name)[:-1]

        if len(split_player_name) == 0 or len(split_player_name) == 1:
            invalid_names.append(profile_url)

        player_name = " ".join(split_player_name)


        full_profile_url = "http://www.draftexpress.com" + str(profile_url)
        profile_r = requests.get(full_profile_url)
        profile_data = profile_r.text

        profile_soup = BeautifulSoup(profile_data, "html.parser")
        # print(profile_soup.prettify())
        # print(profile_soup.get_text())

        # text = []
        # for p in profile_soup.find_all(name="p"):
        #     # print(p)
        #     if p.parent.name == "div" and "item" in p.parent["class"]:
        #         text.append(p.get_text())
        
        m = re.search('Position:\s(\S+)', profile_soup.get_text())
        player_to_position[player_name] = m.group(1)

        text = []
        for a in profile_soup.find_all(class_="article-content"):
            cleaned = re.sub(r'<.+>', '', a.get_text())
            cleaned = re.sub(r'<div>.+<\/div>', '', cleaned)
            cleaned = re.sub(r"\([\S\s]+\)", "", cleaned)
            cleaned = cleaned.replace("-", " ")
            cleaned = cleaned.replace("#", "")
            cleaned = cleaned.replace("%", "")
            cleaned = cleaned.replace("Please enable Javascript to watch this video", "")
            text.append(cleaned.encode("utf-8"))

        if len(text) == 0:
            blank_descriptions.append(profile_url)

        # Try unifying all the articles into a single long doc
        player_to_docs[player_name] = " ".join(text)

with open("curr_player_to_docs_unicode.json", "w") as f:
    json.dump(player_to_docs, f)
    
with open("curr_player_to_position.json", "w") as f:
    json.dump(player_to_position, f)

# with open("invalid_names.json", "w") as f:
#     json.dump(invalid_names, f)
#
# with open("blank_descriptions.json", "w") as f:
#     json.dump(blank_descriptions, f)


# sys.stdout.close()