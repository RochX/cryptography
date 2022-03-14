import os
import pickle
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
        self._rsa_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self._rsa_public_key = self._rsa_private_key.public_key()

        # initial aes keys, these will throw errors if not overwritten
        self._aes_key = b'key_initial'
        self.iv = b'iv_initial'

    # returns public RSA key
    def publicKeyRSA(self):
        return self._rsa_public_key

    def generate_encrypted_aes_key(self, other_rsa_public_key):
        # generate a new AES key
        self._aes_key = os.urandom(32)
        #self.aes_key = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # encrypt the AES key with RSA (using the other's public key)
        encrypted_key = other_rsa_public_key.encrypt(
            self._aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # sign the encrypted AES key
        signature = self._rsa_private_key.sign(
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
        plaintext = self._rsa_private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # set AES key
        self._aes_key = plaintext


'''
establishes a shares AES key with p1 and p2 with RSA.

p1 chooses a random key
p1 encrypts it with p2's public RSA key
p1 signs it with their private RSA key

p1 sends signature and ciphertext to p2

p2 decrypts with their private key
p2 verifies signature with p1's public key

p1 and p2 now have shared keys

we will also establish the shared IV in this step
'''
def aes_key_exchange_with_rsa(p1: CryptographyProperties, p2: CryptographyProperties):
    encrypted_key = p1.generate_encrypted_aes_key(p2.publicKeyRSA())
    p2.decrypt_and_set_aes_key(encrypted_key, p1.publicKeyRSA())

    shared_iv = os.urandom(16)
    p1.iv = shared_iv
    p2.iv = shared_iv


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


def pickle_write_secure(var, filename, aes_key, iv):
    aes = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = aes.encryptor()

    pickle_bytes = pickle.dumps(var)

    # pad the message for AES
    pickle_bytes += PADDING_BYTE * (-len(pickle_bytes) % 16)

    # encrypt our bytes
    encrypted_bytes = encryptor.update(pickle_bytes)

    # write to file
    with open(filename, 'wb') as file:
        file.write(encrypted_bytes)


def pickle_read_secure(filename, aes_key, iv):
    aes = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = aes.decryptor()

    # read encrypted bytes
    with open(filename, 'rb') as file:
        encrypted_bytes = file.read()

    # decrypt bytes
    pickle_bytes = decryptor.update(encrypted_bytes)

    # remove padding bytes from AES
    pickle_bytes.rstrip(PADDING_BYTE)

    # read variable and return
    var = pickle.loads(pickle_bytes)
    return var

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
    print("p1 aes key: ", p1._aes_key)
    print("p2 aes key: ", p2._aes_key)
    print()

    aes_key_exchange_with_rsa(p1, p2)

    print("Post Transfer")
    print("p1 aes key: ", p1._aes_key)
    print("p2 aes key: ", p2._aes_key)

    print()

    message = b'Shared IV through classes!'

    print('iv:', iv)
    ciphertext = encrypt_and_sign(message, p1._rsa_private_key, p1._aes_key, p1.iv)
    print('ciphertext:', ciphertext)

    print()

    print('message:', decrypt_and_verify(ciphertext, p1.publicKeyRSA(), p2._aes_key, p2.iv))

    dict = {'aaaaaaaaaaa': 1, 'bbbbbbbbbb': 2, 'ccccccccc': 3}
    aes_key = os.urandom(32)
    iv = os.urandom(16)

    with open('variable_files/testU.pickle', 'wb') as file:
        pickle.dump(dict, file)

    pickle_write_secure(dict, 'variable_files/test.pickle', aes_key, iv)

    print(pickle_read_secure('variable_files/test.pickle', aes_key, iv))


