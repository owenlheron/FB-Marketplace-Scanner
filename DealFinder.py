from playwright.sync_api import sync_playwright, TimeoutError
import sqlite3
from datetime import datetime
from Mail import Send_Listing
import re
import os
from Distance_Finder import find_distance

class MarketplaceDealFinder:
    def __init__(self, search_title, query, email, location):
        self.search_title = search_title
        self.query = query
        self.conn = None
        self.cursor = None
        self.items_found = 0
        self.email = email
        self.location = location
        self.browser = None
        self.items_searched = 0
        self.updated = True


    def check_listing_existence(self, listing_info):
        self.cursor.execute(
            "SELECT COUNT(*) FROM listings WHERE price=? AND title=? AND location=? AND url=?",
            (listing_info[0], listing_info[1], listing_info[2], listing_info[5]))
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
                distance TEXT,
                url TEXT,
                img TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.cursor.execute("""
            INSERT INTO listings (price, title, location, description, distance, url, img, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                            ("MAIN SEARCH URL", "", "", "", "", "", search_URL, datetime.now()))
        self.conn.commit()

    def insert_listing(self, listing_info):
        # Connect to the database
        self.cursor.execute("""
            INSERT INTO listings (price, title, location, description, distance, url, img, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                            (listing_info[0], listing_info[1], listing_info[2], listing_info[3], listing_info[4], listing_info[5], listing_info[6],
                             datetime.now()))
        self.conn.commit()
        return 1

    def check_db_updated(self):
        #initialize updated as true
        self.updated = True
        self.conn = sqlite3.connect(f"Databases/{self.search_title}/marketplace_{self.query}.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM listings")
        rows = self.cursor.fetchall()
        #if any instance of None or "None" then updated = false
        for row in rows:
            description_column = row[4]
            image_column = row[7]
            # Iterate through each row
            if description_column is None or description_column == "None" or image_column is None:
                self.updated = False

        return self.updated

    def get_description(self, URL):
        # Navigate to the search page using URL
        item_page = self.browser.new_page()
        item_page.goto(URL)
        try:
            item_element = item_page.wait_for_selector(
                '[class="xz9dl7a x4uap5 xsag5q8 xkhd6sd x126k92a"]', timeout=1000)
            description = item_element.inner_text()
        # no description
        except TimeoutError:
            description = "None"

        # create list with item info
        item_page.close()
        return description

    def get_images(self, URL):
        image_page = self.browser.new_page()
        # Launch the browser and create a new page
        # Navigate to the search page
        image_page.goto(URL)

        # Extract the description text
        try:
            try:
                #multiple photos
                element = image_page.wait_for_selector(
                    '[class="x6s0dn4 x78zum5 x193iq5w x1y1aw1k xwib8y2 xu6gjpd x11xpdln x1r7x56h xuxw1ft xc9qbxq"]',
                    timeout=1000)
            except:
                # only one photo
                element = image_page.wait_for_selector(
                    '[class="x6s0dn4 x78zum5 x1iyjqo2 xl56j7k x6ikm8r x10wlt62 xh8yej3 x1ja2u2z"]',
                    timeout=1000)
            # Extract the images
            # photo_descriptor = '[alt="Product photo of Honda EU2200 Generator"]'
            photo_descriptor = 'img'
            image_elements = element.query_selector_all(photo_descriptor)
            image_urls = [element.get_attribute('src') for element in image_elements]
        except:
            image_urls = None

        # Close the browser and return the result
        image_page.close()
        return image_urls

    @staticmethod
    def is_dollar_integer(string):
        pattern = r'^\$[0-9]{1,3}(?:,[0-9]{3})*$'
        return bool(re.match(pattern, string))

    def check_distance(self, listing_location):
        distance = find_distance(listing_location, self.location)
        return distance

    def find_deals(self, ):
        with sync_playwright() as playwright:
            # Launch the browser and create a new page
            self.browser = playwright.chromium.launch()
            page = self.browser.new_page()

            search_URL = f'https://www.facebook.com/marketplace/boston/search?daysSinceListed=1&deliveryMethod=local_pick_up&sortBy=best_match&query={self.query}&exact=true'

            # Navigate to the search page
            try:
                page.goto(search_URL)
            except:
                print(f"Cannot access URL: {search_URL}")
                return
            try:
                page.wait_for_selector('[class="xkrivgy x1gryazu x1n2onr6"]', timeout=1000)
            except TimeoutError:
                print(f"Error scraping HTML section: {search_URL}")

            # Find all the item links on the page
            locators = page.query_selector_all('[class="xkrivgy x1gryazu x1n2onr6"] a')

            elCount = len(locators)

            # connect to database
            directory_path = f"Databases/{self.search_title}"
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            self.conn = sqlite3.connect(f"Databases/{self.search_title}/marketplace_{self.query}.db")
            self.cursor = self.conn.cursor()

            database_exists = self.check_database_existence()
            new_entries = []
            send_mail = database_exists

            for index in range(elCount):
                element = locators[index]
                innerText = element.inner_text()
                href = element.get_attribute('href')
                URL = 'https://www.facebook.com/' + href

                # Extract price, title, and location information
                parts = innerText.split('\n')
                try:
                    if self.is_dollar_integer(parts[0]) and self.is_dollar_integer(parts[1]):
                        price = parts[0].strip()
                        title = parts[2].strip()
                        location = parts[3].strip()
                    else:

                        price = parts[0].strip()
                        title = parts[1].strip()
                        try:
                            location = parts[2].strip()
                        except:
                            print(f"location not found, URL: {'https://www.facebook.com/' + href}")
                except:
                    print(f"Weird string format: {parts}. URL: {URL}")

                # Open URL of specific item in a new page to get description
                distance = 0
                description = None
                img_URL = None
                item_info = [price, title, location, description, distance, URL, img_URL]

                if not database_exists:
                    self.create_database(search_URL)
                    database_exists = True

                if not self.check_listing_existence(item_info):
                    # getting distance data, only 2500 requests per day on api
                    try:
                        distance = round(self.check_distance(location))  # returns distance in miles
                    except:
                        distance = 0
                    # create list with updated item info
                    item_info = [price, title, location, description, distance, URL, img_URL]
                    self.insert_listing(item_info)

                    # send an email with URL if this is a new post
                    if send_mail and (distance < 100):
                        Send_Listing(self.email, title, URL, price, description, distance, self.query)
                        self.items_found += 1
                self.items_searched += 1
            # Close the browser
            page.close()
            self.browser.close()
            self.conn.close()