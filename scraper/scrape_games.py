from bs4 import BeautifulSoup
import json
import progressbar
import requests


RESULTS_PER_PAGE = 100
NUMBER_OF_TOP_GAMES_PAGES = 10
PUBLISHERS_TO_SCRAPE = [
    "Valve",
    "2K",
    "Bethesda",
    "Ubisoft",
    "SEGA",
    "EA",
    "Chucklefish",
    "DevolverDigital",
    "CoffeeStain",
    "BANDAINAMCO",
    "XboxGameStudios",
    "paradoxinteractive",
    "rockstargames",
    "tinybuild",
    "WBGames",
    "deepsilver",
    "THQNordic",
    "505Games"
]


def extract_glance_content(soup):
    """Extract content from the right sidebar
    This will return the description, tags, and release date for the game
    """
    try:
        glance = soup.find(class_="glance_ctn")

        # Don't Starve has no release date??
        if glance.find(class_="date"):
            release_date = glance.find(class_="date").text
        else:
            release_date = "Unknown"

        return {
            "title": glance.find(class_="apphub_AppName").text.strip(),
            "description": glance.find(class_="game_description_snippet").text.strip(),
            "tags": [tag.text.strip() for tag in glance.find_all(class_="app_tag")][:-1],
            "release_date": release_date
        }
    except Exception as e:
        print(glance.find(class_="apphub_AppName").text.strip())
        raise e


def extract_screenshot_links(soup):
    """Extract links for all the screenshots for this game
    Downloading is to be handled seperately!
    """
    return [sc.get("href") for sc in soup.find_all(class_="highlight_screenshot_link")]


def get_info_for_game(steamid):
    """Given a SteamID, extract info for that game
    """
    url = f"https://store.steampowered.com/app/{steamid}"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")

    try:
        details = extract_glance_content(soup)
        details["screenshots"] = extract_screenshot_links(soup)
        details["steamid"] = steamid
        return details
    except Exception:
        print("Error!", steamid)
        return None


def get_top_games(page_number):
    """Get SteamIDs for the top games on the steam
    """
    start = page_number * RESULTS_PER_PAGE
    url = f"https://store.steampowered.com/search/results/?query&start={start}&count={RESULTS_PER_PAGE}"
    url += "&dynamic_data=&sort_by=Reviews_DESC&category1=998&supportedlang=english&snr=1_7_7_230_7&infinite=1"

    resp = requests.get(url)
    data = resp.json()
    if data.get("success") != 1:
        raise Exception("Got bad response from API!")
    else:
        soup = BeautifulSoup(data.get("results_html"), "html.parser")
        games = soup.find_all(class_="search_result_row")
        return [game.get("data-ds-appid") for game in games]


def get_publisher_games(publisher, page_number=0):
    """Get SteamIDs for all games by a given publisher
    """
    start = page_number * RESULTS_PER_PAGE
    end = (page_number + 1) * RESULTS_PER_PAGE
    url = f"https://store.steampowered.com/publisher/{publisher}/ajaxgetfilteredrecommendations/"
    url += f"?query&start={start}&count={RESULTS_PER_PAGE}"
    url += "&dynamic_data=&tagids=&sort=newreleases&app_types=game&curations=&reset=false"

    resp = requests.get(url)
    data = resp.json()
    if data.get("success") != 1:
        raise Exception("Got bad response from API!")
    else:
        soup = BeautifulSoup(data.get("results_html"), "html.parser")
        games = soup.find_all(class_="store_capsule")
        next_page = [] if end >= data.get("total_count") else get_publisher_games(publisher, page_number + 1)
        return [game.get("data-ds-appid") for game in games] + next_page


if __name__ == "__main__":
    game_ids = set()

    # Get some of the top rated Steam games
    for page in range(NUMBER_OF_TOP_GAMES_PAGES):
        game_ids.update(get_top_games(page))

    # Get games by certain publishers
    for publisher in PUBLISHERS_TO_SCRAPE:
        game_ids.update(get_publisher_games(publisher))

    # Convert set back to a list
    game_ids = list(game_ids)

    # Fetch details for all the game IDs we have
    details = []
    for game_id in progressbar.progressbar(game_ids):
        info = get_info_for_game(game_id)
        if info is not None:
            details.append(info)

    with open("game_details.json", "w") as f:
        json.dump(details, f)
