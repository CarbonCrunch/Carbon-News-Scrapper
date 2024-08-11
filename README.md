# Web Scrapper
Scrape articles from BSE, NSE, SEBI, Ministry of Power, linkedIn and Google News.

## Points to remember before installation
- Replace the text in downloads_folder_path.txt with the folder you want to download in.

- You can add you linkedin credentials in 'linkedin_credentials.txt'

- You can change the start date and end date in bseindia.py and sebi.py.

- You can change keywords in linkedin.py and google_news.py

- get_all_data.py funtion combines the data from nse, bse, sebi and ministry of power in a single csv names as main csv

- Data from linkedin.py and google_news.py is saved in downloads folder.



## Installation
- ### Create a virtual environment(for mac):
```sh
python -m venv .venv
source .venv/bin/activate
```
- ### Install libraries:
```sh
pip install -r requirements.txt
```
- ### Run python program
```sh
python main.py
```

