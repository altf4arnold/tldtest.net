import requests
import config
from tldtester.models import TLD
from .models import Atlas


def webrequest(tld, stack):
    description_string = ("DNS measurement for ." + tld + " in IPv" + str(stack))
    url = "https://atlas.ripe.net/api/v2/measurements/"
    api_key = config.ATLAS_API
    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "definitions": [
            {
                "type": "dns",
                "af": stack,
                "resolve_on_probe": True,
                "description": description_string,
                "query_class": "IN",
                "query_type": "SOA",
                "use_macros": False,
                "protocol": "UDP",
                "udp_payload_size": 512,
                "retry": 0,
                "skip_dns_check": False,
                "include_qbuf": False,
                "include_abuf": True,
                "prepend_probe_id": False,
                "set_rd_bit": True,
                "set_do_bit": False,
                "set_cd_bit": False,
                "timeout": 5000,
                "use_probe_resolver": True,
                "set_nsid_bit": True,
                "query_argument": tld
            }
        ],
        "probes": [
            {
                "type": "msm",
                "value": 69775666,
                "requested": 624
            }
        ],
        "is_oneoff": True,
        "bill_to": config.BILLING_RIPE
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        data = (response.json())
        measurement = data['measurements'][0]
    else:
        measurement = None
    dbwriter(tld, stack, measurement)


def dbwriter(intld, stack, measurement):
    tld = Atlas.objects.filter(tld=intld)
    tldstack = tld.filter(stack=stack)
    if tldstack.exists():
        primary_key = tldstack.values_list('pk', flat=True).first()
        db = Atlas.objects.get(pk=primary_key)
    else:
        db = Atlas()
        db.tld = tld
        db.stack = stack
    if measurement is not None:
        db.measurement = measurement
    db.save()
    tld = TLD.objects.filter(tld=intld)
    if tld.exists():
        primary_key = tld.values_list('pk', flat=True).first()
        db = TLD.objects.get(pk=primary_key)
        if measurement is not None:
            if stack == 4:
                db.atlasv4 = measurement
                db.save()
            elif stack == 6:
                db.atlasv6 = measurement
                db.save()
            else:
                print("Unknown IP version")


def main():
    unicodetlds = []
    # This will get the TLD's in unicode format from the database and put them in the list
    tlds = TLD.objects.all().order_by('tld')
    for tld in tlds:
        db = TLD.objects.get(tld=tld)
        tlds.append(db.tld)
    for tld in tlds:
        db = TLD.objects.get(tld=tld)
        if db.atlasv4 is None:
            webrequest(tld, 4)
        if db.atlasv6 is None:
            webrequest(tld, 6)


if __name__ == "__main__":
    main()
