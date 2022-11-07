def reading_smg(file_paths):
    '''
    Using this function to read all sgm files.
    :param file_paths: list of file paths from Reuters files
    :yield:
    file_num (string): from 0 -21 number of files
    '''
    for file_path in file_paths:
        if not file_path.endswith(".sgm"):
            continue

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            file_content = f.read()
            file_name = file_path.split('.')[0]
            file_num = file_name[-2:]
            yield file_num, file_content