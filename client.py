import requests
from pprint import pprint
import pdb

response = requests.get(
    "https://swapi.dev/api/people/1/",
)

film_1 = response.json()["films"][0]

response = requests.get(film_1)

for character_link in response.json()["characters"]:
    # pdb.set_trace()
    response_2 = requests.get(character_link)
    character = response_2.json()
    if "vader" in character["name"].lower():
        pprint(character)

# if response.status_code != 200:
#     print(response.json()["error"])
# else:
#     print(response.json()["result"])
