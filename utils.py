import json
from datetime import datetime
import pandas as pd
from cryptography.fernet import Fernet


class Utils:
    _key = None
    _cipher_suite = None

    @staticmethod
    def generate_and_store_key():
        """Generate a key for encryption and store it securely."""
        Utils._key = Fernet.generate_key()
        Utils._cipher_suite = Fernet(Utils._key)
        # Store the key securely (e.g., in an environment variable or secure storage)
        with open('secret.key', 'wb') as key_file:
            key_file.write(Utils._key)

    @staticmethod
    def load_key():
        """Load the key from secure storage."""
        if Utils._key is None:
            with open('secret.key', 'rb') as key_file:
                Utils._key = key_file.read()
            Utils._cipher_suite = Fernet(Utils._key)

    @staticmethod
    def read_language_files(language: str):
        file_path = f'language/{language}.json'
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def check_and_apply_filter_dates(start_date, end_date, dataframe) -> pd.DataFrame:
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        elif end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            start_date = dataframe['date'].min()
        else:
            start_date = dataframe['date'].min()
            end_date = dataframe['date'].max()

        return dataframe[
            (dataframe['date'] >= start_date) & (dataframe['date'] <= end_date)
        ]

    @staticmethod
    def encrypt_file(file_path):
        Utils.load_key()
        with open(file_path, 'rb') as file:
            file_data = file.read()
        encrypted_data = Utils._cipher_suite.encrypt(file_data)
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)

    @staticmethod
    def decrypt_file(file_path):
        Utils.load_key()
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = Utils._cipher_suite.decrypt(encrypted_data)
        with open(file_path, 'wb') as file:
            file.write(decrypted_data)
