import requests
import json

PINATA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJlYmNkOWE0Ny04MTFiLTQ0OGMtOWVmMi0yY2MwMWQ1OTBkM2IiLCJlbWFpbCI6ImtlbHZpbmxAZW5naW5lZXJpbmcudXBlbm4uZWR1IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiRlJBMSJ9LHsiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiTllDMSJ9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6ImRiYjAwN2RlMDUwZTk5YjczNTVmIiwic2NvcGVkS2V5U2VjcmV0IjoiNzJkYTQ2MTYwNzgwNzUwYWM1ODk1Zjc4NGNiZTVlMWM1NmRmMWEzMTM4M2VjYTc2NjdlZjRmNTU1OWQxZTk0ZSIsImV4cCI6MTgyNDE3MTg1MH0.XGTSt6Y_8Xi17BV63-rXchl9ayqflLnOtN7xGlIbelM"

GATEWAYS = [
	"https://ipfs.io/ipfs/",
	"https://dweb.link/ipfs/",
	"https://gateway.pinata.cloud/ipfs/",
]

def pin_to_ipfs(data):
    assert isinstance(data, dict), f"Error pin_to_ipfs expects a dictionary"
 
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "Authorization": f"Bearer {PINATA_JWT}",
        "Content-Type": "application/json",
    }
    payload = {"pinataContent": data}
 
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
 
    cid = response.json()["IpfsHash"]
    return cid

def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), f"get_from_ipfs accepts a cid in the form of a string"
 
    # Tolerate "ipfs://" prefixes, stray spaces, and extra slashes
    cid = cid.strip().replace("ipfs://", "").strip("/")
 
    data = None
    last_error = None
    for gateway in GATEWAYS:
        try:
            response = requests.get(gateway + cid, timeout=20)
            response.raise_for_status()
            data = response.json()
            break
        except Exception as e:
            last_error = e
 
    if data is None:
        raise Exception(f"Could not fetch {cid} from any gateway. Last error: {last_error}")
 
    assert isinstance(data, dict), f"get_from_ipfs should return a dict"
    return data
