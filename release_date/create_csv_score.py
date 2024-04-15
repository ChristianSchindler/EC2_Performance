import pandas as pd
import re
from general_benchmark.data_parsing.main import find_file, get_DH
import os


def find_folder(start_path, folder_prefix):
    start_path = os.path.abspath(start_path)
    # Check if the start_path is a directory
    if not os.path.isdir(start_path):
        print(f"Error: {start_path} is not a valid directory.")
        return None

    # Walk through the directory tree starting from start_path
    for root, dirs, files in os.walk(start_path):
        for dir_name in dirs:
            # Check if the directory name starts with the specified prefix
            if dir_name.startswith(folder_prefix+ '.metal-48xl'):
                return os.path.join(root, dir_name)
    for root, dirs, files in os.walk(start_path):
        for dir_name in dirs:
            # Check if the directory name starts with the specified prefix
            if dir_name.startswith(folder_prefix+ '.metal'):
                return os.path.join(root, dir_name)
    for root, dirs, files in os.walk(start_path):
        for dir_name in dirs:
            # Check if the directory name starts with the specified prefix
            if dir_name.startswith(folder_prefix):
                return os.path.join(root, dir_name)
    return None  # Return None if folder is not found


def singe(file_name):
    # Read the CSV file
    df = pd.read_csv(f'{file_name}.csv')
    scoer = []
    for i, row in df.iterrows():
        directory_path = '../s3/results/2-general_benchmark'

        # Get a list of all items (files and folders) in the directory

        path = find_folder(directory_path, row['Name'])
        print(path)
        with open(path + '/' + find_file(path), 'r') as file:
            pattern = re.compile(rf'System Benchmarks Index Score\s+([\d.]+)')
            content = file.read()
            matches = pattern.findall(content)
            scoer.append(matches[0])

    # Add a new column with the specified values
    df['score'] = scoer

    # Save the DataFrame to a new CSV file
    df.to_csv(f'{file_name}_single.csv', index=False)


def multi(file_name):
    # Read the CSV file
    df = pd.read_csv(f'{file_name}.csv')
    scoer = []
    for i, row in df.iterrows():
        directory_path = '../s3/results/2-general_benchmark'

        # Get a list of all items (files and folders) in the directory

        path = find_folder(directory_path, row['Name'])
        print(path)
        with open(path + '/' + find_file(path), 'r') as file:
            pattern = re.compile(rf'System Benchmarks Index Score\s+([\d.]+)')
            content = file.read()
            matches = pattern.findall(content)
            scoer.append(matches[1])

    # Add a new column with the specified values
    df['score'] = scoer

    # Save the DataFrame to a new CSV file
    df.to_csv(f'{file_name}_multi.csv', index=False)

def singe_dray(file_name):
    # Read the CSV file
    df = pd.read_csv(f'{file_name}.csv')
    scoer = []
    for i, row in df.iterrows():
        directory_path = '../s3/results/2-general_benchmark'

        # Get a list of all items (files and folders) in the directory

        path = find_folder(directory_path, row['Name'])
        print(path)
        with open(path + '/' + find_file(path), 'r') as file:

            scoer.append(float(get_DH(file.read())[0][2]))

    # Add a new column with the specified values
    df['score'] = scoer

    # Save the DataFrame to a new CSV file
    df.to_csv(f'{file_name}_single_dray.csv', index=False)

def multi_dray(file_name):
    # Read the CSV file
    df = pd.read_csv(f'{file_name}.csv')
    scoer = []
    for i, row in df.iterrows():
        directory_path = '../s3/results/2-general_benchmark'

        # Get a list of all items (files and folders) in the directory

        path = find_folder(directory_path, row['Name'])
        print(path)
        with open(path + '/' + find_file(path), 'r') as file:

            scoer.append(float(get_DH(file.read())[1][2]))

    # Add a new column with the specified values
    df['score'] = scoer

    # Save the DataFrame to a new CSV file
    df.to_csv(f'{file_name}_multi_dray.csv', index=False)


if __name__ == '__main__':
    for csv in ['intel_data', 'amd_data', 'graviton_data']:
        singe(csv)
        multi(csv)
        singe_dray(csv)
        multi_dray(csv)
