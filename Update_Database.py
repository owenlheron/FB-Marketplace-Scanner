import sqlite3
import json
from playwright.sync_api import sync_playwright

def check_listing_existence(URL):
    with sync_playwright() as playwright:
        # Launch the browser and create a new page
        browser = playwright.chromium.launch()
        page = browser.new_page()

        try:
            page.goto(URL)
        except:
            print("Cannot access URL")
            return

        # Get the URL of the current page
        current_url = page.url

        if same_listing(current_url, URL):
            browser.close()
            return True
        else:
            browser.close()
            return False

def ask_login(scanner):
    title = scanner.search_title
    item = scanner.query

    # Connect to the SQLite database
    conn = sqlite3.connect(f"Databases/{title}/marketplace_{item}.db")
    c = conn.cursor()

    # Retrieve all rows from the table
    c.execute("SELECT * FROM listings")
    rows = c.fetchall()

    URL = rows[1][6]

    # login request: https://www.facebook.com/login/?next=https%3A%2F%2Fwww.facebook.com%2Fmarketplace%2Fitem%2F994686051558164%2F%3Fref%3Dsearch%26referral_code%3Dnull%26referral_story_type%3Dpost%26__tn__%3D%2521%253AD
    login_url = "https://www.facebook.com/login"
    with sync_playwright() as playwright:
        # Launch the browser and create a new page
        browser = playwright.chromium.launch()
        page = browser.new_page()

        #go to url
        try:
            page.goto(URL)
        except:
            print("Cannot access URL")
            return

        directed_URL = page.url
        if login_url in directed_URL:
            browser.close()
            conn.close()
            return True
        else:
            browser.close()
            conn.close()
            return False

def listing_unavailable(directed_URL):
    # unavailable product: https://www.facebook.com/marketplace/109407409079108/?unavailable_product=1
    unavailable_url = "unavailable_product=1"
    if unavailable_url in directed_URL:
        return True
    else:
        return False



def same_listing(directed_URL, listing_URL):
    # Compare strings and determine if they are the same or the listing has been deleted
    if directed_URL in listing_URL:
        return True
    else:
        return False

def get_description(search_url):
    with sync_playwright() as playwright:
        # Launch the browser and create a new page
        browser = playwright.chromium.launch()
        page = browser.new_page()

        # Navigate to the search page
        page.goto(search_url)
        current_url = page.url
        #check if item is still available
        unavailable = listing_unavailable(current_url)
        if unavailable == True:
            return "Listing does not exist"

        try:
            item_element = page.wait_for_selector(
                '[class="xz9dl7a x4uap5 xsag5q8 xkhd6sd x126k92a"]', timeout=2000)
            description = item_element.inner_text()
        # no description
        except:
            # TODO: determine if timeout error due to not finding item or determine if there is no desceription
            print(f"No descrption data: {search_url}")
            description = "No Description Data"

        # Close the browser and return the result
        browser.close()
        return description

def get_images(search_url):
    with sync_playwright() as playwright:
        # Launch the browser and create a new page
        browser = playwright.chromium.launch()
        page = browser.new_page()

        # Navigate to the search page
        page.goto(search_url)
        current_url = page.url
        #check if item is still available
        unavailable = listing_unavailable(current_url)
        if unavailable == True:
            return "Listing does not exist"

        # Extract the description text
        try:
            # multiple photos
            element = page.wait_for_selector(
                '[class="x6s0dn4 x78zum5 x193iq5w x1y1aw1k xwib8y2 xu6gjpd x11xpdln x1r7x56h xuxw1ft xc9qbxq"]',
                timeout=2000)
        except:
            # only one photo
            element = page.wait_for_selector(
                '[class="x6s0dn4 x78zum5 x1iyjqo2 xl56j7k x6ikm8r x10wlt62 xh8yej3 x1ja2u2z"]',
                timeout=2000)

        # Extract the images
        #photo_descriptor = '[alt="Product photo of Honda EU2200 Generator"]'
        photo_descriptor = 'img'
        image_elements = element.query_selector_all(photo_descriptor)
        image_urls = [element.get_attribute('src') for element in image_elements]

        # Close the browser and return the result
        browser.close()
        return image_urls

#print(get_description("https://www.facebook.com//marketplace/item/190268330666375/?ref=search&referral_code=null&referral_story_type=post&__tn__=!%3AD"))
#print(get_images("https://www.facebook.com//marketplace/item/647877927223903/?ref=search&referral_code=null&referral_story_type=post&__tn__=!%3AD"))

def update_database(scanner):
    title = scanner.search_title
    item = scanner.query

    # Connect to the SQLite database
    conn = sqlite3.connect(f"Databases/{title}/marketplace_{item}.db")
    c = conn.cursor()

    # Retrieve all rows from the table
    c.execute("SELECT * FROM listings")
    rows = c.fetchall()

    # Iterate through each row
    for row in rows:
        row_id = row[0]
        if row_id > 1:
            URL = row[6]
            #print(f"updating: {URL}")
            if (row[4] is None) or (row[4] == "None") or (row[4] == "Listing does not exists"):
                description = get_description(URL)
                if description == "Listing does not exist":
                    # TODO Delete the row if the listing no longer exists
                    print(f"Listing no longer exists: {URL}")
                    # c.execute("DELETE FROM listings WHERE id = ?", (row_id,))
                    # conn.commit()
                else:
                    c.execute("UPDATE listings SET description = ? WHERE id = ?", (description, row_id))
                    conn.commit()
            if (row[7] is None) or (row[7] == "Listing does not exists"):
                image_url = get_images(URL)
                if image_url == "Listing does not exist":
                    # TODO Delete the row if the listing no longer exists
                    print(f"Listing no longer exists: {URL}")
                    # c.execute("DELETE FROM listings WHERE id = ?", (row_id,))
                    # conn.commit()
                else:
                    image_urls_json = json.dumps(image_url)  # Serialize the list to a JSON string
                    c.execute("UPDATE listings SET img = ? WHERE id = ?", (image_urls_json, row_id))
                    conn.commit()

    # Commit the changes to the database

    # Close the database connection
    conn.close()

# convert seconds to good string
def convert_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60

    hours = int(round(hours))
    minutes = int(round(minutes))
    seconds = int(round(seconds))

    time_string = ""
    if hours > 0:
        time_string += f"{hours} hours, "
    if minutes > 0:
        time_string += f"{minutes} minutes, "
    if seconds > 0 or (hours == 0 and minutes == 0):
        time_string += f"{seconds} seconds"

    return time_string.rstrip(", ")

