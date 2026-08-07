import json
import os
import sys
import requests
#bloco de logica de negocios
def get_activity(username):
    url = "https://api.github.com/users/"+username+"/events"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return ""

def parse_activity(response):
    if response == "":
        print("Request failed!")
        sys.exit(1)
    # Extract all actions from the response
    try:
        actions = [(event["type"], event["repo"]["name"]) for event in response]
        # Get the action of the very first event
        #first_action = response[0]["type"]
    except KeyError:
        print("key error")
        sys.exit(1)

    tuple_counts= {}
    for action in actions:
        if action in tuple_counts:
            tuple_counts[action] +=1
        else:
            tuple_counts[action] = 1
    for key in tuple_counts.keys():
        if key[0] == "PushEvent":
            print("Pushed  ",tuple_counts[key],"commits to ",key[1])
        if key[0] == "CreateEvent":
            print("Created ",tuple_counts[key],"new breanch(es): ",key[1])
        if key[0] == "IssuesEvent":
            print("Opened  ",tuple_counts[key],"new issue(s) to ",key[1])
        if key[0] == "PullRequestEvent":
            print("Created ",tuple_counts[key], "pull request(s) to ",key[1])
        if key[0] == "PublicEvent":
            print("Changed ",key[1], "repository to public")
    #print(tuple_counts.keys())



def load_json_for_test():
    if not os.path.exists("test.json"):
        return {}
    try:
        with open("test.json", "r", encoding="utf-8") as f:
            data =  json.load(f)
            return data
    except (json.JSONDecodeError, PermissionError):
        print(" Warning: Storage file is corrupted or inaccessible. Starting with an empty task list.")
        return {}
   

# bloco de roteamento de comandos
def main():
    args = sys.argv[1:]

    try:
        username = args[0]
    except IndexError:
        print("Error: username not provided")
        sys.exit(1)
    if len(args) >1:
        print("provide just one username")
        sys.exit(1)
    parse_activity(get_activity(username))
if __name__ == "__main__":
    main()
