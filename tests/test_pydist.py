import unittest
from unittest import mock
from subprocess import PIPE

from dhpython import pydist

class Test_guess_dependency(unittest.TestCase):

    def setUp(self):
        self.popen_patcher = mock.patch('dhpython.pydist.Popen')
        self.popen = self.popen_patcher.start()
        self.set_dpkg_retval()

    def tearDown(self):
        self.popen_patcher.stop()

    def set_dpkg_retval(self, stdout=b'', stderr=b'', returncode=None):
        self.popen().communicate.return_value = (stdout, stderr)
        if returncode is None:
            if stdout:
                returncode = 0
            else:
                returncode = 1
        self.popen().returncode = returncode
        self.popen.reset_mock()

    def test_dpkg(self):
        self.set_dpkg_retval(b"python3-barfoo: /usr/lib/python3/dist-packages/foobar-2.3.0.egg-info")
        dep = pydist.guess_dependency('cpython3', 'foobar')
        self.assertEqual(dep, 'python3-barfoo')
        self.popen.assert_called_once_with(
                "/usr/bin/dpkg -S *python3/*/[Ff][Oo][Oo][Bb][Aa][Rr]-?*\\.egg-info",
                shell=True,
                stdout=PIPE,
                stderr=PIPE)
