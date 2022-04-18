# Process

We need two lists of video games for this project to work well:
    - A reasonably long list of game titles, for users to choose from.
    - A list of curated games with screenshots, to guess.

For this process, we build a very long list of games, scrape all the data, and then do a final round of processing for screenshots and descriptions manually.

## Attempt One

Attempt one: take the top 2,500 games by rating from the Steam Store.

This didn't work too well! Top rated games are done by percentage on Steam, which leads to a lot of really obscure games with dedicated fanbases. Not quite what we're after! Also, we're missing a lot of more controversial games - the entire GTA franchise is missing, for example.

We want a mix of 'hidden gems' & well-known games.

## Attempt Two

Take the top 500/1000/whatever games by rating from the Steam Store, plus all the games by a list of given publishers.

See scrape_publishers.py for details

## Processing Scripts

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
