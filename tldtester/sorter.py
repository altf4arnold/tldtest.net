"""
This file is dumping the IANA root zone and sorting it in the database
Link to IANA website : https://www.internic.net/domain/root.zone
"""
import urllib.request
import zonefile_parser
from tldtester.models import zonecontent


def downloader():
    """
    Downloads the data. Returns None if not working, Returns data if working
    """
    url = urllib.request.urlopen("https://www.internic.net/domain/root.zone")
    if url.getcode() == 200:
        raw = url.read()
        raw = raw.decode("utf-8")
    else:
        raw = None
    return raw


def sorter(rawdata):
    """
    This file removes the tabs and line breaks from rawdata
    returns as a list with dictionary in it
    """
    encodeddata = zonefile_parser.parse(rawdata)
    return encodeddata

def dbwriter(data):
    """
    Writes everything in the Zone database
    """
    for line in data:
        print(line)
        DB=zonecontent()
        DB.rtype = line["rtype"]
        DB.name = line["name"]
        DB.rclass = line["rclass"]
        DB.data = line["rdata"]
        DB.ttl = int(line["ttl"])
        DB.save()

def main():
    try:
        dbwriter(sorter(downloader()))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
