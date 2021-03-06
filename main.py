from helper_functions import *

password = random_string(10)

def compile_md_files():
    print("Creating workspace")
    workspace = make_workspace(password)
    print("Uploading file")
    upload_file(workspace, "example.md", password)

    print("Compile HTML")
    compile_file("CompileMDtoHTML", workspace, "example.md", "example.html", password)
    print("Compile PDF")
    compile_file("CompileMDtoPDF", workspace, "example.md", "example.pdf", password)

    print("Delete workspace")
    delete_workspace(workspace, password)

def compile_latex_files():
    print("Create workspace")
    workspace = make_workspace(password)
    print("Upload files")
    for filename in ["report.bib", "report.tex", "FPGA insides 1.png"]:
        print("Uploading file:", filename)
        upload_file(workspace, filename, password)
    print("Compile LaTeX to PDF\n")
    compile_file("CompileLaTeXtoPDF", workspace, "report.tex", "report.pdf", password)

    print("Files in workspace:".center(50, '-'))
    print("{:<30}{:<20}".format("File name:", "File size (bytes)"))
    for file_size_and_name in list_dirs(workspace, password):
        print("{:<30}{:<20}".format(file_size_and_name["name"], file_size_and_name["size"]))
    print("-" * 50, "\n")

    response = requests.get("http://{0}/ListFiles/{1}/abcd".format(address, workspace))
    if response.status_code == 401:
        print("Authentication test succeeded")

    print("Delete workspace")
    delete_workspace(workspace, password)



if __name__ == "__main__":
    print("Markdown compilation:")
    compile_md_files()
    print("LaTeX compilation:")
    compile_latex_files()
    print("All done")