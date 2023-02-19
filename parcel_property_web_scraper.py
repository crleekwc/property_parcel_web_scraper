'''/////////////////////////////////////////

Purpose: Scrape parcel data off Hawaii Real Estate site

Language: python3
Required module(s):
Beautiful Soup 4 - pip3 install beautifulsoup4


Date: 5-29-2017
updated: 2-19-23
Written by: Christopher Lee

/////////////////////////////////////////'''

from bs4 import BeautifulSoup
import urllib
import pandas as pd


def get_response_data(url: str) -> bytes:
    req = urllib.request.Request(url)
    req.add_header('User-Agent',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.97 Safari/537.36 Vivaldi/1.9.818.49')
    resp = urllib.request.urlopen(req)
    resp_data = resp.read()
    return resp_data

def remove_rows_with_totals(dataframe):
    dataframe = dataframe[~dataframe.isin(['Totals:']).any(axis=1)].to_string()
    return dataframe

def scrape_table_data(resp_data: bytes) -> None:
    soup = BeautifulSoup(resp_data, features="html5lib")
    tables = soup.find_all('table')
    parcel_id = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)['KeyValue'][0]
    for table in tables:
        dataframes = pd.read_html(str(table), header=0)
        for dataframe in dataframes:
            if not dataframe.empty:
                if len(dataframe.columns) == 2:
                    dataframe = dataframe.transpose().reset_index()
                    header_row = dataframe.iloc[0]
                    dataframe.rename(columns=header_row, inplace = True)
                    dataframe = dataframe.iloc[1:].reset_index(drop = True)
                    dataframe['Parcel Number'] = parcel_id
                else:
                    dataframe['Parcel Number'] = parcel_id
                
                dataframe = remove_rows_with_totals(dataframe)
                print(dataframe + '\n')


def main():
    scrape_table_data(get_response_data(url))


if __name__ == "__main__":
    url = 'https://qpublic.schneidercorp.com/Application.aspx?AppID=1048&LayerID=23618&PageTypeID=4&PageID=9878&Q=1949324841&KeyValue=230210430000'
    main()
