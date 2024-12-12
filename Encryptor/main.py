from encryptor import Encryptor


ENCR: Encryptor = Encryptor()
ENCR_OPTS: tuple[str, ...] = 'encrypt_file', 'encrypt_folder', 'encrypt_folder_recursive', 'encrypt_user'
DECR_OPTS: tuple[str, ...] = 'decrypt_file', 'decrypt_folder', 'decrypt_folder_recursive', 'decrypt_user'
ENCR_CHOISE: str = ' | '.join([f'{i} {ENCR_OPTS[i]}' for i in range(len(ENCR_OPTS))])
DECR_CHOISE: str = ' | '.join([f'{i} {DECR_OPTS[i]}' for i in range(len(DECR_OPTS))])
NUMS: str = ''.join([str(i) for i in range(len(ENCR_OPTS))])


def call_encr(ind: str,
              path: str) -> None:
    if ind == '0':
        ENCR.encrypt_file(path)
    elif ind == '1':
        ENCR.encrypt_folder(path)
    else:
        ENCR.encrypt_folder_recursive(path)


def call_decr(ind: str,
              path: str) -> None:
    if ind == '0':
        ENCR.decrypt_file(path)
    elif ind == '1':
        ENCR.decrypt_folder(path)
    else:
        ENCR.decrypt_folder_recursive(path)


def get_option_ind(options: str) -> str:
    trying_ind: bool = True
    while trying_ind:
        print(f'Allowed options:\n{options}')
        ind: str = input('Enter the index of the function: ')
        if ind not in NUMS:
            print(f'{ind} is not allowed. Try again')
        else:
            trying_ind = False
    return ind


def get_source_path() -> str:
    path: str = input('Enter the source path: ')
    pth: str = path.replace('\\', '/').replace('\'', '').replace('\"', '').replace('\n', '')
    return pth


def encrypt_mode() -> None:
    ind = get_option_ind(ENCR_CHOISE)
    if ind == str(len(ENCR_OPTS) - 1):
        ENCR.encrypt_user()
        return
    path: str = get_source_path()
    call_encr(ind, path)


def decrypt_mode() -> None:
    ind = get_option_ind(DECR_CHOISE)
    if ind == str(len(DECR_OPTS) - 1):
        ENCR.decrypt_user()
        return
    path: str = get_source_path()
    call_decr(ind, path)


def set_key() -> None:
    keyfile: str = input('Enter the path to key file. If you want default, enter \'current\':\n')
    key_file: str = keyfile.replace('\"', '').replace('\'', '').replace(' ', '').replace('\n', '').replace('\t', '')
    key_new: str = input(f'Enter \'new\' to generate new key in {key_file} or print something else to use current: ')
    nw: str = key_new.replace('\"', '').replace('\'', '').replace(' ', '').replace('\n', '').replace('\t', '')
    if nw == 'new':
        [ENCR.gen_key() if (key_file == 'current') else ENCR.gen_key(key_file)]
    else:
        [ENCR.read_key() if (key_file == 'current') else ENCR.read_key(key_file)]


def set_mode() -> None:
    mode: str = input('Enter \'e\' if you want to encrypt, \'d\' if decrypt or something else to skip it: ')
    md: str = mode.replace('\"', '').replace('\'', '').replace(' ', '').replace('\n', '').replace('\t', '')
    if md == 'e':
        encrypt_mode()
    elif md == 'd':
        decrypt_mode()
    else:
        print('Nothing happened')


def main() -> None:
    print('Using the default path to the key file may cause it to be lost. Try to use your files to store your keys')
    running: bool = True
    while running:
        set_key()
        set_mode()
        on: str = input('Enter \'end\' to end the or program or something else to continue: ')
        if on == 'end':
            running = False


if __name__ == '__main__':
    main()
    