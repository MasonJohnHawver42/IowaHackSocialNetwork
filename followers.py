import requests
from pprint import pprint

import os
from dotenv import load_dotenv
load_dotenv()

key = os.environ.get("KEY")

print(key)
username = "MasonJohnHawver42"

headers = {'Authorization': 'token ' + key}

url = "https://api.github.com/users/{}/starred".format(username)

# url = f"https://api.github.com/users/{username}"
#url = f"https://api.github.com/users/{username}/repos"
url = "https://api.github.com/repos/MasonJohnHawver42/emscripten"

data = requests.get(url, headers=headers).json()

pprint(data)

# for follower in data:
#     pprint(follower)
