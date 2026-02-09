import os

class FileSystem:
    def __init__(self, root_directory):
        self.root_directory = root_directory

    def create_file(self, file_path):
        with open(os.path.join(self.root_directory, file_path), 'w') as f:
            pass

    def read_file(self, file_path):
        with open(os.path.join(self.root_directory, file_path), 'r') as f:
            return f.read()

    def write_file(self, file_path, contents):
        with open(os.path.join(self.root_directory, file_path), 'w') as f:
            f.write(contents)