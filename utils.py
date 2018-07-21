import os
import re
import uuid
import requests

def save_from_url(url, dest_file):
    result = False

    with open(dest_file, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
        result = True

    return result

def make_dir(directory):
    result = False
    if not os.path.exists(directory):
        os.makedirs(directory)
        result = True
    return result

def make_uuid():
    result = uuid.uuid4()
    return str(result)

def normalize_name(s):
    s = s.lower()
    s = re.sub(r"\s+", '_', s)
    return s

