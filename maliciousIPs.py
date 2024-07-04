import requests
import json

def update_suricata_rules(malicious_ips):
    with open('/var/lib/suricata/rules/block_ips.rules', 'a') as rule_file:
        sid = 100001
        for ip in malicious_ips:
            rule_file.write(f'drop ip {ip} any -> any any (msg:"Blocked malicious IP {ip}"; sid: {sid}; rev:1;)\n')
            sid += 1


if __name__ == "__main__":
    malicious_ips = []
    api_key = '<Your API key>'
    url = 'https://api.abuseipdb.com/api/v2/blacklist'

    headers = {
        'Key': api_key,
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            malicious_ips = [entry['ipAddress'] for entry in data['data']]
            print(f"Fetched {len(malicious_ips)} malicious IPs from AbuseIPDB.")
        else:
            print(f"Failed to fetch IPs. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching IPs: {str(e)}")
   
    update_suricata_rules(malicious_ips)
