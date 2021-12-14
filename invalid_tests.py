from helper_functions import *
import unittest
import os

def authentication_test_helper(testclass, command):
    try:
        command()
    except Exception as exp:
        testclass.assertEqual("Incorrect password for workspace", str(exp))
    else:
        testclass.assertTrue(False)

class Tests(unittest.TestCase):
    def test_authentication(self):
        correct_password = random_string_var(5, 15)
        incorrect_password = random_string_exclude_var(5, 15, [correct_password])

        workspace = make_workspace(correct_password)

        authentication_test_helper(self, lambda : create_subfolder(workspace, random_string(10), incorrect_password))

        filename = random_string(10)
        src_filename = filename + ".md"
        os.system("touch {}".format(src_filename))

        authentication_test_helper(self, lambda : upload_file(workspace, src_filename, incorrect_password))
        upload_file(workspace, src_filename, correct_password)
        authentication_test_helper(self, lambda : compile_file("CompileMDtoHTML", workspace, src_filename,
                                                               filename + ".html", incorrect_password))
        authentication_test_helper(self, lambda : compile_file("CompileMDtoPDF", workspace,
                                                               src_filename, filename + ".pdf", incorrect_password))

        src_filename2 = filename + "tex"
        os.system("touch {}".format(src_filename2))

        upload_file(workspace, src_filename2, correct_password)
        authentication_test_helper(self, lambda : compile_file("CompileLaTeXtoPDF", workspace,
                                                               src_filename2, filename + ".pdf", incorrect_password))

        os.remove(src_filename)
        os.remove(src_filename2)

        authentication_test_helper(self, lambda : delete_workspace(workspace, incorrect_password))
        delete_workspace(workspace, correct_password)
