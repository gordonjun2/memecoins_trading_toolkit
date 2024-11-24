import os
import json
import sys
from datetime import datetime
import pytz
from tzlocal import get_localzone


def load_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("\n{} not found or is invalid.\n".format(file_path))
        return {}


def save_json_file(file_path, data):
    with open(file_path, 'w') as f:
        if isinstance(data, list):
            json.dump(data, f, separators=(',', ':'), ensure_ascii=False)
        else:
            json.dump(data, f, indent=4)


def load_txt_file_to_list(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        lines = [line.strip() for line in lines]
        return lines
    except FileNotFoundError:
        print("\nThe file not found or is invalid.\n")
        sys.exit(1)


def can_be_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def convert_utc_to_user_timezone(utc_time_str):
    utc_time = datetime.strptime(utc_time_str,
                                 "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)
    local_timezone = get_localzone()
    user_time = utc_time.astimezone(local_timezone)

    return user_time


def is_list_of_strings(variable):
    return isinstance(variable, list) and all(
        isinstance(item, str) for item in variable)


def is_list_of_dicts(variable):
    return isinstance(variable, list) and all(
        isinstance(item, dict) for item in variable)
