from playwright.sync_api import sync_playwright

def get_images(search_url):
    with sync_playwright() as playwright:
        # Launch the browser and create a new page
        browser = playwright.chromium.launch()
        page = browser.new_page()

        # Navigate to the search page
        page.goto(search_url)

        # Extract the description text
        try:
            # multiple photos
            element = page.wait_for_selector(
                '[class="x6s0dn4 x78zum5 x193iq5w x1y1aw1k xwib8y2 xu6gjpd x11xpdln x1r7x56h xuxw1ft xc9qbxq"]',
                timeout=1000)
        except:
            # only one photo
            element = page.wait_for_selector(
                '[class="x6s0dn4 x78zum5 x1iyjqo2 xl56j7k x6ikm8r x10wlt62 xh8yej3 x1ja2u2z"]',
                timeout=1000)

        # Extract the images
        #photo_descriptor = '[alt="Product photo of Honda EU2200 Generator"]'
        photo_descriptor = 'img'
        image_elements = element.query_selector_all(photo_descriptor)
        image_urls = [element.get_attribute('src') for element in image_elements]

        # Close the browser and return the result
        browser.close()
        return image_urls

#print(get_images("https://www.facebook.com//marketplace/item/647877927223903/?ref=search&referral_code=null&referral_story_type=post&__tn__=!%3AD"))
