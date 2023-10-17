import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from parse_function import *
import sys

# input vars index
ADDRESS_IDX = 1


#file which contains the parsed ur;s
URL_FILE = 'ynet_url_archive.txt'
#The google sheet name
SHEET_NAME = 'fb_comments'
#the work tab of the google sheet
SHEET_TAB_IDX = 1


def get_site_dict(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser') 
    info = soup.findAll('script',attrs={'type':"application/ld+json"})[0].text.strip()
    jsonDict = json.loads(info) 
    return jsonDict


def print_usage():
    print("Usage: python ynet_parser.py [Ynet_URL] ")
    print("Example: python ynet_parser.py 'https://www.ynet.co.il/news/article/hjfpb7j116' ")


def parse_data(ynet_json):
    cols = ['headline','articleBody','keywords']
    date = ynet_json['dateModified'].split('T')[0].replace('-','.')
    date = date.split('.') 
    date = date[2] + '.' + date[1] + '.' + date[0]
    author = ynet_json['author']['name']
    image = ','.join(ynet_json['image'])
    video = ','.join(ynet_json['video'])

    data = [date, author] + [ynet_json[i] for i in cols] + [ image, video]
    output = pd.Series(data = data, index = ['date', 'author']+ cols + ['image', 'video'])
    print(output)
    return output




if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments.")
        print_usage()
        sys.exit(1)

    address = sys.argv[ADDRESS_IDX]

    if 'ynet' not in address.lower():
        print(f"The input should be a ynet article address")
        exit(1)
        
    if url_exist(address,URL_FILE):
        print(f"url '{address}' already parsed.")
        exit(1)
    try:
        ynet_dict = get_site_dict(address)
        if ynet_dict['isAccessibleForFree']  != 'True':
            print(f"No free access to the article")
            exit(1)
        parsed = parse_data(ynet_dict)

        update_sheet_row(data_list =  parsed.tolist(),
                        sheet_name=SHEET_NAME,
                        work_sheet=SHEET_TAB_IDX,
                        col_names=parsed.index.tolist())
        add_urls_to_archive([address], URL_FILE)
        print(f"Data from Ynet has been successfully added to the Google Sheet '{SHEET_NAME}'.")

    except Exception as e:
        print(f"Error: An error occurred. {str(e)}")
