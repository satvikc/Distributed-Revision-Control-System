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
        """
        Initiates the repository
        """
        pass

    def add(self,filename):
        """
        Adds the given file or directory (all files and directories in
        it) to the tracking system. You need to commit before the
        files added are actually tracked.

        Args:
          filename(str) : file or directory name to add
        Raises:
          FileOrDirectoryDoesNotExist : When the file or directory
          does not exist.
        """
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
