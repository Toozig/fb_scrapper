import pandas as pd
import sys
from facebook_scraper import get_posts
import gspread
import os
from parse_function import *

# input vars index
ADDRESS_IDX = 1


#file which contains the parsed ur;s
URL_FILE = 'fb_url_archive.txt'
#The google sheet name
SHEET_NAME = 'fb_comments'
#the work tab of the google sheet
SHEET_TAB_IDX = 0


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



def print_usage():
    print("Usage: python fb_parser.py [Facebook_Post_URL] ")
    print("Example: python fb_parser.py https://facebook.com/post/12345 ")

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
        print(post)
        if post.shape[0] > 0:
            update_sheet(df = pd.DataFrame(post).T, sheet_name=SHEET_NAME, work_sheet=SHEET_TAB_IDX)
            add_urls_to_archive(urls.tolist(), URL_FILE)
            print(f"Data from the Facebook post has been successfully added to the Google Sheet '{SHEET_NAME}'.")
        else:
            add_urls_to_archive([address],URL_FILE)
            print("Could not get the post (private post? closed group?)")
    except Exception as e:
        print(f"Error: An error occurred. {str(e)}")
