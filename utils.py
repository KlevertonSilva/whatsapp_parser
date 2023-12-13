import json
from datetime import datetime
import pandas as pd


class Utils:
    def read_language_files(language: str):
        file_path = f'language/{language}.json'
        with open(file_path, 'r') as file:
            return json.load(file)

    def check_and_apply_filter_dates(start_date,
                                     end_date,
                                     dataframe) -> pd.DataFrame:

        # Filter chat DataFrame based on date range
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
