import json
import os
import progressbar
import random
import requests
from PIL import Image
from multiprocessing.pool import ThreadPool
from urllib.parse import urlparse

POOL_SIZE = 5
IMAGE_RESOLUTION = (1920, 1080)
SKIP_EXISTING = True


def filename_from_url(url, directory):
    """Given a URL, guess a filename for it
    """
    basename = os.path.basename(urlparse(url).path)
    return os.path.join(directory, basename)


def download_screenshot(url, directory):
    """Download a game screenshot, resizing and converting to .jpg as required
    """
    filename = filename_from_url(url, directory).replace(".png", ".jpg")
    resp = requests.get(url, stream=True)
    img = Image.open(resp.raw)
    img = img.resize(IMAGE_RESOLUTION)
    img.save(filename, quality=90)


def censor_description(title, description):
    """Attempt to hide the title from descriptions
    """
    censor = "".join(["■"] * random.randint(4, 10))
    description = description.replace(title, censor)
    return description.replace(title.upper(), censor)


def process_game(data):
    output_dir = os.path.join("output", data.get("steamid"))
    try:
        os.makedirs(output_dir)
    except OSError:
        if not SKIP_EXISTING:
            return
        else:
            pass

    # Clean the data up a little
    sanitized_data = {
        "title": data.get("title"),
        "description": censor_description(data.get("title"), data.get("description")),
        "release_year": data.get("release_date").split(" ")[-1],
        "tags": data.get("tags")[:5],
        "steamid": data.get("steamid"),
    }

    with open(os.path.join(output_dir, "info.json"), "w") as f:
        f.write(json.dumps(sanitized_data))

    # Download all the screenshots
    for screenshot in data.get("screenshots"):
        download_screenshot(screenshot, output_dir)


def process_game_list(data):
    # Save all titles to a file for easy access
    os.makedirs("output", exist_ok=True)
    all_titles = [x.get("title") for x in data]
    with open("output/titles.json", "w") as f:
        json.dump(all_titles, f)

    # Save info + screenshots into subdirectories
    pool = ThreadPool(POOL_SIZE).imap_unordered(process_game, data)
    for _ in progressbar.progressbar(pool, max_value=len(data)):
        pass


if __name__ == "__main__":
    with open("game_details.json", encoding="utf-8") as f:
        process_game_list(json.load(f))
