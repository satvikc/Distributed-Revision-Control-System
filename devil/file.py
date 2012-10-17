class FileController(object):
    """
    Class to perform all the local functionalities of the version
    control system.
    """
    def __init__(self,directory):
        """
        Args:
          directory(str): Full path of the directory where the
          version control is initiated.
        Returns:
          FileController Object
        """
        self.directory = directory

    def start(self):
        pass

    def add(self):
        pass

    def clone(self):
        pass

    def log(self):
        pass

    def diff(self):
        pass

    def status(self):
        pass

    def pull(self,url):
        pass

    def push(self,url):
        pass

    def revert(self,commit_hash):
        pass
