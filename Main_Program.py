from DealFinder import *
import random
import time
from datetime import datetime

search_items = ["electrovoice", "cdj", "djm"]

while True:
    # USER VARIABLES
    search_rate = 5 #minutes
    randomness = 1 # minutes

    # get values in seconds
    search_seconds = search_rate * 60
    random_seconds = 5 * 60

    # update search rate with randomness
    random_search_variation = random.uniform(-random_seconds, random_seconds)
    updated_search_rate = search_seconds + random_search_variation

    items_found = 0
    # perform search
    for item in search_items:
        items_found += Deal_Finder(item)

    print(f"Search completed at {datetime.now()}.  Items found = {items_found}")
    time.sleep(updated_search_rate)