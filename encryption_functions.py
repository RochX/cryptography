import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

PADDING_BYTE = b'#'
SEP_BYTES = b';;;'


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