import os
import sys
import time


class OldFileFromContext(Exception):
    pass


class ExecutionContext(object):
    """ExecutionContext - Change os.getcwd() and sys.argv temporarily
    """

    def __init__(self, args=None, cd=None):
        """
        Args:
            args (list): replacement for sys.argv
            cd (str): temporary working dir
        """
        self.args = args
        self.cd = cd
        self.born = time.time()

    def __enter__(self):
        self.owd = os.getcwd()
        self.argv = sys.argv
        if self.cd:
            os.chdir(self.cd)
        if self.args is not None:
            sys.argv = self.args
        return self

    def __exit__(self, type, value, traceback):
        os.chdir(self.owd)
        sys.argv = self.argv

    def check_new(self, filepath):
        """check_new - check that the given path was modified *after*
        this context was created.

        Args:
            filepath (str): path to check
        Raises:
            OldFileFromContext: if file is older than context
        """
        if os.stat(filepath).st_mtime < self.born:
            raise OldFileFromContext("File '%s' older than context" % filepath)
        return True
