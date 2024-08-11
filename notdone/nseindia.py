import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil

def read_download_folder_path():
    with open('downloads_folder_path.txt', 'r') as file:
        download_folder_path = file.readline().strip()
    return download_folder_path

def download_csv(url, download_dir):
    # Set up the WebDriver (assuming Chrome here)
    options = webdriver.ChromeOptions()
    
    # Set the download directory
    prefs = {'download.default_directory': download_dir}
    options.add_experimental_option('prefs', prefs)
    
    # Clear cookies
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Open the target URL
        driver.get('https://www.nseindia.com/resources/exchange-communication-circulars')
        driver.get(url)
        
        # Wait until the download link is present
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, 'downloadCSV')]"))
        )
        
        time.sleep(2)
        # Click the download link
        download_link.click()

        # Downloading time
        time.sleep(5)

    finally:
        # Close the WebDriver
        driver.quit()


# Example usage:
url = 'https://www.nseindia.com/resources/exchange-communication-circulars'  # Replace with your target URL
download_dir = read_download_folder_path()  # Desired output directorydownload directory

download_csv(url, download_dir)
# print(f'CSV file should be downloaded to {download_dir}')