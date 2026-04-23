import gspread
import pandas as pd
import os
import json

def update_google_sheet(input_file: str, start_date: str, end_date: str):
    if not os.path.exists(input_file):
        print(f"File {input_file} does not exist.")
        return
    
    try:
        with open(input_file, 'r') as file:
            user_input = json.load(file)
            csv_file = user_input.get("csv_file")
            sheet_id = user_input.get("sheet_id")
            credentials_file = user_input.get("credentials_file")
            if not csv_file or not sheet_id or not credentials_file:
                print("CSV file path, sheet ID, and credentials file must be provided in the JSON input.")
                return
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {input_file}.")
        return
    
    # Load the CSV data
    try:
        df = pd.read_csv(csv_file)
        df = df.fillna('')  # Replace NaN with empty string for better compatibility with Google Sheets
        data = [df.columns.values.tolist()] + df.values.tolist()  # Convert DataFrame to list of lists
    except Exception as e:
        print(f"Error reading CSV file {csv_file}: {e}")
        return
    
    # Load Google Sheets credentials and update the sheet
    try:
        gc = gspread.service_account(filename=credentials_file)
        workbook = gc.open_by_key(sheet_id)
        worksheets = workbook.worksheets()
        worksheet_titles = [ws.title for ws in worksheets]
        sheet_name = f"Data_{start_date[:8]}_to_{end_date[:8]}"

        if sheet_name in worksheet_titles:
            worksheet = workbook.worksheet(sheet_name)
        else:
            worksheet = workbook.add_worksheet(title=sheet_name, rows=len(data), cols=len(data[0]) if data else 0)
        
        worksheet.clear()  # Clear existing content
        worksheet.update('A1', data)  # type: ignore # Update with new data starting from cell A1
        print("Google Sheet updated successfully.")
    except Exception as e:
        print(f"Error updating Google Sheet: {e}")