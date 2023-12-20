import os
import csv
import pandas as pd
from dotenv import load_dotenv

FILE_PATH = os.getcwd()
ALL_FILES = os.listdir(FILE_PATH)
PRIMARY_FILE = min(ALL_FILES, key = lambda file: os.path.getctime(os.path.join(FILE_PATH, file)), default = "Empty")
FILE_STEM = 'Report Results'

def find_files(PRIMARY_FILE):
    try:
        filtered_files = [file for file in ALL_FILES if file.startswith(FILE_STEM)]
        
        if not filtered_files:
            raise FileNotFoundError(f"No file starting with {FILE_STEM} found in the specified directory.")

        input_file = min(filtered_files, key = lambda file: os.path.getctime(os.path.join(FILE_PATH, file)), default = "Empty")

    except FileNotFoundError as e:
        print("Error:", e)
        input_file = "Empty"

    except Exception as e:
        print("An unexpected error occurred:", e)
        input_file = "Empty"

    return input_file

def clean_file(input_file):
    output_file = input_file

    if input_file.endswith('.csv'):
        df = pd.read_csv(os.path.join(FILE_PATH, input_file))
    elif input_file.endswith('.xlsx'):
        df = pd.read_excel(os.path.join(FILE_PATH, input_file))

    last_row = len(df)
    df = df.iloc[:, 1:]
    df = df[:-2]

    unwanted_chars = ['\n', ',', "'"]
    replacement_char = ' '

    for col in df.columns:
        for index, value in enumerate(df[col]):
            if isinstance(value, str):
                for char in unwanted_chars:
                    value = value.replace(char, replacement_char)
                df.at[index, col] = value

    if input_file.endswith('.csv'):
        df.to_csv(os.path.join(FILE_PATH, output_file), index = False)
    elif input_file.endswith('.xlsx'):
        df.to_excel(os.path.join(FILE_PATH, output_file), index = False)

def main(input_file):
    input_file = find_files(input_file)
    if input_file != "Empty":
        clean_file(input_file)

if __name__ == "__main__":
    main(PRIMARY_FILE)