from re import S
import sqlite3
import os
import random


class Database(object):


    def __init__(self, path : str ="database.db"):
        "Инициализация базы данных"

        self.__connection__ = sqlite3.connect(path)
        self.__cursor__ =self.__connection__.cursor()

    def CreateTableAllUsers(self):
        "Создание таблицы в которой хранятся все юзеры"

        sql = """CREATE TABLE IF NOT EXISTS all_users (
            name VARCHAR(255) NOT NULL UNIQUE,
            contact VARCHAR(255) NOT NULL UNIQUE,
            password_hash STRING NOT NULL,
            avatar VARCHAR(255) NOT NULL,
            info STRING,
            posts INT,
            likes INT,
            comments INT,
            followers INT,
            theme STRING
        );"""
        self.__cursor__.execute(sql)
        self.__connection__.commit()


    def new(self, name : str, contact : str, hashed_password : bytes):
        "Регестрируем нового пользователя"

        path = os.getcwd() + "/static/img/avatars/"
        num_files = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])
        rnd_avatar = random.randint(1, num_files) # Выдаем пользователю рандомный аватар
        sql = f"INSERT INTO all_users values('{name}', '{contact}', '{hashed_password.decode('utf-8')}', '../static/img/avatars/{rnd_avatar}.jpg', 'Привет я пользуюсь сайтом Allelleo!', 0, 0, 0, 0, 'white')"
        self.__cursor__.execute(sql)
        self.__connection__.commit()


    def get_user(self, bcrypt, username : str, password : str):
        "Проверяем пользоватя при входе"

        sql = f"SELECT password_hash FROM all_users WHERE name='{username}'"
        data = self.__cursor__.execute(sql).fetchone()
        if data:
            pw_hash = data[0]
            if bcrypt.check_password_hash(pw_hash, password):
                sql = f"SELECT rowid FROM all_users WHERE name='{username}'"
                data = self.__cursor__.execute(sql).fetchone()
                
                return True


    def get_user_info(self, name : str, close : bool = False):
        "Информация о пользвателе"

        sql = f"SELECT * FROM all_users WHERE name='{name}'"
        data = self.__cursor__.execute(sql).fetchone()
        if close: self.close()
        return data


    def updateMainUserInfo(self, name, description, path=False, close=False):
        
        if path:
            sql = f"UPDATE all_users SET avatar='{path}', info='{description}' WHERE name='{name}'"
        else:
            sql = f"UPDATE all_users SET info='{description}' WHERE name='{name}'"

        self.__cursor__.execute(sql)
        self.__connection__.commit()
        if close: self.close()


    def changeTheme(self, username, close=False):
        sql = f"SELECT theme FROM all_users WHERE name='{username}'"
        data = self.__cursor__.execute(sql).fetchone()[0]
        if data == "white":
            sql = f"UPDATE all_users SET theme='dark' WHERE name='{username}'"
        else:
            sql = f"UPDATE all_users SET theme='white' WHERE name='{username}'"

        self.__cursor__.execute(sql)
        self.__connection__.commit()

    def close(self):
        "Закрытие подключения"

        self.__connection__.close()