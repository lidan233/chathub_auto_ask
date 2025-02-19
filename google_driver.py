from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os


import undetected_chromedriver as uc
import time
import json


def login_to_google(driver):
    try:
        google_button = driver.find_element(By.XPATH, '//button[.//span[text()="Google"]]')
        google_button.click()
        email_input = WebDriverWait(driver, 10, poll_frequency=0.5).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys("your@gmail.com")  # Replace with your actual Gmail
        time.sleep(1)  
        email_input.send_keys(Keys.ENTER)
        time.sleep(2) 
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="password" and @name="Passwd"]'))
        )
        password_input.send_keys("yourpassword")  # Replace with your actual password
        time.sleep(1)  # Short delay to mimic human behavior
        password_input.send_keys(Keys.ENTER)
        time.sleep(2) 
    except Exception as e:
        print(f"no need to login")

def send_problem(driver, problem_text):
    try:
        textarea = WebDriverWait(driver, 5, poll_frequency=0.5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'textarea[name="input"]'))
        )
        textarea.send_keys(problem_text)
        time.sleep(1) 
        textarea.send_keys(Keys.ENTER)
        time.sleep(1) 
        return True
    except Exception as e:
        return False

def get_outputs(driver):
    results = []
    try:
        output_elements = WebDriverWait(driver, 5, poll_frequency=0.5).until(
            EC.presence_of_all_elements_located((By.XPATH, 
                '//div[contains(@class, "w-fit") and contains(@class, "overflow-x-hidden") and contains(@class, "rounded-[15px]") and contains(@class, "px-4") and contains(@class, "py-2") and contains(@class, "bg-secondary") and contains(@class, "text-primary-text") and .//div[contains(@class, "markdown-body") and contains(@class, "markdown-custom-styles") and contains(@class, "!text-base") and contains(@class, "font-normal")]]'))
        )
        for output in output_elements:
            print("Output received:", output.text)
            results.append(output.text)
        return results
    except Exception as e:
        print(f"An error occurred while fetching outputs: {e}")
        return []


def extract_titles(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        # Assuming the JSON contains a list of items with "title" field
        titles = []
        for item in data:
            if 'title' in item:
                titles.append(item['title'])
                
        return titles
        
    except FileNotFoundError:
        print(f"File {json_file} not found")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON format in file {json_file}")
        return None

def save_list_to_txt(strings, file_name="outputs.txt", directory=None):
    """Save a list of strings to a text file."""
    try:
        # Determine the save path
        if directory is None:
            # Default to Downloads directory
            home = os.path.expanduser("~")
            directory = os.path.join(home, "Downloads")
        
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)
        
        # Create the full file path
        file_path = os.path.join(directory, file_name)
        
        # Write each string to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            for s in strings:
                f.write(s + "\n")
        
        print(f"List saved to: {file_path}")
        return True
        
    except Exception as e:
        print(f"An error occurred while saving the list: {e}")
        return False
    

def main():
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = uc.Chrome(options=options)
    driver.get("https://app.chathub.gg/")
    try:
        # Wait for the page to load
        login_to_google(driver)
        # send_problem(driver, "What is the capital of France?")
        # outputs = get_outputs(driver)

        for json_file in os.listdir("/media/lida/softwares/QE/inputs/"):
            json_files = os.path.join("/media/lida/softwares/QE/inputs/", json_file)
            output_file = os.path.join("/media/lida/softwares/QE/outputs/", json_file.replace(".json", "_output.txt"))

            if json_files == "/media/lida/softwares/QE/inputs/iclr2021.json":
                start = 1200 
            else:
                start = 0 
            titles = extract_titles(json_files)
            for i in range(start, len(titles), 100):
                this_titles = titles[i:i+100]
                prefix = "paper's title is " + ",'".join(this_titles) + ".'"
                suffix = "Please analyze the titles; if any are highly related to the field of 3D reconstruction or generation, output only those titles without any explanations."
                flag = send_problem(driver, prefix + suffix)
                if flag is True:
                    outputs = get_outputs(driver)
                    save_list_to_txt(outputs, output_file + "output.txt")
                    time.sleep(5) 
                else:
                    continue 
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()