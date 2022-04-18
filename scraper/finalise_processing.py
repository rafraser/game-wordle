import hashlib
import json
import os
import shutil
import datetime
from random import shuffle

INPUT_DIR = "output"
OUTPUT_DIR = "assets"
EPOCH = datetime.date(2022, 4, 18)

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


def process_game_list():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_directories = [dir for dir in os.listdir(INPUT_DIR) if os.path.isdir(os.path.join(INPUT_DIR, dir))]
    for id in all_directories:
        copy_across_if_ready(id)

    # Read in the existing hashes from ready.json
    # We don't want to change the order for games that have already been played (or are next up)
    # but everything else from there - fair game!
    existing_hashes = []
    try:
        days = (EPOCH - datetime.date.today()).days + 2
        with open(os.path.join(OUTPUT_DIR, "ready.json")) as f:
            existing_hashes = json.load(f)
            print(days)
            existing_hashes = existing_hashes[:days]
    except Exception:
        print("Could not read existing queue")
        pass

    # Shuffle the hashes so we get a nice random order
    final_hashes = [h for h in ready_hashes if h not in existing_hashes]
    shuffle(final_hashes)

    with open(os.path.join(OUTPUT_DIR, "ready.json"), "w") as f:
        json.dump(existing_hashes + final_hashes, f)


def process_titles():
    # Simple postprocessing-step: sort, remove duplicates, format nicely so I can sanity check it
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    titles = []
    with open(os.path.join(INPUT_DIR, "titles.json")) as f:
        titles = json.load(f)

    titles = sorted(list(set(titles)))
    with open(os.path.join(OUTPUT_DIR, "game_titles.json"), "w") as f:
        json.dump(titles, f, indent=4)


if __name__ == "__main__":
    # process_game_list()
    process_titles()
