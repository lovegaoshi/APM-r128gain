import requests
import json
import sys

if __name__ == "__main__":

    with open('rules.json', 'w', encoding='utf-8') as f:
        res = requests.get(sys.argv[1]).json()
        json.dump(res, f)
