from playwright.sync_api import sync_playwright, TimeoutError
import sqlite3
from datetime import datetime
from Mail import Send_Listing
import re

def insert_listing_into_database(query, entries):
    # Connect to the database
    conn = sqlite3.connect(f"Databases/marketplace_{query}.db")
    cursor = conn.cursor()
    insert_count = 0
    try:
        # Check if the listing database already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='listings'")
        table_exists = cursor.fetchone()

        # if the listing database does not exist then create a new database
        if not table_exists:
            create_database(cursor)

        # iterate through each item in the entires list and add to database if is not in it yet
        for listing_info in entries:
            # Check if the listing_info already exists in the list
            cursor.execute("SELECT COUNT(*) FROM listings WHERE price=? AND title=? AND location=? AND description=? AND url=?", (listing_info[0], listing_info[1], listing_info[2], listing_info[3], listing_info[4]))
            count = cursor.fetchone()[0]

            # put listing in database
            insert_count += insert_listing(conn, count, cursor, listing_info, table_exists)

    except sqlite3.Error as e:
        print(f"Error inserting listing: {e}")

    # Close the connection
    conn.close()
    return insert_count

def create_database(cursor):
    # Create the listings table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            price TEXT,
            title TEXT,
            location TEXT,
            description TEXT,
            url TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

def insert_listing(conn, count, cursor, listing_info, table_exists):
    # Insert the listing into the database table if it doesnt exist
    if count == 0:
        cursor.execute("""
            INSERT INTO listings (price, title, location, description, url, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
                       (listing_info[0], listing_info[1], listing_info[2], listing_info[3], listing_info[4],
                        datetime.now()))
        conn.commit()

        # email the URL if the listing is a newly posted item
        if table_exists:
            Send_Listing(listing_info[4])
            return 1

    # if already in table then do nothing
    else:
        pass
    return 0

def view_listings(query):
    # Connect to the database
    conn = sqlite3.connect(f"Databases/marketplace_{query}.db")
    cursor = conn.cursor()

    # Execute a SELECT query to fetch all rows from the table
    cursor.execute("SELECT * FROM listings")

    # Fetch all the rows returned by the query
    rows = cursor.fetchall()

    # Print the contents of the table
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

def Deal_Finder(query):
    with sync_playwright() as playwright:
        # Launch the browser and create a new page
        browser = playwright.chromium.launch()
        page = browser.new_page()

        search_URL = f'https://www.facebook.com/marketplace/boston/search?daysSinceListed=1&deliveryMethod=local_pick_up&sortBy=best_match&query={query}&exact=true'

        # Navigate to the search page
        page.goto(search_URL)
        page.wait_for_selector('[class="xkrivgy x1gryazu x1n2onr6"]')

        # Find all the item links on the page
        locators = page.query_selector_all('[class="xkrivgy x1gryazu x1n2onr6"] a')

        elCount = len(locators)

        entries = []

        for index in range(elCount):
            element = locators[index]
            innerText = element.inner_text()
            href = element.get_attribute('href')

            # Extract price, title, and location information
            parts = innerText.split('\n')
            if is_dollar_integer(parts[0]) and is_dollar_integer(parts[1]):
                price = parts[0].strip()
                title = parts[2].strip()
                location = parts[3].strip()
            else:
                price = parts[0].strip()
                title = parts[1].strip()
                location = parts[2].strip()

            description = ""


            # Open URL of specific item in a new page
            URL = 'https://www.facebook.com/' + href
            # item_page = browser.new_page()
            # item_page.goto(URL)
            #
            # try:
            #     #print(f"Finding Description for {price} {title}")
            #     # Wait for the description element to appear
            #     element = item_page.wait_for_selector('[class="xz9dl7a x4uap5 xsag5q8 xkhd6sd x126k92a"]', timeout=1)
            #     full_text = element.inner_text()
            #     # Count the number of lines and split text into a list so it can be indexed
            #     # reaoon for this is because the element variable spits a bunch of data back, I found description starts at line 11 and posts with no description data have 19 lines
            #     lines = full_text.count("\n")
            #     text_lines = full_text.split('\n')
            #     description_lines = lines - 19
            #     description_start = 11
            #
            # except TimeoutError:
            #     pass
            #     #print(f"Element not found within the timeout period.\nURL = {URL}")

            # Append all information to entries list
            item_info = [price, title, location, description, URL]
            entries.append(item_info)

        # Close the browser
        items_found = insert_listing_into_database(query, entries)
        browser.close()
        print(f"URL Search: {search_URL}")
    return items_found

def is_dollar_integer(string):
    pattern = r'^\$[0-9]{1,3}(?:,[0-9]{3})*$'
    return bool(re.match(pattern, string))

