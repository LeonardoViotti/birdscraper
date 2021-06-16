import os
try:
    with open(os.path.join("../data/get_request.txt", 'get_request.txt'), 'r') as file:
        REQUEST_URL = file.read()
except SystemExit:    #This means that the file does not exist (or some other IOError)
    print("get_request.txt file not found! Make sure it is on the file specifiec in --urls_path.")

print(REQUEST_URL)

print("Done")
