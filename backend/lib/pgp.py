from gnupg import GPG

_gpg_client = GPG()

async def symmetric_encrypt(data, key)->str:
    """
    Encrypts data using a symmetric key.
    """
    encrypted =  _gpg_client.encrypt(data, recipients="None", symmetric=True, passphrase=key)
    return str(encrypted)

async def symmetric_decrypt(data, key)->str:
    """
    Decrypts data using a symmetric key.
    """
    decrypted = _gpg_client.decrypt(message=data, passphrase=key)
    return str(decrypted)