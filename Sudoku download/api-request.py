import requests
import json
import hashlib

difficulties = ("easy","medium","hard","random")
url = 'https://sugoku.herokuapp.com/board?difficulty={0}'

how_many = 100
the_json = {}
old_json = {}
with open('Sudokus.json','r') as file_r:
    old_json = json.load(file_r)


for i in range(how_many - len(old_json)):
    result = requests.get(url.format(difficulties[0]))
    json_s = json.dumps(result.json(), sort_keys=True)
    # print(json_s)
    hash_v = hashlib.sha256(json_s.encode('utf-8')).hexdigest()[:16]
    the_json[hash_v] = result.json()
    print(hash_v)

new_json = {**old_json,**the_json}

with open('Sudokus.json', 'w') as f:
    json.dump(new_json, f)