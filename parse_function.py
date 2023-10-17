import pandas as pd
import gspread
import os


def add_urls_to_archive(strings_list, file_path):
    create_file_if_not_exists(file_path)

    try:
        # Read existing lines from the ordered file
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        # Append new strings to the lines
        lines += strings_list

        # Sort the lines
        lines.sort()

        # Convert the sorted lines to a pandas Series
        sorted_series = pd.Series(lines)

        # Write the Series to the file
        sorted_series.to_csv(file_path, header=False, index=False, mode='w')

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")



def create_file_if_not_exists(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass
        print(f"File '{file_path}' did not exist. Created a new file.")


def url_exist(input_string, file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            left, right = 0, len(lines) - 1

            while left <= right:
                mid = (left + right) // 2
                line = lines[mid].strip()
                
                if input_string == line:
                    return True
                elif input_string < line:
                    right = mid - 1
                else:
                    left = mid + 1

        return False
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return False


def update_sheet_row(data_list,sheet_name, col_names=[], work_sheet=0):
        """
        sheet: the gspread worksheet object to be updated
        df :  pd DataFrame with the new data
        col_names : (bool) add the columns names
        work_sheet : which tab to update (index/str)
        """
        gc = gspread.oauth()
        sh = gc.open(sheet_name)
        page = sh.get_worksheet(work_sheet)
        if len(col_names):
                page.append_row(col_names)
        page.append_row(data_list)

def update_sheet(df,sheet_name, col_names=False, reset_index=False, work_sheet=0):
        """
        sheet: the gspread worksheet object to be updated
        df :  pd DataFrame with the new data
        col_names : (bool) add the columns names
        work_sheet : which tab to update (index/str)
        """
        gc = gspread.oauth()
        sh = gc.open(sheet_name)
        page = sh.get_worksheet(work_sheet)
        data = df if not reset_index else df.reset_index()
        data = [data.columns.values.tolist()] + data.values.tolist() if col_names else data.values.tolist()[0]
        page.append_row(data)
