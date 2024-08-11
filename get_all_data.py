import os
import csv
from datetime import datetime

def read_download_folder_path():
    with open('downloads_folder_path.txt', 'r') as file:
        download_folder_path = file.readline().strip()
    return download_folder_path

def insert_into_master_csv(file_name, row, encoding='utf-8'):
    # Check if the file exists
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"The file '{file_name}' does not exist.")
    
    # Read the existing rows from the file
    existing_rows = set()
    with open(file_name, mode='r', newline='', encoding=encoding) as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        for existing_row in reader:
            existing_rows.add(tuple(existing_row))  # Add existing rows as tuples to the set
    
    # Check if the row already exists
    if tuple(row) in existing_rows:
        # print(f"Row {row} already exists. Skipping insertion.")
        return
    
    # Open the file in append mode and write the new row
    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Writing the data
        writer.writerow(row)

def fetching_bse(download_dir):
    def convert_date(date_str):
        try:
            main_date_str = date_str.split('-')[0]
            main_date = datetime.strptime(main_date_str, '%Y%m%d')
            formatted_date = main_date.strftime('%d-%m-%Y')
            return formatted_date
        except ValueError as e:
            return f"Error: {e}"
    
    # List all files in the specified folder
    for filename in os.listdir(download_dir):
        # Check if the filename starts with 'bse' and ends with '.csv'
        if filename.startswith('bse') and filename.endswith('.csv'):
            # Construct the full file path
            file_path = os.path.join(download_dir, filename)
            
            with open(file_path, mode='r', encoding='ISO-8859-1') as file:
                csv_reader = csv.reader(file)
                i=1
                header = next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    date=convert_date(row[0])
                    source="BSE"
                    desc=row[1]
                    link=row[5].replace(":6443", "")
                    insert_into_master_csv('maincsv.csv',[date,source,desc,link],encoding='ISO-8859-1')

def fetching_ministry_of_power(download_dir):
    def fix_date(date_str):
        try:
            date_object = datetime.strptime(date_str, '%d/%m/%Y')
            formatted_date = date_object.strftime('%d-%m-%Y')
            return formatted_date
        except Exception as e:
            print(date_str)
            print(e)
    for filename in os.listdir(download_dir):
        if filename.startswith('ministryofpower') and filename.endswith('.csv'):
            file_path = os.path.join(download_dir, filename)
            
            with open(file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    date = fix_date(row[1])
                    source = "Ministry of Power"
                    desc = row[0]
                    link = row[2]
                    insert_into_master_csv('maincsv.csv', [date, source, desc, link])

def fetching_sebi(download_dir):
    def fix_date(date_str):
        try:
            date_object = datetime.strptime(date_str, '%b %d, %Y')
            formatted_date = date_object.strftime('%d-%m-%Y')
            return formatted_date
        except Exception as e:
            print(e)
            return

    for filename in os.listdir(download_dir):
        if filename.startswith('sebi') and filename.endswith('.csv'):
            file_path = os.path.join(download_dir, filename)
            
            with open(file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    date=fix_date(row[0])
                    source="SEBI"
                    desc=row[1]
                    link=row[2]
                    # print([date,desc,link])
                    insert_into_master_csv('maincsv.csv',[date,source,desc,link])

def fetching_nse(download_dir):
    def fix_date(date_str):
        try:
            date_object = datetime.strptime(date_str, '%B %d, %Y')
            formatted_date = date_object.strftime('%d-%m-%Y')
            return formatted_date
        except Exception as e:
            print(e)
            return

    for filename in os.listdir(download_dir):
        if filename.startswith('nse') and filename.endswith('.csv'):
            file_path = os.path.join(download_dir, filename)
            
            with open(file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    date=fix_date(row[0])
                    source="NSE"
                    desc=row[3]
                    link=row[4]
                    # print([date,desc,link])
                    insert_into_master_csv('maincsv.csv',[date,source,desc,link])


def main():
    # Define the folder path
    download_dir = read_download_folder_path()
    fetching_bse(download_dir)
    fetching_ministry_of_power(download_dir)
    fetching_sebi(download_dir)
    fetching_nse(download_dir)

if __name__=="__main__":
    main()
