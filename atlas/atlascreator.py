import requests
import config
from tldtester.models import TLD
from .models import Atlas


def webrequest(tld, stack):
    description_string = ("DNS measurement for " + tld + " in IPv" + str(stack))
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

def dbwriter(unicodetld, stack, measurement):
    tld = Atlas.objects.filter(unicodetld=unicodetld)
    tldstack = tld.filter(stack=stack)
    if tldstack.exists():
        primary_key = tldstack.values_list('pk', flat=True).first()
        db = Atlas.objects.get(pk=primary_key)
    else:
        db = Atlas()
        db.unicodetld = unicodetld
        db.stack = stack
    db.measurement = measurement
    db.save()


def main():
    unicodetlds = []
    # This will get the TLD's in unicode format from the database and put them in the list
    tlds = TLD.objects.all().order_by('tld')
    for tld in tlds:
        db = TLD.objects.get(tld=tld)
        unicodetlds.append(db.unicodetld)
    for tld in unicodetlds:
        webrequest(tld, 4)
        webrequest(tld, 6)

if __name__ == "__main__":
    main()