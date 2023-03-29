import re
from typing import Dict

import requests
from bs4 import BeautifulSoup

_host = 'https://maclookup.app'


def download_file() -> Dict[str, str]:
    response = requests.get(_host + '/downloads/json-database')
    if not response.ok:
        raise Exception('Failed to load the source page to find the link for file downloading')

    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find('a', attrs={'href': re.compile(r'^/downloads/json-database/get-db.+$', flags=re.DOTALL)})
    if not tag or 'href' not in tag.attrs:
        raise Exception('Failed to find the link to download the file')

    response = requests.get(_host + tag.attrs.get('href'))
    if not response.ok:
        raise Exception('Failed to download the file')

    return extract_values(response.json())


# Use with import in the beginning of the file: `from datetime import datetime, timedelta`
# def filter_by_updates_in_last_days(content, days: int = 3):
#     date_from = datetime.today().date() + timedelta(days=-days)
#     return filter(
#         lambda line: datetime.strptime(line['lastUpdate'], '%Y/%m/%d').date() > date_from,
#         content
#     )


def extract_values(content) -> Dict[str, str]:
    return dict(map(lambda line: (line['macPrefix'], line['vendorName']), content))
