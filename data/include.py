import sys
import subprocess
from config.config import Config
from data.data import Data
import pandas as pd
import random, string


class Methods:
    @staticmethod
    def store_password():
        name = input("Enter Name / URL: ")
        username_provided = input("Login: ")
        password_provided = input("Password: ")
        print("Notes: ")
        notes = []
        while True:
            note_line = input("\t> ")
            if note_line:
                notes.append(note_line)
            else:
                break
        notes_text_provided = '\n'.join(notes)

        username = username_provided.encode()
        password = password_provided.encode()
        note = notes_text_provided.encode()

        config = Config()
        f = config.GetKey()

        username_stored = f.encrypt(username)
        password_stored = f.encrypt(password)
        notes_stored = f.encrypt(note)

        d = Data()
        data = d.Fetch()

        data[str(name)] = {"username": str(username_stored.decode()), "password": str(password_stored.decode()),
                           "notes": notes_stored.decode()}

        d.Update(data)
        print(f"{name} stored!")

    @staticmethod
    def list_names():
        config = Config()
        f = config.GetKey()

        d = Data()
        data = d.Fetch()

        name_list = []
        username_list = []
        password_list = []
        notes_list = []
        for obj in data:
            name_list.append(obj)

            username = f.decrypt(data[obj]['username'].encode())
            username_list.append(username.decode())

            password = f.decrypt(data[obj]['password'].encode())
            password_list.append(password.decode())

            note = f.decrypt(data[obj]['notes'].encode())
            notes_list.append(note.decode())
        df = pd.DataFrame(
            {'name / url': name_list, 'username': username_list, 'password': password_list, 'notes': notes_list})
        df = df[['name / url', 'username', 'password', 'notes']]
        df.head()
        pd.options.display.max_columns = None
        pd.options.display.width = None
        print(df)

    @staticmethod
    def search_password():
        user_input = input("Search: ")

        config = Config()
        f = config.GetKey()

        d = Data()
        data = d.Fetch()

        passwords_found = 0
        for name in data:
            find = name.lower().find(user_input.lower())
            if find >= 0:
                passwords_found += 1
                username_stored = data[name]['username'].encode()
                password_stored = data[name]['password'].encode()
                notes_stored = data[name]['notes'].encode()

                username = f.decrypt(username_stored)
                password = f.decrypt(password_stored)
                notes = f.decrypt(notes_stored)

                print(f"*** {name} ***")
                print(f"UID - {username.decode()}")
                print(f"PWD - {password.decode()}")
                print("--------------------------")
                print("Notes:")
                print(f"{notes.decode()}")
                print("--------------------------")
                print("")
        if passwords_found == 0:
            print(f"'{user_input}' not found!")

    @staticmethod
    def update_password():
        password_name = input("Which password should be changed?: ")

        config = Config()
        f = config.GetKey()

        d = Data()
        data = d.Fetch()

        for name in data:
            if password_name.lower() == name.lower():
                password_stored = data[name]['password'].encode()
                notes_stored = data[name]['notes'].encode()
                current_password = f.decrypt(password_stored)
                print(f"Current Password: {current_password.decode()}")
                password_input = input("New Password: ")
                username_stored = data[name]['username'].encode()

                password = password_input.encode()
                password_stored = f.encrypt(password)
                data[str(name)] = {"username": str(username_stored.decode()), "password": str(password_stored.decode()),
                                   "notes": notes_stored.decode()}

        d.Update(data)

        print(f"{password_name} updated!")

    @staticmethod
    def remove_password():
        user_input = input("Which name should I remove?: ")
        d = Data()
        data = d.Fetch()

        password_found = False
        for key, value in list(data.items()):
            if user_input.lower() == key.lower():
                password_found = True

        if password_found:
            confirm = False
            while confirm is False:
                confirm_input = input(f"Are you sure you want to delete {user_input}? (y/n): ")
                if confirm_input.lower() == 'y':
                    confirm = True
                    for key, value in list(data.items()):
                        if user_input.lower() == key.lower():
                            del data[key]

                    d.Update(data)

                    print(f"{user_input} deleted!")
                else:
                    pass
        else:
            print(f"{user_input} is not found!")

    @staticmethod
    def password_generator():
        password_length = input("Password Length: ")
        chars = string.ascii_letters + string.digits + '!@#$%^&*()'

        rnd = random.SystemRandom()
        new_password = ''.join(rnd.choice(chars) for i in range(int(password_length)))
        print(new_password)

        store_input = input("Should I store this password? (y/n): ")

        if store_input.lower() == 'y':
            name = input("Enter Name/Site: ")
            username_provided = input("Enter Username: ")
            print("Notes: ")
            notes = []
            while True:
                note_line = input("\t> ")
                if note_line:
                    notes.append(note_line)
                else:
                    break
            notes_text_provided = '\n'.join(notes)

            username = username_provided.encode()
            password = new_password.encode()
            note = notes_text_provided.encode()

            config = Config()
            f = config.GetKey()

            username_stored = f.encrypt(username)
            password_stored = f.encrypt(password)
            notes_stored = f.encrypt(note)

            d = Data()
            data = d.Fetch()

            data[str(name)] = {"username": str(username_stored.decode()), "password": str(password_stored.decode()),
                               "notes": notes_stored.decode()}

            d.Update(data)

            print(f"{name} stored!")
            subprocess.Popen(['clip'], stdin=subprocess.PIPE).communicate(password)
            print(f"{name} password copied to clipboard")

    @staticmethod
    def get_password():
        user_input = input("Name / URL: ")

        config = Config()
        f = config.GetKey()

        d = Data()
        data = d.Fetch()

        passwords_found = 0
        for name in data:
            if name.lower() == user_input.lower():
                passwords_found += 1
                username_stored = data[name]['username'].encode()
                password_stored = data[name]['password'].encode()
                notes_stored = data[name]['notes'].encode()

                username = f.decrypt(username_stored)
                password = f.decrypt(password_stored)
                notes = f.decrypt(notes_stored)

                print(f"*** {name} ***")
                print(f"UID - {username.decode()}")
                print(f"PWD - {password.decode()}")
                print("")
                print("Notes:")
                print(f"{notes.decode()}")
                print("")

                subprocess.Popen(['clip'], stdin=subprocess.PIPE).communicate(password)
                print(f"{name} password copied to clipboard")
        if passwords_found == 0:
            print(f"{user_input} not found!")
