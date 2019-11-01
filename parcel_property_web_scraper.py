'''/////////////////////////////////////////

Purpose: Scrape parcel data off Hawaii Real Estate site

Language: python3.6
Required module(s):
Beautiful Soup 4 - pip3.6 install beautifulsoup4
Requests - pip3.6 install requests


Date: 5-29-2017
Written by: Christopher Lee

/////////////////////////////////////////'''

from bs4 import BeautifulSoup
import requests
import urllib
import datetime
from datetime import timedelta
import openpyxl
import re
import pandas as pd

try:
    url = 'http://qpublic9.qpublic.net/hi_honolulu_display.php?KEY=940440610000&' + 'show_history=1&' + '#hist_taxes'
            #url is updated with the current month and year
    # while True:
    req = urllib.request.Request(url)
        #handles request

    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.97 Safari/537.36 Vivaldi/1.9.818.49')
        #adds User-Agent header

    resp = urllib.request.urlopen(req)
        #prints header from response
    respData = resp.read()
        #handles the response back from server

    soup = BeautifulSoup(respData, features="html5lib")
    body = soup.body

    links = soup.find_all('a')
    tables = soup.find_all('table')

    for link in links:
        x = str(link.contents)
        if x == '[\' Next Parcel \']':
            url = link.get('href') + 'show_history=1&' + '#hist_taxes'
            print(url)

    for table in tables[2:14]:
        header = table.findAll(attrs={'class': re.compile(r".*\btable_header\b.*")})
        if len(header) > 0:
            print(header[0].find(text=True).strip())
        df = pd.read_html(str(table), header=1)
        for dataframe in df:
            if not dataframe.empty:
                print(dataframe.to_string())
        print('\n\n')

    if len(url) <= 6:
        print(url)


except Exception as e:
    print(str(e))
        #prints error status codes
