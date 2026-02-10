import os
import hashlib
import json

class IntegrityChecker:
    def __init__(self, checksums_file='security_checksums.json'):
        self.checksums_file = checksums_file
        self.checksums = self.load_checksums()

    def load_checksums(self):
        if os.path.exists(self.checksums_file):
            with open(self.checksums_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_checksums(self):
        with open(self.checksums_file, 'w') as f:
            json.dump(self.checksums, f)

    def calculate_checksum(self, file_path):
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def verify_checksum(self, file_path):
        if file_path not in self.checksums:
            return False
        return self.calculate_checksum(file_path) == self.checksums[file_path]

    def update_checksum(self, file_path):
        self.checksums[file_path] = self.calculate_checksum(file_path)
        self.save_checksums()

    def check_integrity(self):
        for file_path in self.checksums:
            if not self.verify_checksum(file_path):
                raise ValueError(f'Integrity check failed for {file_path}')

# Example usage:
integrity_checker = IntegrityChecker()
integrity_checker.check_integrity()