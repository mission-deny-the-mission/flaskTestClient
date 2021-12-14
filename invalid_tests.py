from helper_functions import *
import unittest
import os

class Tests(unittest.TestCase):
    def test_authentication(self):
        correct_password = random_string_var(5, 15)
        incorrect_password = random_string_exclude_var(5, 15, [correct_password])
        workspace = make_workspace(correct_password)
        filename = random_string(10)
        src_filename = filename + ".md"
        os.system("touch {}".format(src_filename))
        try:
            upload_file(workspace, src_filename, incorrect_password)
        except Exception as exp:
            self.assertEqual("Incorrect password for workspace", str(exp))
        else:
            self.assertTrue(False)
        upload_file(workspace, src_filename, correct_password)
        try:
            compile_file("CompileMDtoHTML", workspace, src_filename, filename + ".html", incorrect_password)
        except Exception as exp:
            self.assertEqual("Incorrect password for workspace", str(exp))
        else:
            self.assertTrue(False)
        try:
            compile_file("CompileMDtoPDF", workspace, src_filename, filename + ".pdf", incorrect_password)
        except Exception as exp:
            self.assertEqual("Incorrect password for workspace", str(exp))
        else:
            self.assertTrue(False)
        os.remove(src_filename)
        delete_workspace(workspace, correct_password)
