from playwright.sync_api import sync_playwright

def get_description(search_url):
    with sync_playwright() as playwright:
        # Launch the browser and create a new page
        browser = playwright.chromium.launch()
        page = browser.new_page()

        # Navigate to the search page
        page.goto(search_url)
        current_url = page.url
        print(current_url)
        try:
            item_element = page.wait_for_selector(
                '[class="xz9dl7a x4uap5 xsag5q8 xkhd6sd x126k92a"]', timeout=2000)
            description = item_element.inner_text()
        # no description
        except:
            description = "No Description Data"

        # Close the browser and return the result
        browser.close()
        return description
    
print(get_description("https://www.facebook.com//marketplace/item/3561753297480231/?ref=search&referral_code=null&referral_story_type=post&__tn__=!%3AD"))