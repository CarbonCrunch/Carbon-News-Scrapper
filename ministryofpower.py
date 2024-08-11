import requests
from bs4 import BeautifulSoup
import csv
import os

def read_download_folder_path():
    with open('downloads_folder_path.txt', 'r') as file:
        download_folder_path = file.readline().strip()
    return download_folder_path

def scrape_site(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all table rows with class 'even' or 'odd'
    rows = soup.find_all('tr', class_=['even', 'odd'])
    
    pdf_details = []

    for row in rows:
        # Extract the title
        title = row.find('td', class_='views-field views-field-title-1').get_text(strip=True)
        
        # Extract the date
        date = row.find('td', class_='views-field views-field-field-date active').get_text(strip=True)
        
        # Extract the link
        link = row.find('a', class_='pdfIcon').get('href')
        
        pdf_details.append({'Title': title, 'Date': date, 'Link': link})
    
    return pdf_details

def save_to_csv(pdf_details, download_dir, filename):
    # Ensure the download_dir exists
    os.makedirs(download_dir, exist_ok=True)
    
    # Define the full file path
    file_path = os.path.join(download_dir, filename)
    
    # Define the CSV file header
    headers = ['Title', 'Date', 'Link']
    
    # Write data to CSV file
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for detail in pdf_details:
            writer.writerow(detail)

    return file_path

def main():
    # Example usage:
    url = 'https://powermin.gov.in/circular'  # Replace with your target URL
    pdf_details = scrape_site(url)

    download_dir = read_download_folder_path()
    csv_filename = 'ministryofpower.csv'

    # Save the details to a CSV file in the specified download_dir
    file_path = save_to_csv(pdf_details, download_dir, csv_filename)

    print(f'Ministry of power articles saved to {file_path}')


if __name__=="__main__":
    main()


