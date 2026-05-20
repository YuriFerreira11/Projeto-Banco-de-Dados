from cryptography.fernet import Fernet
from Config.paths import CONFIG_PATH
import yaml


with open(CONFIG_PATH, "r") as ymlfile:
    config = yaml.safe_load(ymlfile)

key = config["chave_Fernet"]["SECRET_KEY"].encode()

fernet = Fernet(key)
def encrypt_cpf(cpf: str) -> str:
    encrypted = fernet.encrypt(cpf.encode())
    return encrypted.decode()
def decrypt_cpf(encrypted_cpf: str) -> str:
    decrypted = fernet.decrypt(encrypted_cpf.encode())
    return decrypted.decode()
