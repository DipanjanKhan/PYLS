import unittest
import sys
from pyls.__main__ import main
from io import StringIO

class TestPyls(unittest.TestCase):
    def test_main_with_invalid_directory(self) -> None:
        """
        Test behavior when an invalid directory is provided
        """
        sys.argv = ['pyls', 'hello', '-l']
        main_output = StringIO()
        sys.stdout = main_output
        main()
        expected_output = "error: cannot access 'hello': No such file or directory"
        self.assertEqual(main_output.getvalue().strip(), expected_output)
    
    def test_main_with_valid_directory(self) -> None:
        """
        Test behavior when a valid directory is provided
        """
        sys.argv = ['pyls', 'parser', '-l']
        main_output = StringIO()
        sys.stdout = main_output
        main()
        expected_output = "drwxr-xr-x 1.3K Nov 17 12:51 parser_test.go\n-rw-r--r-- 1.6K Nov 17 12:05 parser.go\ndrwxr-xr-x  533 Nov 14 16:03 go.mod"
        self.assertEqual(main_output.getvalue().strip(), expected_output)

    def test_main_with_filter(self) -> None:
        """
        Test behavior when using the filter option
        """
        sys.argv = ['pyls', '-l', '--filter=dir']
        main_output = StringIO()
        sys.stdout = main_output
        main()
        expected_output = "-rw-r--r-- 4.0K Nov 14 15:58 ast\ndrwxr-xr-x 4.0K Nov 14 15:21 lexer\ndrwxr-xr-x 4.0K Nov 17 12:51 parser\n-rw-r--r-- 4.0K Nov 14 14:57 token"
        self.assertEqual(main_output.getvalue().strip(), expected_output)

    def test_main_with_invalid_filter(self) -> None:
        """
        Test behavior when an invalid filter option is provided
        """
        sys.argv = ['pyls', '-l', '--filter=folder']
        with self.assertRaises(SystemExit):
            main()

    def test_main_with_A_l_r_t(self) -> None:
        """
        Test behavior when A, l, r, t are provided
        """ 
        sys.argv = ['pyls', '-A', '-l', '-r', '-t']
        main_output = StringIO()
        sys.stdout = main_output
        main()
        expected_output = "drwxr-xr-x 4.0K Nov 17 12:51 parser\n-rw-r--r-- 4.0K Nov 14 15:58 ast\ndrwxr-xr-x 4.0K Nov 14 15:21 lexer\n-rw-r--r-- 4.0K Nov 14 14:57 token\n-rw-r--r--   74 Nov 14 13:57 main.go\ndrwxr-xr-x   60 Nov 14 13:51 go.mod\ndrwxr-xr-x   83 Nov 14 11:27 README.md\ndrwxr-xr-x 1.0K Nov 14 11:27 LICENSE\ndrwxr-xr-x 8.7K Nov 14 11:27 .gitignore"
        self.assertEqual(main_output.getvalue().strip(), expected_output)


if __name__ == '__main__':
    unittest.main()