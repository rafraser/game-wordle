scrape_games.py
    - Get a list of the top N games from the Steam store

download_game_screenshots.py
    - Download all the screenshots from these games (multi-threaded so it doesn't take an eternity)
    - Also do a first pass on the descriptions - try and censor titles or other obvious details

From here, the data needs to be processed manually. For each game, 6 screenshots should be picked - ideally from 'least obvious' to 'incredibly obvious'.
These should be renamed from 1.jpg to 6.jpg.

finalise_processing.py
    - Look through any folders in the output directory
    - Compute an MD5 hash so the SteamID isn't given away
    - If it has 1.jpg to 6.jpg, copy all the files to processed directory
    - Shuffle the list of ready SteamIDs so we can pick one each day
