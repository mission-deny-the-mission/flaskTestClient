import requests

addressfile = open("server.url", 'r')
address = addressfile.read().strip()
addressfile.close()

response = requests.get("http://{0}/register".format(address))
dir = response.text
sample_file = open("example.md", "rb")
response = requests.post("http://{0}/upload/{1}/example.md".format(address, dir), data=sample_file)
if response.status_code == 201:
    response = requests.get("http://{0}/compile/{1}/example.md".format(address, dir))
    file = open("example.html", "w")
    file.write(response.text)
    file.close()

    response = requests.get("http://{0}/compilepdf/{1}/example.md".format(address, dir))
    file = open("example.pdf", "wb")
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
    file.close()
