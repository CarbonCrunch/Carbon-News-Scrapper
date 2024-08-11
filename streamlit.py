import os
import pandas as pd
import streamlit as st

def read_download_folder_path():
    with open('downloads_folder_path.txt', 'r') as file:
        download_folder_path = file.readline().strip()
    return download_folder_path

def make_clickable(val):
    # Convert URLs into clickable links
    return f'<a href="{val}" target="_blank">{val}</a>'

def view_csv(csv_file_path):
    # Set the layout to wide to utilize the full width of the browser window
    st.set_page_config(layout="wide")

    # Custom CSS to center the content and set column sizes
    center_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .css-1d391kg {margin: 0 auto; max-width: 1000px;}
        table {
            table-layout: fixed;
            width: 100%;
        }
        th, td {
            word-wrap: break-word;
            overflow-wrap: break-word;
            white-space: pre-wrap;
            word-break: break-word;
            max-width: 200px;
        }
        </style>
        """
    st.markdown(center_streamlit_style, unsafe_allow_html=True)

    st.title("CSV File Viewer")

    # Check if the file exists
    if os.path.exists(csv_file_path):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path, encoding='utf-8')

        # Check for URL columns and make them clickable
        for col in df.columns:
            if df[col].str.contains('http').any():
                df[col] = df[col].apply(make_clickable)

        # Display the DataFrame in a table format with full width
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.error(f"The file '{csv_file_path}' does not exist.")

def view_linkedin():
    pass

if __name__ == "__main__":
    download_dir = read_download_folder_path()
    # filename = 'googlenews_articles.csv'
    # filename = 'linkedin_posts.csv'
    # filename = 'linkedin_posts.csv'
    # file_path = os.path.join(download_dir, filename)
    file_path='maincsv.csv'
    view_csv(file_path)
