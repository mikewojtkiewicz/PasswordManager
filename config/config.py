import os
import json
from getpass import getpass
from cryptography.fernet import Fernet


class Config:
    def GetKey(self):
        file_root = os.listdir('.')
        if 'config.json' not in file_root:
            file_obj = open('config.json', "a+")
            config_file = file_obj.read(1)
            print(config_file)
            if config_file == '':
                file_obj.write("{}")
            file_obj.close()

        with open("config.json", "r") as f:
            config = json.load(f)

        if 'Fernet' not in config:
            key = self.generate_key()
        else:
            key = config['Fernet']['key']
        f = Fernet(key)

        return f
    
    @staticmethod
    def generate_key():
        key = Fernet.generate_key()
        with open("config.json", "r") as f:
            data = json.load(f)

        data["Fernet"] = {"key": key.decode()}

        with open("config.json", "w") as f:
            json.dump(data, f, indent=4)

        print("Key Generated!")
        return key

    def master_password(self):
        with open("config.json", "r") as f:
            data = json.load(f)

        key = data['Fernet']['key']
        f = Fernet(key)

        if 'master' not in data:
            new_master_pass = getpass(prompt="Enter a New Master Password: ")
            verify_master_pass = getpass(prompt="Verify New Master Password: ")

            if new_master_pass == verify_master_pass:
                master_key = f.encrypt(verify_master_pass.encode())
                data['master'] = {"password": str(master_key.decode())}

            with open("config.json", "w") as f:
                json.dump(data, f, indent=4)
            self.create_data_file()
            return True
        else:
            master_key = data['master']['password'].encode()
            master_pass = f.decrypt(master_key)
            times_tried = 0
            while times_tried <= 5:
                master = getpass(prompt="Enter Master Password: ")
                if not master == str(master_pass.decode()):
                    print("That is not the correct password")
                    times_tried += 1
                else:
                    return True

    @staticmethod
    def create_data_file():
        file_root = os.listdir('.')
        if 'data.json' not in file_root:
            file_obj = open('data.json', "a+")
            config_file = file_obj.read(1)
            print(config_file)
            if config_file == '':
                file_obj.write("{}")
            file_obj.close()
