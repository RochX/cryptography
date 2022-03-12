import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

PADDING_BYTE = b'#'
SEP_BYTES = b';;;'


class CryptographyProperties:
    def __init__(self):
        # Generate RSA keys
        self.rsa_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.rsa_public_key = self.rsa_private_key.public_key()

        self.aes_key = b'initial'

    # returns public RSA key
    def publicKeyRSA(self):
        return self.rsa_public_key

    def generate_encrypted_aes_key(self, other_rsa_public_key):
        # generate a new AES key
        self.aes_key = os.urandom(32)
        #self.aes_key = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # encrypt the AES key with RSA (using the other's public key)
        encrypted_key = other_rsa_public_key.encrypt(
            self.aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # sign the encrypted AES key
        signature = self.rsa_private_key.sign(
            encrypted_key,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        signature_and_encrypted_key = signature + SEP_BYTES + encrypted_key

        return signature_and_encrypted_key

    # takes in a signature and encrypted key, verifies signature, decrypts it, and sets its AES key as the contents of the message
    def decrypt_and_set_aes_key(self, signature_and_encrypted_key, other_rsa_public_key):
        signature, ciphertext = signature_and_encrypted_key.split(sep=SEP_BYTES)

        # verify signature
        other_rsa_public_key.verify(
            signature,
            ciphertext,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # decrypt received ciphertext
        plaintext = self.rsa_private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # set AES key
        self.aes_key = plaintext


'''
establishes a shares AES key with p1 and p2 with RSA.

p1 chooses a random key
p1 encrypts it with p2's public RSA key
p1 signs it with their private RSA key

p1 sends signature and ciphertext to p2

p2 decrypts with their private key
p2 verifies signature with p1's public key

p1 and p2 now have shared keys
'''
def aes_key_exchange_with_rsa(p1: CryptographyProperties, p2: CryptographyProperties):
    encrypted_key = p1.generate_encrypted_aes_key(p2.publicKeyRSA())
    p2.decrypt_and_set_aes_key(encrypted_key, p1.publicKeyRSA())


# takes in a message a byte string and signs it, then encrypts it with AES
def encrypt_and_sign(message, rsa_private_key, aes_key, iv):
    # obtain RSA signature
    signature = rsa_private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # use a triple semicolon as separator between message and signature
    signedMessage = signature + SEP_BYTES + message

    # pad the message for AES
    signedMessage += PADDING_BYTE * (-len(signedMessage) % 16)

    # encrypt with AES in CBC block mode with our IV
    aes = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = aes.encryptor()
    ciphertext = encryptor.update(signedMessage)

    return ciphertext


def decrypt_and_verify(ciphertext, rsa_public_key, aes_key, iv):
    aes = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = aes.decryptor()

    # get our signature and message from the ciphertext
    signature, message = decryptor.update(ciphertext).split(SEP_BYTES)

    # remove the padding bytes from our message
    message = message.rstrip(PADDING_BYTE)

    # throws an InvalidSignature exception if verification fails
    rsa_public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # return our message
    return message


# testing function
if __name__ == '__main__':
    rsa_priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    rsa_pub = rsa_priv.public_key()
    message = b'I want to encrypt this!'

    aes_key = os.urandom(32)
    iv = os.urandom(16)

    print('aes_key:', aes_key)
    print('iv:', iv)
    ciphertext = encrypt_and_sign(message, rsa_priv, aes_key, iv)
    print('ciphertext:', ciphertext)

    print()

    print('message:', decrypt_and_verify(ciphertext, rsa_pub, aes_key, iv))

    p1 = CryptographyProperties()
    p2 = CryptographyProperties()

    print("Initial")
    print("p1 aes key: ", p1.aes_key)
    print("p2 aes key: ", p2.aes_key)
    print()

    aes_key_exchange_with_rsa(p1, p2)

    print("Post Transfer")
    print("p1 aes key: ", p1.aes_key)
    print("p2 aes key: ", p2.aes_key)


