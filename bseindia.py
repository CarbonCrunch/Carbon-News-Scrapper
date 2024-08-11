import time
import os
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def read_download_folder_path():
    with open('downloads_folder_path.txt', 'r') as file:
        download_folder_path = file.readline().strip()
    return download_folder_path

def scrape(url, start_date, end_date, download_dir):
    # Set up the WebDriver (assuming Chrome here)
    options = webdriver.ChromeOptions()
    
    # Set the download directory
    prefs = {'download.default_directory': download_dir}
    options.add_experimental_option('prefs', prefs)
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Open the target URL
        driver.get(url)
        
        # Wait until the start date input is present
        start_date_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_txtDate'))
        )
        
        # Change the value of the start date input field
        driver.execute_script("arguments[0].value = arguments[1];", start_date_element, start_date)
        
        # Wait until the end date input is present
        end_date_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_txtTodate'))
        )
        
        # Change the value of the end date input field
        driver.execute_script("arguments[0].value = arguments[1];", end_date_element, end_date)
        
        # Wait until the submit button is present and clickable
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'ContentPlaceHolder1_btnSubmit'))
        )
        
        # Click the submit button
        submit_button.click()
        
        # Wait for the page to load after submission
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_lnkDownload'))
        )
        
        # Wait until the download link is clickable
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'ContentPlaceHolder1_lnkDownload'))
        )
        
        # Click the download link
        download_link.click()
        
        # Wait for the download to complete
        time.sleep(3)

    finally:
        # Close the WebDriver
        driver.quit()

def rename_csv(download_dir,start_date,end_date):
    old_file_name = glob.glob(os.path.join(download_dir, 'Notices & Circulars*'))[0]
    start_date_formatted = start_date.replace('/', '-')
    end_date_formatted = end_date.replace('/', '-')
    
    # Generate the new file name
    new_file_name = f"bse_{start_date_formatted}_{end_date_formatted}.csv"
    
    # Rename the file
    os.rename(old_file_name, os.path.join(download_dir, new_file_name))
    new_file_path=os.path.join(download_dir,new_file_name)
    print(f"BSE articles saved to {new_file_path}")

def main():
    # Example usage:
    url = 'https://www.bseindia.com/markets/MarketInfo/NoticesCirculars.aspx?id=0'  # Replace with your target URL
    start_date = '23/07/2024'
    end_date = '30/07/2024'
    download_dir = read_download_folder_path()

    scrape(url, start_date, end_date, download_dir)
    rename_csv(download_dir, start_date, end_date)


if __name__ == "__main__":
    main()