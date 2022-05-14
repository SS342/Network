import os

def check_file(filename: str) -> bool:
    "Функция для проверки файлов"
    ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']
    for extension in ALLOWED_EXTENSIONS:
        if filename.lower().endswith(extension):
            path = os.getcwd() + "/static/img/userAvatars/"
            num_files = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])
            return f"{num_files+1}{extension}"
    return False