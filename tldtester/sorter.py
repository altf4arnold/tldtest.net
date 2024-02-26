"""
This file is dumping the IANA root zone and sorting it in the database
Link to IANA website : https://www.internic.net/domain/root.zone
"""
import urllib.request
from tldtester.models import TLD
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


def dbwriter(recs):
    """
    Writes the dictionnary values in the database
    """
    if TLD.objects.filter(tld=recs["tld"]).exists():
        db = TLD.objects.get(tld=recs["tld"])
    else:
        db = TLD()
        db.tld = recs["tld"]
    db.nsamount = recs["nsserveramount"]
    db.v4nsamount = recs["v4resolvers"]
    db.v6nsamount = recs["v6resolvers"]
    db.dnssec = recs["algo"]
    db.save()


def grabber(data):
    """
    This function takes the TLD's and makes querrys to the DNS. It looks up how many authoritative DNS's there are and
    analyses the v4, v6 and DNSSEC. Returns a list of dictionaries with all the vallues to write in the database
    """
    for tld in data:
        nsservers = []
        dnsseckeys = []
        Arecords = 0
        AAAArecords = 0
        try:
            ns = dns.resolver.resolve(tld, 'NS')
            for server in ns:
                nsservers.append(server.to_text())
        except Exception as e:
            print(e)
        for Arecord in nsservers:
            try:
                try:
                    dns.resolver.resolve(Arecord, 'A')
                except Exception as e:
                    # retry
                    print(e)
                    dns.resolver.resolve(Arecord, 'A')
                Arecords += 1
            except Exception as e:
                print(e)
        for AAAArecord in nsservers:
            try:
                try:
                    dns.resolver.resolve(AAAArecord, 'AAAA')
                except Exception as e:
                    # retry
                    print(e)
                    dns.resolver.resolve(AAAArecord, 'AAAA')
                AAAArecords += 1
            except Exception as e:
                print(e)
        try:
            try:
                ds = dns.resolver.resolve(tld, 'DS')
            except Exception as e:
                # retry
                print(e)
                ds = dns.resolver.resolve(tld, 'DS')
            for dsrecord in ds:
                algo = dsrecord.to_text()
                line = algo.split()
                dnsseckeys.append(int(line[1]))
            algo = max(list(dict.fromkeys(dnsseckeys)))
        except Exception as e:
            algo = 400
            print(e)

        results = {"tld": tld, "nsserveramount": int(len((nsservers))), "v4resolvers": Arecords,
                   "v6resolvers": AAAArecords, "algo": algo}
        dbwriter(results)


def main():
    try:
        grabber(downloader())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
