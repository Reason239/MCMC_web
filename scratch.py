import requests

# Create a dictionary containing the form elements and their values
data = {"state": "ca", "population": 100}

# POST to the remote endpoint. The Requests library will encode the
# data automatically
r = requests.post("http://example.com/showtree.js", data=data)

# Get the raw body text back
body_data = r.text

print(body_data)

