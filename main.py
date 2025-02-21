from playwright.sync_api import sync_playwright, expect
import os
import json
import time

# --- Configuration (Replace with your actual values) ---
USER_EMAIL = "your_email@example.com"  # Replace with your email
USER_PASSWORD = "your_password"  # Replace with your password
INPUTS_DIR = "/path/to/your/inputs"  # Replace with your inputs directory
OUTPUTS_DIR = "/path/to/your/outputs"  # Replace with your outputs directory
CHATHUB_URL = "https://app.chathub.gg/"
# -------------------------------------------------------

def login_to_google(page, email=USER_EMAIL, password=USER_PASSWORD):
    try:
        # Wait for and click the Google login button
        page.locator('//button[.//span[contains(text(), "Google")]]').click()

        # Wait for the email input, fill it, and click the next button
        page.wait_for_selector('input[type="email"]')
        page.type('input[type="email"]', email)
        page.click("#identifierNext")

        # Wait for the password input, fill it, and click the next button
        page.wait_for_selector('input[type="password"]')
        page.type('input[type="password"]', password)
        page.wait_for_selector("#passwordNext")
        page.click("#passwordNext")

        # Click a link (assuming this is part of the login flow, adjust as needed)
        page.locator('div.flex.shrink-0.flex-row.items-center.gap-2 a:nth-child(2)').click()

    except Exception as e:
        print(f"Login may not be needed or failed: {e}")


def click_all_stop_svgs_by_class(page):
    try:
        # Use a more robust selector (consider using data-testid if available)
        svg_selector = "svg.text-primary-text.bg-primary-background.absolute.bottom-1\\.5.right-2\\.5.cursor-pointer"
        svg_locator = page.locator(svg_selector)
        count = svg_locator.count()
        print(f"Found {count} matching SVG buttons")

        for i in range(count):
            try:
                svg = svg_locator.nth(i)
                svg.click()
                print(f"Successfully clicked SVG {i+1}")
            except Exception as e:
                print(f"Error clicking SVG {i+1}: {e}")

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def send_problem(page, problem_text):
    try:
        locator = page.locator('textarea[name="input"]')
        expect(locator).to_be_editable(timeout=10000)
        locator.fill(problem_text)
        page.keyboard.press("Enter")
        page.wait_for_load_state("networkidle")
        count = 0
        while check_spinner_spinner(page):
            count += 1
            time.sleep(1)
            if count > 5:
                try:
                    click_all_stop_svgs_by_class(page)
                except Exception as e:
                    print(f"Error clicking all stop svgs: {e}")
            if count > 10:
                page.reload()
                print("Page reloaded")

        page.wait_for_load_state('domcontentloaded')
        return True
    except Exception as e:
        print(f"Error sending problem: {e}")
        return False


def get_outputs(page):
    results = []
    try:
        # More robust selector using data-testid if available, otherwise use a combination of classes
        output_selector = 'div[data-testid^="output-"] > div.markdown-body, div.w-fit.overflow-x-hidden.rounded-\\[15px\\].px-4.py-2.bg-secondary.text-primary-text > div.markdown-body'
        page.locator(output_selector).first.wait_for(timeout=10000)
        output_elements = page.locator(output_selector).all()
        for output in output_elements:
            results.append(output.inner_text())
        return results
    except Exception as e:
        print(f"An error occurred while fetching outputs: {e}")
        return []


def extract_titles(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return [item['title'] for item in data if 'title' in item]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file: {e}")
        return []


def save_list_to_txt(strings, file_name, directory):  # Removed default directory
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file_name)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:  # Changed to 'w' mode
            for s in strings:
                f.write(s + "\n")
        print(f"List saved to: {file_path}")
        return True
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False


def check_spinner_spinner(page):
    selector = "span.leading-tight > span"  # Could be improved with data-testid
    spinner_elements = page.locator(selector)
    return spinner_elements.count() > 0


def handle_fetch_error(page):
    try:
        error_text = "Failed to fetch"
        if page.get_by_text(error_text, exact=False).is_visible(timeout=5000):
            print("Detected 'Failed to fetch' error. Reloading...")
            page.reload()
            page.wait_for_timeout(10000)
            print("Wait complete. Continuing...")
            return True
    except TimeoutError:
        print("Failed to fetch error not found (timeout).")
        return False
    except Exception as e:
        print(f"An error occurred while handling the error: {e}")
        return False



def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled'])
        page = browser.new_page()
        page.goto(CHATHUB_URL)

        try:
            login_to_google(page)

            for json_file in os.listdir(INPUTS_DIR):
                if not json_file.endswith(".json"):
                    continue

                json_file_path = os.path.join(INPUTS_DIR, json_file)
                output_file_path = os.path.join(OUTPUTS_DIR, json_file.replace(".json", "_output.txt"))
                if os.path.exists(output_file_path):
                    print(f"Skipping {json_file} (output file already exists)")
                    continue

                titles = extract_titles(json_file_path)
                if not titles:
                    print(f"Skipping {json_file} (no titles found)")
                    continue

                # Removed the condition to skip specific files (you can add it back if needed)

                for i in range(0, len(titles), 300):
                    batch_titles = titles[i:i + 300]
                    prompt = (
                        "paper's title is '" + "','".join(batch_titles) +
                        "'.Please analyze the titles; if any are highly related to single-view 3D "
                        "reconstruction or generation, output only those titles without any explanations."
                    )

                    if send_problem(page, prompt):
                        outputs = get_outputs(page)
                        if handle_fetch_error(page):  # Check and handle the error *after* getting outputs
                            outputs = get_outputs(page)  # Try to get outputs again after reload
                        if outputs:
                            save_list_to_txt(outputs, os.path.basename(output_file_path), OUTPUTS_DIR)
                    else: #added else statement
                        page.reload()
                        page.wait_for_timeout(10000)
                        if send_problem(page, prompt): #added if statement
                            outputs = get_outputs(page)
                            if handle_fetch_error(page):
                                outputs = get_outputs(page)
                            if outputs:
                                save_list_to_txt(outputs, os.path.basename(output_file_path), OUTPUTS_DIR)

                page.reload()
                page.wait_for_timeout(10000)
        finally:
            browser.close()
            print("Browser closed.")

if __name__ == "__main__":
    main()