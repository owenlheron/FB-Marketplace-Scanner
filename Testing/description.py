from playwright.sync_api import sync_playwright, TimeoutError

with sync_playwright() as playwright:
    # Launch the browser and create a new page
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Navigate to the search page
    page.goto(
        f'https://www.facebook.com//marketplace/item/156147867282302/?ref=search&referral_code=null&referral_story_type=post')
    page.wait_for_selector('[aria-label="Collection of Marketplace items"]')

    # Find all the item links on the page
    locators = page.query_selector_all('[aria-label="Collection of Marketplace items"] a')
    elCount = len(locators)

    entries = []

    for index in range(elCount):
        element = locators[index]
        innerText = element.inner_text()
        href = element.get_attribute('href')
        print(innerText)