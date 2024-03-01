"""
This file is dumping the IANA root zone and sorting it in the database
Link to IANA website : https://www.internic.net/domain/root.zone
"""
import json
import urllib.request
from tldtester.models import TLD, RootZone
from django.core.exceptions import MultipleObjectsReturned


def zonedownloader():
    """
    Downloads the root zone (as to not put constraint on the DNSses and resolve locally). Returns the zonefile in lines.
    returns None if not working.
    """
    url = urllib.request.urlopen("https://www.internic.net/domain/root.zone")
    if url.getcode() == 200:
        raw = url.read()
        raw = raw.decode("utf-8")
    else:
        raw = None
    return raw


def tlddownloader():
    """
    Downloads the TLD data. Returns None if not working, returns a list of TLD's if working. Returns None if not working
    """
    url = urllib.request.urlopen("https://data.iana.org/TLD/tlds-alpha-by-domain.txt")
    if url.getcode() == 200:
        raw = url.read()
        raw = raw.decode("utf-8").splitlines()
        # File has a timestamp as first line. This will take it out so we only keep the TLD's
        raw.pop(0)
        for i in range(len(raw)):
            raw[i] = raw[i].lower()
    else:
        raw = None
    return raw


def zonesorter(zonefile):
    """
    Takes the zonefile as an input and writes the records to the database
    """
    for line in zonefile:
        value = ""
        record = line.split()
        if len(record) >= 5:
            name = record[0]
            recordtype = record[3]
            if len(record) == 5:
                value = record[4]
            else:
                for i in range(len(record) - 4):
                    value = value + record[i + 4] + " "
        towrite = {"name": name, "type": recordtype, "value": value}
        zonedbwriter(towrite)


def zonedbwriter(recs):
    """
    Writes the Zone File to database
    """
    db = RootZone()
    db.name = recs["name"]
    db.rectype = recs["type"]
    db.value = recs["value"]
    db.save()


def tlddbwriter(recs):
    """
    Writes the dictionnary values in the database
    """
    if TLD.objects.filter(tld=recs["tld"]).exists():
        db = TLD.objects.get(tld=recs["tld"])
    else:
        db = TLD()
        db.tld = recs["tld"]
    db.unicodetld = recs["unicodeTld"]
    db.nsamount = recs["nsserveramount"]
    db.v4nsamount = recs["v4resolvers"]
    db.v6nsamount = recs["v6resolvers"]
    db.dnssec = recs["algo"]
    db.amountofkeys = recs["amountofkeys"]
    db.organisation = recs["organisation"]
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
        amountofkeys = 0
        nses = RootZone.objects.all().filter(name=tld + ".", rectype="NS")
        for ns in nses:
            nsservers.append(ns.value)
        for Arecord in nsservers:
            try:
                RootZone.objects.all().get(name=Arecord, rectype="A")
                Arecords += 1
            except MultipleObjectsReturned:
                Arecords += 1
                print("Multiple IPv4 for " + Arecord)
            except:
                print(Arecord + " Has no IPv4 record")
        for AAAArecord in nsservers:
            try:
                RootZone.objects.all().get(name=AAAArecord, rectype="AAAA")
                AAAArecords += 1
            except MultipleObjectsReturned:
                AAAArecords += 1
                print("Multiple IPv6 for" + AAAArecord)
            except:
                print(AAAArecord + " Has no IPv6 record")

        dsrec = RootZone.objects.all().filter(name=tld + ".", rectype="DS")
        if len(dsrec) == 0:
            # Means No DNSSEC
            algo = 400
        else:
            try:
                for ds in dsrec:
                    dnsseckeys.append(int(ds.value.split()[1]))
                    amountofkeys += 1
                algo = max(dnsseckeys)
            except Exception as e:
                print(tld + " DNSSEC " + e)
                algo = 300
        # Who registers the thing and get unicode
        rdap = urllib.request.urlopen("https://root.rdap.org/domain/" + tld)
        if rdap.getcode() == 200:
            raw = rdap.read()
            raw = raw.decode("utf-8")
            data = json.loads(raw)
            try:
                if "xn--" in tld:
                    unicodetld = data["unicodeName"]
                else:
                    unicodetld = tld
            except Exception as e:
                unicodetld = tld
                print(tld)
                print(e)
            for entity in data["entities"]:
                try:
                    organisation = entity["vcardArray"][1][2][3]
                except:
                    organisation = "Reserved"

        results = {"tld": tld, "unicodeTld": unicodetld, "nsserveramount": int(len((nsservers))),
                   "organisation": organisation, "v4resolvers": Arecords, "v6resolvers": AAAArecords, "algo": algo,
                   "amountofkeys": amountofkeys}
        tlddbwriter(results)


def main():
    try:
        zonefile = zonedownloader().splitlines(True)
        if zonefile is not None:
            # First delete the entire zone database if file polling is successful and re write
            RootZone.objects.all().delete()
            zonesorter(zonefile)
        tlds = tlddownloader()
        if tlds is not None:
            grabber(tlds)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
