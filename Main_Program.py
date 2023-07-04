from Scanners import *
import random
from SearchStruct import *
from Update_Database import *
import time

# USER INPUT VARIABLES
# limit 6 keywords per search list
search_1 = ["cdj", "djm", "dj flight case", "DJS-1000", "Maschine+"]
search_2 = ["Honda Generators"]
search_3 = ["ev zlx", "ev elx", "electrovoice", "jbl sub", "qsc speakers", "qsc amplifier", "crown amplifier"]
search_4 = ["Toyota Tundra"]

search_5 = ["Maschine+", "CDJ"]

town = "YOUR TOWN"
email = "youremail@email.com"

DJ = SearchDataStructure("DJ Equipment", search_1, email, town)
Generators = SearchDataStructure("Generators", search_2, email, town)
Speakers = SearchDataStructure("Speakers", search_3, email, town)
Trucks = SearchDataStructure("Trucks", search_4, email, town)
testing = SearchDataStructure("Testing", search_5, email, town)


search_list = [Generators]
request_DB_update = True

#search times
search_rate = 5  # minutes
randomness = 1  # minutes

# PROGRAM VARIABLES
# get values in seconds
search_seconds = search_rate * 60
update_time_start = datetime.now().timestamp()



# -----------------------------------------------------------------
#                         MAIN FUNCTION
# -----------------------------------------------------------------


scanners = create_new_scanners(search_list)

while True:
    # update search rate with randomness
    random_seconds = randomness * 60
    random_search_variation = random.uniform(-random_seconds, random_seconds)
    updated_search_rate = search_seconds + random_search_variation

    # Run scanners every 5 minutes
    print("Running Scanners")
    print(run_scanner(scanners))

    # Update database for 90 seconds, rest for 2 minutes
    update = datetime.now().timestamp() > update_time_start
    start_time = datetime.now().timestamp()
    update_time = 0
    everything_updated = False

    # TODO: if redirected to the login page, do not update dataset for 60 minutes
    if ask_login(scanners[0]) and update and request_DB_update:
        update = False
        print("Asked for login")
        update_time_start = datetime.now().timestamp() + (12 * updated_search_rate)

    if update == False:
        print(f"Next update request in {convert_seconds(round(update_time_start - datetime.now().timestamp()))}")

    # Run update_database for 90 seconds
    while update == True and request_DB_update:
        # check if there is a dataset to update
        update = False
        for scanner in scanners:
            if scanner.check_db_updated() == False:
                update = True
                #TODO: if fully updated with information, indicate that all listings are updated
                print(f"Updating Scanner: {scanner.query}")
                update_database(scanner)
                update_time = round(datetime.now().timestamp() - start_time)
                # only update for 2 minutes to avoid facebook detection
                if (update_time) > 120:
                    update = False
                    break

        if (update_time) > 120:
            update = False

    # Rest
    rest_time = max(0, updated_search_rate - update_time)
    if update == True:
        print(f"Update time: {convert_seconds(update_time)} seconds, now resting {convert_seconds(rest_time)} seconds")
    else:
        print(f"Resting {convert_seconds(rest_time)} seconds")
    time.sleep(rest_time)  # Rest


