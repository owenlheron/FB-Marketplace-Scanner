import sqlite3
from datetime import datetime
from playwright.sync_api import sync_playwright

def insert_listing_into_database(listing_info):
    # Connect to the database
    conn = sqlite3.connect("../Databases/marketplace.db")
    cursor = conn.cursor()

    # Insert the listing into the database table
    cursor.execute("INSERT INTO listings (price, title, location, description, url, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                   (listing_info[0], listing_info[1], listing_info[2], listing_info[3], listing_info[4], datetime.now()))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def Deal_Finder(query):
    with sync_playwright() as playwright:
        # Launch the browser and create a new page
        browser = playwright.chromium.launch()
        page = browser.new_page()

        # Navigate to the search page
        page.goto(f'https://www.facebook.com/marketplace/boston/search?sortBy=creation_time_descend&query={query}&exact=true')
        page.wait_for_selector('[aria-label="Collection of Marketplace items"]')

        # Find all the item links on the page
        locators = page.query_selector_all('[aria-label="Collection of Marketplace items"] a')
        elCount = len(locators)

        entries = []

        for index in range(elCount):
            element = locators[index]
            innerText = element.inner_text()
            href = element.get_attribute('href')

            # Extract price, title, and location information
            parts = innerText.split('\n')
            price = parts[0].strip()
            title = parts[1].strip()
            location = parts[2].strip()
            description = ""

            # Open URL of specific item in a new page
            URL = 'https://www.facebook.com/' + href
            item_page = browser.new_page()
            item_page.goto(URL)

            try:
                print(f"Finding Description for {price} {title}")
                # Wait for the description element to appear
                element = item_page.wait_for_selector('[class="xz9dl7a x4uap5 xsag5q8 xkhd6sd x126k92a"]', timeout=1)
                full_text = element.inner_text()
                # Count the number of lines and split text into a list so it can be indexed
                # The reason for this is because the element variable contains a bunch of data.
                # I found that the description starts at line 11, and posts with no description data have 19 lines.
                lines = full_text.count("\n")
                text_lines = full_text.split('\n')
                description_lines = lines - 19
                description_start = 11

                # Extract the description from the lines
                description = "\n".join(text_lines[description_start: description_start + description_lines])

            except TimeoutError:
                print(f"Element not found within the timeout period.\nURL = {URL}")

            # Append all information to entries list
            item_info = [price, title, location, description, URL]
            entries.append(item_info)
            insert_listing_into_database(item_info)

        # Close the browser
        browser.close()
    return

import sqlite3

def view_listings():
    # Connect to the database
    conn = sqlite3.connect("../Databases/marketplace.db")
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

Deal_Finder('iphone')
view_listings()