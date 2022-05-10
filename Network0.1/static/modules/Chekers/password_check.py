import re

def pcheck(a: str) -> str:
    res = [re.search(r"[a-z]", a), re.search(r"[A-Z]", a), re.search(r"[0-9]", a)]
    if all(res):
        return "Password is okay"
    return ("Пароль не надёжен. Добавте "+
            "Строчные буквы, "*(res[0] is None) +
            "Заглавные буквы, "*(res[1] is None) +
            "Цифры, "*(res[2] is None) +
            "И попробуйте снова!")