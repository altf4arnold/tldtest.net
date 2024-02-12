"""
This file is dumping the IANA root zone and sorting it in the database
Link to IANA website : https://www.internic.net/domain/root.zone
"""
import urllib.request


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
    print(str(rawdata))


def main():
    try:
        sorter(downloader())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
