from DealFinder import *
from datetime import datetime

def create_new_scanners(search_struct):
    scanners = []
    lists = 0
    for search in search_struct:
        title = search.title
        search_list = search.get_list()
        email = search.email
        town = search.town
        for item in search_list:
            scanners.append(MarketplaceDealFinder(title, item, email, town))
            lists += 1
    return scanners

def run_scanner(scanners):
    # init variables
    items_found = 0
    items_searched = 0

    # current time
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H:%M")

    # perform search
    search_start_time = datetime.now().timestamp()
    searched_items = []
    for keyword_scanner in scanners:
        keyword_scanner.items_searched = 0
        keyword_scanner.items_found = 0
        keyword_scanner.find_deals()
        items_searched += keyword_scanner.items_searched
        items_found += keyword_scanner.items_found

    # get search time
    search_end_time = datetime.now().timestamp()
    search_time = round(search_end_time - search_start_time)

    return f"{formatted_time} - Search time: {search_time} seconds. Items Search = {items_searched},  New items found = {items_found}"

