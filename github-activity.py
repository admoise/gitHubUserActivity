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
        actions=[]
        #actions = [(event["type"], event["repo"]["name"]) for event in response]
        for event in response:
            if "action" in event["payload"].keys():
                actions.append([event["payload"]["action"], event["repo"]["name"]])

        # Get the action of the very first event
        #first_action = response[0]["type"]
        return actions
    except KeyError:
        print("key error")

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
    #print(get_activity(username))
    #print(parse_activity(load_json_for_test()))
    print(parse_activity(get_activity(username)))
if __name__ == "__main__":
    main()
