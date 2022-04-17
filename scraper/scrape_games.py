from bs4 import BeautifulSoup
import json
import progressbar
import requests

RESULTS_PER_PAGE = 100
NUMBER_OF_PAGES = 25


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

    details = extract_glance_content(soup)
    details["screenshots"] = extract_screenshot_links(soup)
    details["steamid"] = steamid
    return details


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


if __name__ == "__main__":
    game_ids = []
    for page in range(NUMBER_OF_PAGES):
        game_ids += get_top_games(page)

    details = []
    for game_id in progressbar.progressbar(game_ids):
        details.append(get_info_for_game(game_id))

    with open("game_details.json", "w") as f:
        json.dump(details, f)
