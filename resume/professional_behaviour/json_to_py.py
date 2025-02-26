import json

# Path to your JSON file
json_file_path = "prof.json"

# Read JSON data from the file and convert it to a Python dictionary
with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Now `data` is a Python dictionary
print("Loaded Data:")
print(data)

# Save the dictionary to a .py file
output_py_file_path = "linkedin_data.py"
with open(output_py_file_path, "w", encoding="utf-8") as output_file:
    output_file.write(f"linkedin_data = {data}")

print(f"\nData saved to {output_py_file_path}")