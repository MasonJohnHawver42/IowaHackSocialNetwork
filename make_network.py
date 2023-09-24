import csv
import requests

import os
from dotenv import load_dotenv
load_dotenv()

key = os.environ.get("KEY")

headers = {'Authorization': 'token ' + key}

hacker_set = set()
one_degree = set()

graph = {}
edges = {}

def add_node(username, name):

    global graph, headers
    url = f"https://api.github.com/users/{username}"
    data = requests.get(url, headers=headers).json()


    if 'message' in data:
        print("msg:", data["message"])
        return -1

    if data["name"] == None:
        data["name"] = name

    if data["id"] not in graph:
        graph[data["id"]] = data
            
    return data["id"]

def add_edge(to_id, from_id):
    if from_id not in edges:
        edges[from_id] = set()
    
    edges[from_id].add(to_id)

def add_edges():

    global graph, hacker_set

    for i, user_id in enumerate(hacker_set):

        username = graph[user_id]["login"]
        print(username, i, len(hacker_set))

        in_url = f"https://api.github.com/users/{username}/followers"
        out_url = f"https://api.github.com/users/{username}/following"
        star_url = f"https://api.github.com/users/{username}/starred"
        repo_url = f"https://api.github.com/users/{username}/repos"
        follower_data = requests.get(in_url, headers=headers).json()

        for follower in follower_data:
            
            follower_name = follower["login"]
            follower_id = follower["id"]

            if follower_id not in graph:
                add_node(follower_name, follower_name)
            
            add_edge(user_id, follower_id)
            # edges.append({"to": user_id, "from": follower_id})

        # following_data = requests.get(out_url, headers=headers).json()
        # # print(out_url, following_data)
        # for following in following_data:
            
        #     follower_name = following["login"]
        #     follower_id = following["id"]

        #     # print("name", follower_name)

        #     if follower_id not in graph:
        #         add_node(follower_name, follower_name)
            
        #     add_edge(follower_id, user_id)

        #     if follower_id not in hacker_set:
        #         one_degree.add(follower_id)
        #     # edges.append({"from": user_id, "to": follower_id})
        
        # star_data = requests.get(star_url, headers=headers).json()

        # for star in star_data:
        #     if star['owner']['login'] != username:
        #         if star['owner']['id'] not in graph:
        #             add_node(star['owner']['login'], star['owner']['login'])
            
        #         add_edge(user_id, star['owner']['id'])
        
        repo_data = requests.get(repo_url, headers=headers).json()

        for repo in repo_data:
            
            repo_name = repo["name"]

            if repo["fork"]:
                continue

            contrib_url = f"https://api.github.com/repos/{username}/{repo_name}/contributors"
            # print("here", contrib_url)
            contrib_data = requests.get(contrib_url, headers=headers)

            if (len(contrib_data.text) == 0):
                continue

            # print("here2", len(contrib_data.text), contrib_data.url)
            # .json()

            # print(repo_name, repo["owner"])

            contrib_data = contrib_data.json()

            contrib_ids = set()
            contrib_ids.add(user_id)



            for contrib_user in contrib_data:
                if contrib_user['login'] != username:
                    if contrib_user['id'] not in graph:
                        add_node(contrib_user['login'], contrib_user['login'])
                
                    contrib_ids.add(contrib_user['id'])

                    add_edge(user_id, contrib_user['id'])
                    
                    if contrib_user['id'] not in hacker_set:
                        one_degree.add(contrib_user['id'])
    
    for i, user_id in enumerate(one_degree):

        username = graph[user_id]["login"]
        print(username, i, len(one_degree))

        in_url = f"https://api.github.com/users/{username}/followers"
        out_url = f"https://api.github.com/users/{username}/following"
        star_url = f"https://api.github.com/users/{username}/starred"
        repo_url = f"https://api.github.com/users/{username}/repos"
        
        repo_data = requests.get(repo_url, headers=headers).json()

        for repo in repo_data:
            
            repo_name = repo["name"]

            if repo["fork"]:
                continue

            contrib_url = f"https://api.github.com/repos/{username}/{repo_name}/contributors"
            # print("here", contrib_url)
            contrib_data = requests.get(contrib_url, headers=headers)

            if (len(contrib_data.text) == 0):
                continue

            # print("here2", len(contrib_data.text), contrib_data.url)
            # .json()

            # print(repo_name, repo["owner"])

            contrib_data = contrib_data.json()

            contrib_ids = set()
            contrib_ids.add(user_id)

            for contrib_user in contrib_data:
                try:
                    if contrib_user['login'] != username:
                        if contrib_user['id'] not in graph and contrib_user['id'] in hacker_set:
                            add_node(contrib_user['login'], contrib_user['login'])
                    
                        contrib_ids.add(contrib_user['id'])

                        add_edge(user_id, contrib_user['id'])
                except:
                    print("ERROR")

                


def gen_javascript():

    #    { id: 5, shape: "circularImage", image: DIR + "5.png" },

    global graph, edges

    nodes = []
    edges_lines = []
    data_lines = []

    for user_id, data in graph.items():
        node_id = data["id"]
        img = data["avatar_url"]
        name = data["name"]
        uname = data["login"]
        email = data["email"]
        js_code = f"""id: {node_id}, shape: "circularImage", image: "{img}\", label: "{name}" """
        nodes.append("{" + js_code + "}")
        js_code = f"""name: "{name}", username: "{uname}", email: "{email}" """
        data_lines.append(f"""data.set({user_id}, {"{" + js_code + "}"}); """)

    
    # { from: 1, to: 2 },

    for from_id, to_set in edges.items():
        for to_id in to_set:
            js_code = f""" to: {to_id}, from: {from_id}"""
            edges_lines.append("{" + js_code + "}")
    
    print("nodes = [{}];".format(", ".join(nodes)))
    print("edges = [{}];".format(", ".join(edges_lines)))
    print("data = new Map(); {}" .format(" ".join(data_lines)))


user_id = add_node("MasonJohnHawver42", "Mason Hawver")
if user_id != -1:
    hacker_set.add(user_id)

with open("data.csv", mode = 'r') as file:
    csv_file = csv.reader(file)
    next(csv_file)

    for line in csv_file:
        # print(line)
        user_id = add_node(line[0], line[1])
        if user_id != -1:
            hacker_set.add(user_id)

add_edges()
gen_javascript()
