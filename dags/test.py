import json


with open("../data/github_data.json",'r') as file:
    f=dict(json.load(file))
    
ee=f.get('organization',{})\
                .get('projectV2',{})\
                .get('items')
print(ee['nodes'][1])