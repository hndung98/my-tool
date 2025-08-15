import json
import shutil
import time
from datetime import datetime
from functools import wraps
from os import listdir, unlink, urandom
from os.path import isdir, isfile, islink, join
from pathlib import Path


def timer(func):
    """Print the runtime of the decorated function"""

    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        print("Started at " + str(datetime.now()))
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__}() in {run_time:.4f} secs \n")
        return value

    return wrapper_timer


def debugger(func):
    """Avoid exception when calling a function"""

    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        try:
            value = func(*args, **kwargs)
            return value
        except Exception as e:
            print(str(e))
            return None

    return wrapper_timer


def ensure_extension(filename, ext="txt"):
    extension = "." + ext
    if not filename.endswith(extension):
        filename += extension
    return filename


def read_filename(folder_path, filename):
    output_filename = "./uploads/output/text/" + ensure_extension(filename)
    file_path = Path(output_filename)

    # delete file
    if file_path.exists():
        file_path.unlink()

    path = folder_path
    files = [f for f in listdir(path) if isfile(join(path, f))]

    with open(output_filename, "w", encoding="utf-8") as file:
        for f in files:
            file.write(f + "\n")


def remove_all_files(folder):
    for filename in listdir(folder):
        file_path = join(folder, filename)
        try:
            if isfile(file_path) or islink(file_path):
                unlink(file_path)
            elif isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def read_all_lines(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        return [line.replace("\n", "") for line in lines]
    except FileNotFoundError:
        print(f"'{file_path}' does not exist.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []


@debugger
def print_text_file(filename, text):
    file_path = "./uploads/output/text/" + ensure_extension(filename)
    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as file:
        if text != None:
            file.write(text)
        else:
            file.write("something went wrong..")


@debugger
def print_json_file(filename, data):
    file_path = "./uploads/output/json/" + ensure_extension(filename, "json")
    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as file:
        if data != None:
            file.write(json.dumps(data, ensure_ascii=False, indent=4))


def print_random_key():
    print_text_file("random_key", str(urandom(24)))
