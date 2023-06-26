from DealFinder import *
import random
import time
from datetime import datetime

# User itmers they want to search. Input as array of strings.  example below is Iphone
search_items = ["iphone"]

while True:
    # USER VARIABLES
    search_rate = 5 #minutes
    randomness = 1 # minutes

    #init variables
    items_found = 0

    # get values in seconds
    search_seconds = search_rate * 60
    random_seconds = randomness * 60

    # update search rate with randomness
    random_search_variation = random.uniform(-random_seconds, random_seconds)
    updated_search_rate = search_seconds + random_search_variation

    #current time
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H:%M")

    # perform search
    search_start_time = datetime.now().timestamp()
    searched_items = []
    for item in search_items:
        scanner = MarketplaceDealFinder(item)
        scanner.find_deals()
        items_found += scanner.items_found

    #get search time
    search_end_time = datetime.now().timestamp()
    search_time = round(search_end_time - search_start_time)

    print(f"{formatted_time} - Search time: {search_time} seconds.  New items found = {items_found}")
    time.sleep(updated_search_rate)