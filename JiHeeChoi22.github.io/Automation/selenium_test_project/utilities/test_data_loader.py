import csv
import json
import os

def read_test_data(file_name):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_data", file_name)
    
    if file_name.endswith('.csv'):
        return read_csv_data(file_path)
    elif file_name.endswith('.json'):
        return read_json_data(file_path)
    else:
        raise ValueError(f"지원하지 않는 파일 형식: {file_name}")

def read_csv_data(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def read_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file) 