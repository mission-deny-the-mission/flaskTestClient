import requests
import json
import random
import string

addressfile = open("server.url", 'r')
address = addressfile.read().strip()
addressfile.close()

def upload_file(workspace, filename, password):
    file = open(filename, 'rb')
    response = requests.post("http://{0}/upload/{1}/{2}/{3}".format(address, workspace, password, filename), data=file)
    file.close()
    if response.status_code == 401:
        raise Exception("Incorrect password for workspace")
    if response.status_code not in [201, 200]:
        raise Exception("bad status code: {0}".format(response.status_code))

def make_workspace(password):
    response = requests.get("http://{0}/register/{1}".format(address, password))
    if response.status_code == 401:
        raise Exception("Incorrect password for workspace")
    if response.status_code != 200:
        raise Exception("Bad status code: {0}".format(response.status_code))
    return response.text

def delete_workspace(workspace, password):
    response = requests.get("http://{0}/Delete/{1}/{2}".format(address, workspace, password))
    if response.status_code == 401:
        raise Exception("Incorrect password for workspace")
    if response.status_code not in [200, 201]:
        raise Exception("Bad status code:{0}".format(response.status_code))

def compile_file(function, workspace, input_filename, output_filename, password):
    response = requests.get("http://{0}/{1}/{2}/{3}/{4}".format(address, function, workspace, password, input_filename))
    if response.status_code == 401:
        raise Exception("Incorrect password for workspace")
    if response.status_code in [200, 201]:
        file = open(output_filename, "wb")
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    else:
        raise Exception("Bad response code: {0}".format(response.status_code))

def list_dirs(dir, password):
    response = requests.get("http://{0}/ListFiles/{1}/{2}".format(address, dir, password))
    if response.status_code == 401:
        raise Exception("Incorrect password for workspace")
    if response.status_code in [200, 201]:
        return json.loads(response.text)
    else:
        raise Exception("Bad response code: {0}".format(response.status_code))

def create_subfolder(workspace, subfolder_name, password):
    response = requests.get("http://{0}/CreateSubFolder/{1}/{2}/{3}".format(address, workspace, password, subfolder_name))
    if response.status_code == 401:
        raise Exception("Incorrect password for workspace")
    if response.status_code in [200, 201]:
        return json.loads(response.text)
    else:
        raise Exception("Bad response code: {0}".format(response.status_code))

def random_string_var(min, max):
    return random_string(random.randint(min, max))

def random_string(length):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])

def random_string_exclude_var(min, max, excludelist):
    string = random_string_var(min, max)
    while string in excludelist:
        string = random_string_var(min, max)
    return string

def random_string_exclude(length, excludelist):
    string = random_string(length)
    while string in excludelist:
        string = random_string(length)
    return string