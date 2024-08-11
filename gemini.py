import google.generativeai as genai
import os
import pandas as pd

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Read the CSV file
main_csv_path = "maincsv.csv"
google_csv_path="downloads/googlenews_articles.csv"
linkedin_csv_path="downloads/linkedin_posts.csv"
# df = pd.read_csv(main_csv_path)
# df = pd.read_csv(google_csv_path)
df = pd.read_csv(linkedin_csv_path)

# Extract data from the DataFrame
csv_content = df.to_csv(index=False)
# Format the instructions with the extracted data
instructions = [
    "Categorise each of the article in one of these. 1. New government notification, 2. A knowledge post. 3. Company Notification, 4. Other"
]

combined_input = f"{csv_content}\n\n{instructions}"

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content([combined_input])

with open("response.txt", "w") as file:
    file.write(response.text)
