from helper_functions import *
import unittest
import os

class Tests(unittest.TestCase):
    def test_upload(self):
        password = random_string(10)
        workspace = make_workspace(password)

        filename = "example.md"
        file = open(filename, 'rb')

        params = {"workspace": workspace, "filename": filename}
        jstring = json.dumps(params)
        files = {"json": jstring, filename: file}
        response = requests.post("http://{0}/upload".format(address), files=files)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "Missing information in JSON file")

        params = {"workspace": workspace, "filename": filename, "password": password}
        files = {}
        response = requests.post("http://{0}/upload".format(address), files=files)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "Missing JSON")

        params = {"workspace": workspace, "filename": filename, "password": password}
        jstring = json.dumps(params)
        files = {"json": jstring}
        response = requests.post("http://{0}/upload".format(address), files=files)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "Missing file")

        params = {"workspace": workspace, "filename": filename, "password": password}
        jstring = json.dumps(params)
        response = requests.post("http://{0}/upload".format(address))
        self.assertEqual(response.status_code, 400)

        params = {"workspace": "asdf", "filename": filename, "password": password}
        jstring = json.dumps(params)
        files = {"json": jstring, filename: file}
        response = requests.post("http://{0}/upload".format(address), files=files)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "workspace name not found")

        file.close()

    def test_compile_md_to_html(self):
        password = random_string(12)
        workspace = make_workspace(password)
        upload_file(workspace, "example.md", password)

        params = {"workspace": workspace, "password": password}
        response = requests.post("http://{0}/CompileMDtoHTML/".format(address), json=params)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "Missing parameter in JSON")

        response = requests.post("http://{0}/CompileMDtoHTML/".format(address))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "Missing JSON")

        params = {"workspace": workspace, "password": password, "filename": "asfdsdf.md"}
        response = requests.post("http://{0}/CompileMDtoHTML/".format(address), json=params)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "The file you are trying to compile does not exist")

        compile_file("CompileMDtoHTML", workspace, "example.md", "example.html", password)

        delete_workspace(workspace, password)
        os.remove("example.html")

    def test_compile_md_to_html(self):
        password = random_string(12)
        workspace = make_workspace(password)
        upload_file(workspace, "example.md", password)

        params = {"workspace": workspace, "password": password}
        response = requests.post("http://{0}/CompileMDtoPDF/".format(address), json=params)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "Missing parameter in JSON")

        response = requests.post("http://{0}/CompileMDtoHTML/".format(address))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "Missing JSON")

        params = {"workspace": workspace, "password": password, "filename": "asfdsdf.md"}
        response = requests.post("http://{0}/CompileMDtoPDF/".format(address), json=params)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "The file you are trying to compile does not exist")

        delete_workspace(workspace, password)

    def test_authentication(self):
        def authentication_test_helper(testclass, command):
            try:
                command()
            except Exception as exp:
                testclass.assertEqual("Incorrect password for workspace", str(exp))
            else:
                testclass.assertTrue(False)

        correct_password = random_string_var(5, 15)
        incorrect_password = random_string_exclude_var(5, 15, [correct_password])

        workspace = make_workspace(correct_password)

        authentication_test_helper(self, lambda: create_subfolder(workspace, random_string(10), incorrect_password))

        filename = random_string(10)
        src_filename = filename + ".md"
        os.system("touch {}".format(src_filename))

        authentication_test_helper(self, lambda: upload_file(workspace, src_filename, incorrect_password))
        upload_file(workspace, src_filename, correct_password)
        authentication_test_helper(self, lambda: compile_file("CompileMDtoHTML", workspace, src_filename,
                                                               filename + ".html", incorrect_password))
        authentication_test_helper(self, lambda: compile_file("CompileMDtoPDF", workspace,
                                                               src_filename, filename + ".pdf", incorrect_password))

        src_filename2 = filename + "tex"
        os.system("touch {}".format(src_filename2))

        upload_file(workspace, src_filename2, correct_password)
        authentication_test_helper(self, lambda: compile_file("CompileLaTeXtoPDF", workspace,
                                                               src_filename2, filename + ".pdf", incorrect_password))

        os.remove(src_filename)
        os.remove(src_filename2)

        authentication_test_helper(self, lambda: delete_workspace(workspace, incorrect_password))
        delete_workspace(workspace, correct_password)
