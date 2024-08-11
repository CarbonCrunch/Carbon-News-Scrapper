from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
import csv
import os

def read_download_folder_path():
    with open('downloads_folder_path.txt', 'r') as file:
        download_folder_path = file.readline().strip()
    return download_folder_path

# Function to read credentials from a file
def read_credentials(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
    return username, password

# Function to log in and save cookies
def login_and_save_cookies(cookies_file):
    # Read credentials from the file
    username, password = read_credentials('linkedin_credentials.txt')

    # Initialize the Chrome driver
    driver = webdriver.Chrome()

    wait= WebDriverWait(driver, 10)
    login_url = 'https://www.linkedin.com/login'    
    driver.get(login_url)

    username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    username_field.send_keys(username)
    password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    password_field.send_keys(password)
    
    # Submit the login form
    login_button = driver.find_element(By.XPATH, '//*[@type="submit"]')
    login_button.click()
    
    # Wait for the login process to complete
    wait.until(EC.presence_of_element_located((By.ID, 'global-nav')))
    
    # Save cookies
    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)
    
    print("Cookies saved successfully.")
    driver.quit()

# Function to load cookies
def load_cookies(driver, cookies_file):
    driver.get("https://www.linkedin.com")
    with open(cookies_file, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    print("Cookies loaded successfully.")

# Function to scrape posts
def scrape(driver, min_posts=10):
    posts_data = []
    wait = WebDriverWait(driver, 10)

    while len(posts_data) < min_posts:
        # Wait for the posts to be loaded in the container
        post_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.occludable-update')))

        for post_element in post_elements:
            if len(posts_data) >= min_posts:
                break
            try:
                # Extracting post details
                author_element = post_element.find_element(By.CSS_SELECTOR, 'span.update-components-actor__name')
                author = author_element.text if author_element else 'N/A'

                description_element = post_element.find_element(By.CSS_SELECTOR, 'div.feed-shared-update-v2__description')
                description = description_element.text if description_element else 'N/A'
                
                # Extracting all image URLs if present
                image_urls = []
                try:
                    image_elements = post_element.find_elements(By.CSS_SELECTOR, 'div.update-components-image img')
                    for img in image_elements:
                        image_urls.append(img.get_attribute('src'))
                except:
                    image_urls = []

                # Storing post data
                post_data = {
                    'author': author,
                    'description': description,
                    'image_urls': image_urls
                }
                # Ensure no duplicates
                if post_data not in posts_data:
                    posts_data.append(post_data)
                
            except Exception as e:
                print(f"Error extracting data from a post: {e}")
                continue

        # Scroll down to load more posts
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adding a delay to ensure posts are loaded

    return posts_data


# Function to save posts to CSV
def save_to_csv(data, output_dir, output_filename):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Path to save the CSV file
    file_path = os.path.join(output_dir, output_filename)
    
    # Using a set to track unique entries
    seen = set()
    unique_data = []
    
    for row in data:
        # Convert the list of image URLs to a tuple for hashing
        row_tuple = (row['author'], row['description'], tuple(row['image_urls']))
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique_data.append(row)
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['author', 'description', 'image_urls'])
        writer.writeheader()
        for row in unique_data:
            # Convert the list of image URLs to a string for CSV output
            row['image_urls'] = '; '.join(row['image_urls'])
            writer.writerow(row)
    
    print(f'CSV file saved to {file_path}')

def main(login_first_time=False):
    cookies_file = 'linkedin_cookies.pkl'

    # UNCOMMENT THIS THE FIRST TIME YOU RUN THIS PROGRAM, THEN COMMENT IT OUT AGAIN 
    if(login_first_time):
        login_and_save_cookies(cookies_file)

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    # Load cookies and navigate to LinkedIn
    load_cookies(driver, cookies_file)
    keyword = 'brsr'
    driver.get(f"https://www.linkedin.com/search/results/content/?keywords={keyword}&origin=FACETED_SEARCH&sid=YD%3A&sortBy=%22date_posted%22")
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.search-results-container')))  # Wait for the page to load

    # Scrape the posts
    posts = scrape(driver, min_posts=10)
    driver.quit()

    # Save the posts to a CSV file
    output_dir = read_download_folder_path()  # Desired output directory
    output_filename = 'linkedin_posts.csv'  # Desired output filename
    save_to_csv(posts, output_dir, output_filename)

if __name__ == "__main__":
    main()
