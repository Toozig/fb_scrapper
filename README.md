# Facebook Post to Google Sheet Exporter

This script allows you to extract data from a Facebook post and export it to a Google Sheet using the Facebook Scraper and Gspread libraries.

## Requirements

- Python 3.7+
- [Facebook Scraper](https://github.com/kevinzg/facebook-scraper)
- [Gspread](https://github.com/burnash/gspread)
- Google Sheets and Drive APIs enabled
- Google Sheets API credentials (client_secrets.json)

## Installation

1. Install the required Python libraries using pip:

   ```
   pip install pandas facebook-scraper gspread
   ```

2. Enable Google Sheets and Drive APIs and create API credentials. You can follow the [official Google Sheets API documentation](https://developers.google.com/sheets/api/quickstart) for instructions on how to set up the API and obtain the `client_secrets.json` file.

## Usage

To run the script, use the following command:

```bash
python fb_parser.py [Facebook_Post_URL]
```

- `Facebook_Post_URL`: The URL of the Facebook post you want to extract data from.

### Example

```bash
python fb_parser.py https://facebook.com/post/12345
```

This command will extract data from the specified Facebook post and add it to the Google Sheet defined in the global variables (`URL_FILE`, `SHEET_NAME`, and `SHEET_TAB_IDX`).

## Note

- Make sure to enable the Google Sheets and Drive APIs and create the necessary credentials (`client_secrets.json`) as mentioned in the Requirements section.
- The script provides basic error handling for ease of use and troubleshooting. If any issues occur during execution, an error message will be displayed.
- The URLs parsed will be saved in a file named `url_archive.txt`.

## Configuration

In the script, you can configure the following global variables:

- `URL_FILE`: The file containing parsed URLs. It will be created if it doesn't exist.
- `SHEET_NAME`: The name of the Google Sheet where you want to store the data.
- `SHEET_TAB_IDX`: The index of the worksheet tab within the Google Sheet.
