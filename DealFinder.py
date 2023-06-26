from playwright.sync_api import sync_playwright, TimeoutError
import sqlite3
from datetime import datetime
from Mail import Send_Listing
import re


class MarketplaceDealFinder:
    def __init__(self, query):
        self.query = query
        self.conn = None
        self.cursor = None
        self.items_found = 0

    def check_listing_existence(self, listing_info):
        self.cursor.execute(
            "SELECT COUNT(*) FROM listings WHERE price=? AND title=? AND location=? AND url=?",
            (listing_info[0], listing_info[1], listing_info[2], listing_info[4]))
        count = self.cursor.fetchone()[0]
        return count

    def check_database_existence(self):
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='listings'")
        table_exists = self.cursor.fetchone()
        return table_exists

    def create_database(self, search_URL):
        # Create the listings table if it doesn't exist
        self.cursor.execute("""
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
        self.cursor.execute("""
            INSERT INTO listings (price, title, location, description, url, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
                            ("MAIN SEARCH URL", "", "", "", search_URL, datetime.now()))
        self.conn.commit()

    def insert_listing(self, listing_info):
        # Connect to the database
        self.cursor.execute("""
            INSERT INTO listings (price, title, location, description, url, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
                            (listing_info[0], listing_info[1], listing_info[2], listing_info[3], listing_info[4],
                             datetime.now()))
        self.conn.commit()
        return 1

    def get_description(self, browser, URL):
        #TODO: make this work, does not return data, instead time out. Sometimes work, but doesn't last

        # Navigate to the search page using URL
        item_page = browser.new_page()
        item_page.goto(URL)
        try:
            item_element = item_page.wait_for_selector(
                '[class="xz9dl7a x4uap5 xsag5q8 xkhd6sd x126k92a"]', timeout=00)
            description = item_element.inner_text()
        # no description
        except TimeoutError:
            description = ""

        # create list with item info
        return description

    @staticmethod
    def is_dollar_integer(string):
        pattern = r'^\$[0-9]{1,3}(?:,[0-9]{3})*$'
        return bool(re.match(pattern, string))

    def find_deals(self):
        items_found = 0
        with sync_playwright() as playwright:
            # Launch the browser and create a new page
            browser = playwright.chromium.launch()
            page = browser.new_page()

            search_URL = f'https://www.facebook.com/marketplace/boston/search?daysSinceListed=1&deliveryMethod=local_pick_up&sortBy=best_match&query={self.query}&exact=true'

            # Navigate to the search page
            page.goto(search_URL)
            page.wait_for_selector('[class="xkrivgy x1gryazu x1n2onr6"]')

            # Find all the item links on the page
            locators = page.query_selector_all('[class="xkrivgy x1gryazu x1n2onr6"] a')

            elCount = len(locators)

            # connect to database
            self.conn = sqlite3.connect(f"Databases/marketplace_{self.query}.db")
            self.cursor = self.conn.cursor()

            database_exists = self.check_database_existence()
            new_entries = []
            send_mail = database_exists

            for index in range(elCount):
                element = locators[index]
                innerText = element.inner_text()
                href = element.get_attribute('href')

                # Extract price, title, and location information
                parts = innerText.split('\n')
                if self.is_dollar_integer(parts[0]) and self.is_dollar_integer(parts[1]):
                    price = parts[0].strip()
                    title = parts[2].strip()
                    location = parts[3].strip()
                else:
                    price = parts[0].strip()
                    title = parts[1].strip()
                    location = parts[2].strip()

                # Open URL of specific item in a new page to get description
                URL = 'https://www.facebook.com/' + href
                description = ""
                item_info = [price, title, location, description, URL]

                if not database_exists:
                    self.create_database(search_URL)
                    database_exists = True

                if not self.check_listing_existence(item_info):
                    #TODO: get item description
                    #description = self.get_description(browser, URL)

                    # create list with updated item info
                    item_info = [price, title, location, description, URL]
                    self.insert_listing(item_info)
                    self.items_found += 1

                    # send an email with URL if this is a new post
                    if send_mail:
                        Send_Listing(item_info[1], item_info[4], item_info[0], self.query)

            # Close the browser
            browser.close()
            self.conn.close()

