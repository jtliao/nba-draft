from bs4 import BeautifulSoup
import requests
import re
import json
import nltk

prospect_to_docs = {}
prospect_to_position = {}

#page of the top 100 prospects
profile_urls = set()
url = "http://www.nbadraft.net/ranking/bigboard"
    
r = requests.get(url)
data = r.text
    
soup = BeautifulSoup(data, "html.parser")
    
profile_urls = [tag["href"] for tag in soup.find_all(name="a", href=re.compile(r"\/players\/.+"))]
                # if "/stats" not in tag["href"] and "/videos" not in tag["href"]}

# print(profile_urls)

valid1_count = 0
valid2_count = 0

player_to_strengths = {}
player_to_weaknesses = {}

# for profile_url in [profile_urls[91]]:
for i, profile_url in enumerate(profile_urls):
    # print(profile_url)
    player_name = re.findall(r"\/players\/([^\/]+)", profile_url)[0]
    player_name = " ".join(re.split(r"-", player_name))
    # print(player_name)

    full_profile_url = "http://www.nbadraft.net" + str(profile_url)
    profile_r = requests.get(full_profile_url)
    profile_data = profile_r.text

    profile_soup = BeautifulSoup(profile_data, "html.parser")
    
    # m = re.search('Position:\s(\S+)', profile_soup.get_text())
    # prospect_to_position[player_name] = m.group(1)


    for div in profile_soup.find_all(id="nbap_content_bottom"):    
        # for child in div.children:
        if len(div.contents) <= 3:
            print("%d. INVALID: %s" % (i+1, player_name))
            break
        child = div.contents[3]
        # print(child)
        # break

        if (child.name == "p" and len(child.contents) >= 8 and child.contents[0].name == "strong" 
            and "Strengths:" in child.contents[0].get_text()):
            valid1_count += 1
            # print("VALID: " + player_name)
            # print([c.name for c in child.contents])

            # ASSUMES THAT child.contents[0] is <strong>Strengths:</strong>
            # child.contents[1] is text for 'Strengths'
            # child.contents[6] is <strong>Weaknesses:</strong>
            # child.contents[7] is text for 'Weaknesses'

            strengths_text = child.contents[1].encode("utf-8")
            cleaned_strengths = re.sub(r'\.\.\.', '', strengths_text)
            weaknesses_text = child.contents[7].encode("utf-8")
            cleaned_weaknesses = re.sub(r'\.\.\.', '', weaknesses_text)
            # print(strengths_text)
            # print
            # print(weaknesses_text)
            # print
            # print
            player_to_strengths[player_name] = cleaned_strengths
            player_to_weaknesses[player_name] = cleaned_weaknesses
            break


        elif (child.name == "p" and len(child.contents) >= 0 
                and child.contents[0].name == "strong" and "Strengths:" in child.contents[0].get_text()
                and child.next_sibling.next_sibling is not None and child.next_sibling.next_sibling.contents[0].name == "strong"
                and "Weaknesses:" in child.next_sibling.next_sibling.contents[0].get_text()):

            # print("VALID2: " + player_name)
            valid2_count += 1
            strengths_text = child.contents[1].encode("utf-8")
            cleaned_strengths = re.sub(r'\.\.\.', '', strengths_text)
            weaknesses_text = child.next_sibling.next_sibling.contents[1].encode("utf-8")
            cleaned_weaknesses = re.sub(r'\.\.\.', '', weaknesses_text)
            # print(strengths_text)
            # print
            # print(weaknesses_text)
            # print
            # print
            player_to_strengths[player_name] = cleaned_strengths
            player_to_weaknesses[player_name] = cleaned_weaknesses
            break

        else:
            # print(child)
            # pass
            print("%d. INVALID: %s" % (i+1, player_name))


print(valid1_count)
print(valid2_count)
        # cleaned = re.sub(r'<.+>', '', a.get_text())
        # cleaned = re.sub(r'<div>.+<\/div>', '', cleaned)
        # cleaned = re.sub(r"\([\S\s]+\)", "", cleaned)
        # cleaned = cleaned.replace("-", " ")
        # cleaned = cleaned.replace("#", "")
        # cleaned = cleaned.replace("%", "")
        # cleaned = cleaned.replace("Please enable Javascript to watch this video", "")
        # text += cleaned

        #if a.parent.name == "div" and "item" in p.parent["class"]:
        #    text.append(a.get_text())


with open("nbadraftnet_prospect_to_strengths.json", "w") as f:
    json.dump(player_to_strengths, f)

with open("nbadraftnet_prospect_to_weaknesses.json", "w") as f:
    json.dump(player_to_weaknesses, f)