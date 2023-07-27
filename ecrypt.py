import os
import tempfile
import cryptography.hazmat.primitives.hashes as hashes
import cryptography.hazmat.primitives.asymmetric.ec as ec
import cryptography.hazmat.primitives.serialization as serialization


class Ecrypt:

    def __init__(self, isServer=False, private_key=None, private_pass=None, public_key=None):
        if isServer:
            if private_key != None:
                self.private_key = Ecrypt.load_private_key_pem(
                    private_key, private_pass)
                self.public_key = self.private_key.public_key()
            else:
                self.private_key, self.public_key = Ecrypt.generate_key_pair(
                    self)
        else:
            self.public_key = public_key

    def set_public_key(self, pkey):
        self.public_key = pkey

    def get_public_key(self):
        return self.public_key

    def generate_key_pair(self):
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()
        return private_key, public_key

    def encrypt_content(self, content):
        encrypted_content = self.public_key.encrypt(
            content,
            ec.ECIES(hashes.SHA256())
        )
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(encrypted_content)
            return temp_file

    def encrypt_file(self, file):
        with open(file, 'rb') as file:
            plaintext_content = file.read()
            return self.encrypt_content(plaintext_content)

    def decrypt_file(self, file):
        plaintext_content = file.read()
        return self.decrypt_context(plaintext_content)

    def decrypt_context(self, ciphertext):
        plaintext = self.private_key.decrypt(
            ciphertext,
            ec.ECIES(hashes.SHA256())
        )
        return plaintext

    def get_public_key_pem(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def generate_key_pair(self):
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def load_private_key_pem(filename, password=None):
        with open(filename, 'rb') as file:
            pem_data = file.read()
            private_key = serialization.load_pem_private_key(
                pem_data,
                password=password
            )
            return private_key
