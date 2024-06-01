import requests
import config


def webrequest():
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
                "af": 6,
                "resolve_on_probe": True,
                "description": "DNS measurement for be",
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
                "query_argument": "be"
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

    print(response.status_code)
    print(response.json())
    print("https://atlas.ripe.net/measurementdetail/")

def dbwriter(response):
    print(response)

def main():
    dbwriter(webrequest())