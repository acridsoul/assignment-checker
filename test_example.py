from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    # Launch the browser
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://elearning.mku.ac.ke/")
    
    # Open the popup
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name=" Day, Evening & Weekend").click()
    page1 = page1_info.value

    # Login
    page1.get_by_placeholder("User").fill("xxxx")  # Replace with your username
    page1.get_by_placeholder("Password").fill("xxxxxx")  # Replace with your password
    page1.get_by_role("button", name="Log In").click()

    # Define a list of links to visit and take screenshots
    links_to_visit = [
        ("/25 Sep/Dec (Thika Day) BIT4103 Human Computer Interaction", "HCI"),
        ("/25 Sep/Dec (Thika Day) ABCU001 Research Methodology", "Research_Methodology"),
        ("/25 Sep/Dec (Thika Day) BIT3107 Database systems II", "Database_Systems"),
    ]

    screenshot_index = 1

    for link_name, file_prefix in links_to_visit:
        # Click the course link
        page1.get_by_role("link", name=link_name).click()

        # Click on "Tests & Quizzes"
        page1.get_by_role("link", name=" Tests & Quizzes").click()

        # Wait for the content to load
        page1.wait_for_load_state("networkidle")  # Wait for network to be idle
        page1.screenshot(path=f"{screenshot_index}_{file_prefix}.png", full_page=True)
        screenshot_index += 1

        # Return to the main page or previous state if needed
        page1.go_back()  # Navigate back

    # Close browser
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
