from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import pandas as pd
import time

# Function to setup WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    service = Service("path/to/chromedriver")  # Replace with your chromedriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to login to LinkedIn
def linkedin_login(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

# Function to scrape data from search results
def scrape_profiles(driver):
    profiles = []
    # Navigate to search results (e.g., "IIT graduates")
    driver.get("https://www.linkedin.com/search/results/people/?keywords=IIT%20graduates")
    time.sleep(3)

    # Loop through multiple pages
    for page in range(1, 6):  # Adjust page range as needed
        time.sleep(2)
        # Scrape profile details
        profiles_section = driver.find_elements(By.CLASS_NAME, "reusable-search__result-container")
        for profile in profiles_section:
            try:
                name = profile.find_element(By.CSS_SELECTOR, ".entity-result__title-text").text
                job_title = profile.find_element(By.CSS_SELECTOR, ".entity-result__primary-subtitle").text
                company = profile.find_element(By.CSS_SELECTOR, ".entity-result__secondary-subtitle").text
                profiles.append({"Name": name, "Job Title": job_title, "Company": company})
            except NoSuchElementException:
                continue

        # Navigate to next page
        try:
            next_button = driver.find_element(By.XPATH, "//button[@aria-label='Next']")
            next_button.click()
        except NoSuchElementException:
            print("No more pages.")
            break

    return profiles

# Main function
def main():
    # Replace with your LinkedIn credentials
    username = "your_email@example.com"
    password = "your_password"
    
    driver = setup_driver()
    try:
        linkedin_login(driver, username, password)
        profiles = scrape_profiles(driver)
        # Save data to CSV
        df = pd.DataFrame(profiles)
        df.to_csv("linkedin_profiles.csv", index=False)
        print("Data saved to linkedin_profiles.csv")
    except WebDriverException as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
