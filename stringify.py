import json

# A Python dictionary
data = {
    "name": "John Doe",
    "age": 30,
    "isStudent": False,
    "courses": ["Math", "Science", "History"]
}

# Stringify the dictionary to a JSON string
json_string = json.dumps(data)

# Print the JSON string
print(type(json_string))
print(json_string)