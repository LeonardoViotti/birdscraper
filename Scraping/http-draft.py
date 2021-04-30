import requests
import json
import os

with open('get_request.txt', 'r') as file:
    request_str = file.read()

res = requests.get(request_str,  verify=False)

res.text
json_data = json.loads(res.text)

# Print pretty JSON
json_formatted_str = json.dumps(json_data, indent=2)
print(json_formatted_str)

# session = requests.Session()
# session.get(request_str,  verify=False)