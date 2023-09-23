import requests
from pprint import pprint

key = "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"
username = "MasonJohnHawver42"

url = "https://api.github.com/users/{}/followers".format(username)

data = requests.get(url).json()

for follower in data:
    pprint(follower["login"])
