import os
import hashlib
import hmac
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import getpass
import platform
import uuid

class SecureConfig:
    def __init__(self, config_file='.secure_config'):
        self.config_file = config_file
        self.key = self.derive_key()
        self.cipher_suite = Fernet(self.key)

    def derive_key(self):
        # Derive key from environment and machine ID
        machine_id = platform.node() + platform.platform()
        salt = hashlib.sha256(machine_id.encode()).digest()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        password = getpass.getpass('Enter password: ')
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def encrypt(self, data):
        return self.cipher_suite.encrypt(json.dumps(data).encode())

    def decrypt(self, encrypted_data):
        return json.loads(self.cipher_suite.decrypt(encrypted_data))

    def save_config(self, data):
        with open(self.config_file, 'wb') as f:
            f.write(self.encrypt(data))

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'rb') as f:
                return self.decrypt(f.read())
        else:
            return None

    def rotate_key(self):
        # Generate new key and re-encrypt config
        new_key = self.derive_key()
        new_cipher_suite = Fernet(new_key)
        config = self.load_config()
        if config:
            encrypted_config = new_cipher_suite.encrypt(json.dumps(config).encode())
            with open(self.config_file, 'wb') as f:
                f.write(encrypted_config)
        self.key = new_key
        self.cipher_suite = new_cipher_suite

# Example usage:
secure_config = SecureConfig()
config = {'api_key': 'secret_key'}
secure_config.save_config(config)
loaded_config = secure_config.load_config()
print(loaded_config)