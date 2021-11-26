import requests

addressfile = open("server.url", 'r')
address = addressfile.read().strip()
addressfile.close()

def upload_file(dir, filename):
    file = open(filename, 'rb')
    response = requests.post("http://{0}/upload/{1}/{2}".format(address, dir, filename), data=file)
    if response.status_code not in [201, 200]:
        raise Exception("bad status code: {0}".format(response.status_code))

def make_workspace():
    response = requests.get("http://{0}/register".format(address))
    if response.status_code != 200:
        raise Exception("Bad status code: {0}".format(response.status_code))
    return response.text

def delete_workspace(workspace):
    response = requests.get("http://{0}/Delete/{1}".format(address, workspace))
    if response.status_code not in [200, 201]:
        raise Exception("Bad status code:{0}".format(response.status_code))

def compile_file(function, workspace, input_filename, output_filename):
    response = requests.get("http://{0}/{1}/{2}/{3}".format(address, function, workspace, input_filename))
    if response.status_code in [200, 201]:
        file = open(output_filename, "wb")
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    else:
        raise Exception("Bad response code: {0}".format(response.status_code))

def compile_md_files():
    workspace = make_workspace()
    upload_file(workspace, "example.md")

    compile_file("CompileMDtoHTML", workspace, "example.md", "example.html")
    compile_file("CompileMDtoPDF", workspace, "example.md", "example.pdf")

    delete_workspace(workspace)

def compile_latex_files():
    workspace = make_workspace()
    for filename in ["report.bib", "report.tex", "FPGA insides 1.png"]:
        upload_file(workspace, filename)
    compile_file("CompileLaTeXtoPDF", workspace, "report.tex", "report.pdf")
    delete_workspace(workspace)

if __name__ == "__main__":
    compile_md_files()
    compile_latex_files()