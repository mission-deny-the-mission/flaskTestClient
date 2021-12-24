import requests
import json
import random
import string

addressfile = open("server.url", 'r')
address = addressfile.read().strip()
addressfile.close()

def test_response(response):
    if response.status_code == 401:
        raise Exception("Incorrect password for workspace")
    if response.status_code not in [201, 200]:
        raise Exception("bad status code: {0}\nMessage: {1}".format(response.status_code, response.text))

def upload_file(workspace, filename, password):
    file = open(filename, 'rb')
    params = {"workspace": workspace, "filename": filename, "password": password}
    jstring = json.dumps(params)
    files = {"json": jstring, filename: file}
    response = requests.post("http://{0}/upload".format(address), files=files)
    file.close()
    test_response(response)

def make_workspace(password):
    response = requests.post(url="http://{0}/register/".format(address), json={"password": password})
    test_response(response)
    return response.text

def delete_workspace(workspace, password):
    response = requests.get("http://{0}/Delete/".format(address), json={"workspace": workspace, "password": password})
    test_response(response)

def compile_file(function, workspace, input_filename, output_filename, password):
    data = {"workspace": workspace, "filename": input_filename, "password": password}
    response = requests.post("http://{0}/{1}/".format(address, function), json=data)
    if response.status_code == 401:
        raise Exception("Incorrect password for workspace")
    if response.status_code in [200, 201]:
        file = open(output_filename, "wb")
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
        file.close()
    else:
        raise Exception("Bad response code: {0}".format(response.status_code))

def list_dirs(dir, password):
    response = requests.get("http://{0}/ListFiles/".format(address), json={"workspace": dir, "password": password})
    if response.status_code == 401:
        raise Exception("Incorrect password for workspace")
    if response.status_code in [200, 201]:
        return json.loads(response.text)
    else:
        raise Exception("Bad response code: {0}".format(response.status_code))

def create_subfolder(workspace, subfolder_name, password):
    data = {"workspace": workspace, "subfolder": subfolder_name, "password": password}
    response = requests.get("http://{0}/CreateSubFolder/".format(address), json=data)
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