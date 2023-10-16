import subprocess
import pandas as pd
import gspread


#file which contains the parsed ur;s
URL_FILE = 'url_archive.txt'
#The google sheet name
SHEET_NAME = 'fb_comments'
#the work tab of the google sheet
SHEET_TAB_IDX = 0

#post google sheet
POSTS_SHEET = "https://docs.google.com/spreadsheets/d/1JrIFDIbEo-Y7sZzch0O9HbHzUNi0m_jlr-xR5WFHitU/edit?usp=sharing"
# url col index in the posts_sheet
URL_COL = 2

def filter_sites(sites_series):
    # drop non facebook address
    f_sites = sites_series[sites_series.str.lower().str.contains('facebook')]

    #drop parsed linked
    archive = pd.read_csv(URL_FILE, header=None)
    f_sites = f_sites[~sites_series.isin(archive[0].tolist())]
    return f_sites


def parse_urls(url_list):

    for url in url_list:
        subprocess.call(['python', 'fb_parser.py', url])

if __name__ == '__main__':
    gc = gspread.oauth()    
    sh = gc.open_by_url(POSTS_SHEET)
    sheet = sh.get_worksheet(SHEET_TAB_IDX)

    sites  = pd.Series(sheet.col_values(URL_COL))

    new_sites = filter_sites(sites)
    print(f"adding new {new_sites.shape} posts")
    parse_urls(new_sites)
    print('done')