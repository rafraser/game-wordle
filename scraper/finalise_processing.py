import hashlib
import json
import os
import shutil
from random import shuffle

INPUT_DIR = "output - Copy"
OUTPUT_DIR = "assets"

ready_hashes = []


def obfuscate_id(steamid):
    # tested to have no collisions up until 5000000
    return hashlib.sha224(steamid.encode('utf-8')).hexdigest()[:12]


def copy_across_if_ready(id):
    directory = os.path.join(INPUT_DIR, id)
    files_to_check = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "info.json"]
    if all(os.path.exists(os.path.join(directory, file)) for file in files_to_check):
        hash = obfuscate_id(id)
        new_directory = os.path.join(OUTPUT_DIR, hash)
        os.makedirs(new_directory, exist_ok=True)

        for file in files_to_check:
            shutil.copy(os.path.join(directory, file), os.path.join(new_directory, file))
        ready_hashes.append(hash)


def process():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(os.listdir(INPUT_DIR))
    all_directories = [dir for dir in os.listdir(INPUT_DIR) if os.path.isdir(os.path.join(INPUT_DIR, dir))]
    print(all_directories)
    for id in all_directories:
        copy_across_if_ready(id)

    # Shuffle the hashes so we get a nice random order
    shuffle(ready_hashes)

    with open(os.path.join(OUTPUT_DIR, "ready.json"), "w") as f:
        json.dump(ready_hashes, f)


if __name__ == "__main__":
    process()
