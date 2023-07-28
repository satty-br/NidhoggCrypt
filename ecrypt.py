import base64
import tempfile
from typing import AnyStr
import cryptography.hazmat.primitives.hashes as hashes
import cryptography.hazmat.primitives.serialization as serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa,padding

class Ecrypt:

    def __init__(self, isServer=False, private_key=None, private_pass=None, public_key=None):
        if isServer:
            if private_key:
                self.load_private_key_pem(
                    private_key, private_pass)
                self.public_key = self.private_key.public_key()
            else:
                self.generate_keys()
        else:
            self.load_public_key_from_string(public_key)

    def set_public_key(self, pkey):
        self.public_key = pkey

    def load_public_key_from_string(self, public_key_string):
        public_key_data = public_key_string.encode('utf-8')
        self.public_key =  serialization.load_pem_public_key(public_key_data, backend=default_backend())


    def public_key_to_string(self):
        if self.public_key is None:
            raise ValueError("Public key has not been generated.")
        
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode('utf-8')

    def get_public_key(self):
        return self.public_key

    def generate_keys(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()


    def want_bytes(self, s: AnyStr) -> bytes:
        """Convert string to bytes."""
        if isinstance(s, str):
            return s.encode()
        return s
    

    def encrypt(self, plaintext):
        if self.public_key is None:
            raise ValueError("Public key has not been generated or loaded.")

        block_size = 128
        encrypted_blocks = []

        for i in range(0, len(plaintext), block_size):
            block = plaintext[i : i + block_size]
            encrypted_block = self.public_key.encrypt(
                block.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            encrypted_blocks.append(encrypted_block)

        encrypted_text = b"".join(encrypted_blocks)
        return base64.b64encode(encrypted_text).decode()

    def decrypt(self, ciphertext):
        if self.private_key is None:
            raise ValueError("Private key has not been generated.")

        ciphertext = base64.b64decode(ciphertext)
        block_size = 256
        decrypted_blocks = []

        for i in range(0, len(ciphertext), block_size):
            encrypted_block = ciphertext[i : i + block_size]
            decrypted_block = self.private_key.decrypt(
                encrypted_block,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            decrypted_blocks.append(decrypted_block)

        return b"".join(decrypted_blocks).decode()

    def encrypt_file(self, file):
        with open(file, 'rb') as file:
            plaintext_content = file.read()
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(self.encrypt(plaintext_content))
                return temp_file

    def decrypt_file(self, file):
        plaintext_content = file.read()
        return self.decrypt(plaintext_content)



    def get_public_key_pem(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def load_private_key_pem(self, filename, password=None):
        with open(filename, 'rb') as file:
            pem_data = file.read()
            private_key = serialization.load_pem_private_key(
                pem_data,
                password=password
            )
            self.private_key = private_key
