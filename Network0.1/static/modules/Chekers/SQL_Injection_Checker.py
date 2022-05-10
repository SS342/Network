def SQL_Injection_Checker(string : str) -> bool:
    string = string.lower()

    query = ["select", "insert", "update", "delete", "drop"]

    for operation in query:
        if operation in string:
            return False
    return True
    

        