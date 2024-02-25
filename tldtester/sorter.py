"""
This file is dumping the IANA root zone and sorting it in the database
Link to IANA website : https://www.internic.net/domain/root.zone
"""
import urllib.request
import json
# from tldtester.models import zonecontent, TLD
import dns.resolver


def downloader():
    """
    Downloads the data. Returns None if not working, returns a list of TLD's if working
    """
    url = urllib.request.urlopen("https://data.iana.org/TLD/tlds-alpha-by-domain.txt")
    if url.getcode() == 200:
        raw = url.read()
        raw = raw.decode("utf-8").splitlines()
        # File has a timestamp as first line. This will take it out so we only keep the TLD's
        raw.pop(0)
    else:
        raw = None
    return raw


def main():
    try:
        data = sorter(downloader())
        dbwriter(data)
        print(data)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
