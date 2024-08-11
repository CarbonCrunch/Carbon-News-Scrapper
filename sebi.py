import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def read_download_folder_path():
    with open('downloads_folder_path.txt', 'r') as file:
        download_folder_path = file.readline().strip()
    return download_folder_path

def set_dates_and_submit(url, start_date, end_date, download_dir, downloaded_filename):
    # Set up the WebDriver (assuming Chrome here)
    options = webdriver.ChromeOptions()
    
    driver = webdriver.Chrome(options=options)
    # Open the target URL
    driver.get(url)
    
    try:       
        # Wait until the start date input is present
        start_date_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'fromDate'))
        )
        
        # Set the start date
        start_date_element.clear()
        start_date_element.send_keys(start_date)
        
        # Wait until the end date input is present
        end_date_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'toDate'))
        )
        
        # Set the end date
        end_date_element.clear()
        end_date_element.send_keys(end_date)
        
        # Find the GO button and scroll into view
        go_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='go-search go_search' and contains(@href, 'searchFormNewsListAll')]"))
        )
        
        # Scroll to the GO button
        driver.execute_script("arguments[0].scrollIntoView(true);", go_button)
        time.sleep(1)  # Allow time for any animations or scrolling
        
        # Click the GO button using JavaScript
        driver.execute_script("arguments[0].click();", go_button)
        
        # Wait for the results table to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'sample_1'))
        )

        # Extract data from the table
        extract_data(driver, download_dir, downloaded_filename)

    finally:
        # Close the WebDriver
        driver.quit()

def extract_data(driver, download_dir, downloaded_filename):
    announcements = []
    while True:
        # Wait until the table is present
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'sample_1'))
        )
        
        # Find all rows in the table
        rows = table.find_elements(By.TAG_NAME, 'tr')
        
        for row in rows[1:]:  # Skip the header row
            cells = row.find_elements(By.TAG_NAME, 'td')
            date = cells[0].text
            subject = cells[2].text
            link = cells[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
            announcements.append({'date': date, 'subject': subject, 'link': link})
        
        # Check if there is a next page
        try:
            next_button = driver.find_element(By.XPATH, "//a[@title='Next']")
            if 'disabled' in next_button.get_attribute('class'):
                break
            else:
                next_button.click()
                time.sleep(2)  # Wait for the next page to load
        except:
            break

    save_to_csv(announcements, download_dir, downloaded_filename)

def save_to_csv(data, download_dir, downloaded_filename):
    # Ensure the output directory exists
    os.makedirs(download_dir, exist_ok=True)
    
    # Path to save the CSV file
    file_path = os.path.join(download_dir, downloaded_filename)
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'subject', 'link'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    
    print(f'SEBI articles saved to {file_path}')

def main():
    # Example usage
    url = 'https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListingAll=yes'  # Target URL
    start_date = '26-07-2024'  # Start date in DD-MM-YYYY format
    end_date = '30-07-2024'  # End date in DD-MM-YYYY format
    download_dir = read_download_folder_path()  # Desired output directory
    downloaded_filename = f"sebi_{start_date}_{end_date}.csv"  # Desired output filename
    set_dates_and_submit(url, start_date, end_date, download_dir, downloaded_filename)
    
if __name__=="__main__":
    main()
