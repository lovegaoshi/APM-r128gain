import requests
import json
import sys
import gzip

if __name__ == "__main__":

    res = requests.get(sys.argv[1]).json()
    with open('rules.json', 'w', encoding='utf-8') as f:
        json.dump(res, f)
    with gzip.open('rules.gzip', 'wb') as gf:
        gf.write(gzip.compress(bytes(json.dumps(res), 'utf-8')))
