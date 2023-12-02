import json


class Utils:
    def read_language_files(language):
        file_path = f'language/{language}.json'
        with open(file_path, 'r') as file:
            return json.load(file)
