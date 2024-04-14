from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

app = Flask(__name__)

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
spreadsheet_id = '1jokrByeScIw8K9XePl4ublTdfDrkSVq7kp-lPZyHGQA'
spreadsheet = client.open_by_key(spreadsheet_id)
sheet = spreadsheet.sheet1

@app.route('/')
def index():
    # Fetch data from Google Sheet
    data = pd.DataFrame(sheet.get_all_records())

    # Ensure there are enough columns
    if len(data.columns) < 7:
        return "Insufficient columns in the dataset."

    # Group data by the 3rd, 5th, and 7th columns and count occurrences
    grouping_results = []
    for col_index in [2, 4, 6]:  # Column indexes for 3rd, 5th, and 7th columns
        grouped_data = data.groupby(data.columns[col_index]).size().reset_index(name='counts')
        grouping_results.append((data.columns[col_index], grouped_data.to_html(classes='data', header="true")))

    # Convert the grouped data to HTML table for display
    return render_template('index.html', grouping_results=grouping_results)

if __name__ == '__main__':
    app.run(debug=True)
