from get_arxiv_data import get_arxiv_data
from update_google_sheet import update_google_sheet
import pandas as pd
import datetime
import json
import os

def get_date_string(date: datetime.datetime) -> str:
    return date.strftime("%Y%m%d000000")

if __name__ == "__main__":
    now = datetime.datetime.now()
    startdate = get_date_string(now - datetime.timedelta(days=7))
    enddate = get_date_string(now)

    catagories = ["hep-ph", "hep-ex"]  # Example category, you can change it to any valid arXiv category

    # Loop through the categories and get data for each category. Merge the data into a single DataFrame if needed.
    dfs = []
    for category in catagories:
        print(f"Retrieving data for category {category} from {startdate} to {enddate}...")
        df = get_arxiv_data(category, startdate, enddate)
        print(f"Data for category {category} retrieved successfully.")
        dfs.append(df)
    merged_df = pd.concat(dfs, ignore_index=True)

    # Load the csv file name from the JSON input file
    input_file = "user_input.json"  # You can change this to the path of your JSON input file
    if not os.path.exists(input_file):
        print(f"File {input_file} does not exist.")
    else:
        try:
            with open(input_file, 'r') as file:
                user_input = json.load(file)
                csv_file = user_input.get("csv_file")
                if not csv_file:
                    print("CSV file path must be provided in the JSON input.")
                else:
                    merged_df.to_csv(csv_file, index=False)
                    print(f"Merged data saved to '{csv_file}'")
                    update_google_sheet(input_file, startdate, enddate)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {input_file}.")