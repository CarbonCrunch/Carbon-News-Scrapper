import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
import os

def read_download_folder_path():
    with open('downloads_folder_path.txt', 'r') as file:
        download_folder_path = file.readline().strip()
    return download_folder_path

def construct_google_news_url(keywords, days=1, hl='en-IN', gl='IN', ceid='IN:en'):
    search_query = '%7C'.join(keywords).replace(' ', '%20')
    search_url = f'https://news.google.com/search?q={search_query}%20when%3A{days}d&hl={hl}&gl={gl}&ceid={ceid}'
    print(search_url)
    return search_url

def extract_articles(keywords):
    search_url = construct_google_news_url(keywords)
    # print(search_url)
    response = requests.get(search_url)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = []
    for c_wiz in soup.find_all('c-wiz', {'class': 'PO9Zff Ccj79 kUVvS'}):
        article = {}
        header = c_wiz.find('article', {'class': 'IFHyqb DeXSAc'})
        if header:
            # Extract the time
            time_tag = header.find('time')
            if time_tag:
                article['time'] = time_tag.get_text()

            # Extract the source
            source_tag = header.find('div', {'class': 'vr1PYe'})
            if source_tag:
                article['source'] = source_tag.get_text()

            # Extract the title
            title_tag = header.find('div', {'class': 'IL9Cne'})
            if title_tag:
                article['title'] = title_tag.get_text().replace(f"{article['source']}More",'')

            # Extract the link
            link_tag = header.find('a', {'class': 'JtKRv'})
            if link_tag:
                article['link'] = link_tag['href'].replace('.', 'https://news.google.com', 1)

            articles.append(article)
    return articles

def save_to_csv(articles,download_dir,downloaded_filename):
    all_articles=[]
    all_articles.extend(articles)
    
    file_path = os.path.join(download_dir, downloaded_filename)
    # Save to a CSV file
    if all_articles:
        df = pd.DataFrame(all_articles)
        df.to_csv(file_path, index=False)
        print(f'Google news articles saved to {file_path}')
    else:
        print('No google news articles found.')

# Main function
def main():
    keywords = ['brsr', 'esg','carbon credits','environment']  # Replace with the actual keywords
    download_dir = read_download_folder_path()  # Desired output directory
    downloaded_filename = f"googlenews_articles.csv"  # Desired output filename

    # extract_articles(keywords,download_dir,downloaded_filename)
    articles=extract_articles(keywords)
    save_to_csv(articles,download_dir,downloaded_filename)

if __name__ == '__main__':
    main()

