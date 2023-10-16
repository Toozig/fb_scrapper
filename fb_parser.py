import pandas as pd
import sys
from facebook_scraper import get_posts
import gspread
import os
# input vars index
ADDRESS_IDX = 1
SHEET_NAME_IDX = 2

#file which contains the parsed ur;s
URL_FILE = 'url_archive.txt'
#The google sheet name
SHEET_NAME = 'fb_comments'
#the work tab of the google sheet
SHEET_TAB_IDX = 0


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

def create_file_if_not_exists(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass
        print(f"File '{file_path}' did not exist. Created a new file.")


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




def parse_post(address):
    """
    address: link to the post
    parse a post  into a pd.series object
    """
    fields = ['username', 'post_url' , 'text','reaction_count', 'image', 'original_request_url']
    urls = ['post_url', 'original_request_url']
    
    # get the post data (note that coockies is not mandatory)
    post = pd.Series(list(get_posts(post_urls=[address]))[0]) # if not wokrign  , cookies='coockies.co' add thos yo get_posts
    if not pd.Series(fields).isin(post.index).all():
          return pd.Series(), pd.Series()
    
    # prepare the neccesery fields
    sub_post = post[fields]
    sub_post['date'] = post['time'].strftime("%d/%m/%y")

    # save the used url to avoid duplications
    urls_series = post[urls]
    urls_series['submitted_url'] = address
    
    return sub_post.fillna(''), urls_series.drop_duplicates()

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



def print_usage():
    print("Usage: python script_name.py [Facebook_Post_URL] ")
    print("Example: python your_script.py https://facebook.com/post/12345 ")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments.")
        print_usage()
        sys.exit(1)

    address = sys.argv[ADDRESS_IDX]

    if 'facebook' not in address.lower():
        print(f"The input should be a facebook post address")
        exit(1)
        
    if url_exist(address,URL_FILE):
        print(f"url '{address}' already parsed.")
        exit(1)
    try:
        post, urls = parse_post(address)
        if post.shape:
            update_sheet(df = pd.DataFrame(post).T, sheet_name=SHEET_NAME, work_sheet=SHEET_TAB_IDX)
            add_urls_to_archive(urls.tolist(), URL_FILE)
            print(f"Data from the Facebook post has been successfully added to the Google Sheet '{SHEET_NAME}'.")
        else:
            print("Could not get the post (private post? closed group?)")
    except Exception as e:
        print(f"Error: An error occurred. {str(e)}")
