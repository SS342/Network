
def pcheck(password: str) -> str:
    if len(password) < 5: return False
    sumols = "qwertyuiopasdfghjklzxcvbnmQAZXSWEDCVFRTGBNHYUJMMJUIKOL1234567890"
    for i in password:
        if not(i in sumols):
            return False
    return True