#!/usr/bin/env python3
import boto3
import socket
from requests import get

# ---------- CONFIG:
hosted_zone_id = "1234567890"
target_record_name = "your.site.com."
ttl = 300
# ----------

# Get the current value of the dns record:
dns_ip = socket.gethostbyname(target_record_name[:-1])
print("DNS IP: " + dns_ip)

# Get the current IP of the box running this script:
current_ip = get('https://api.ipify.org').text
print("Current IP: " + current_ip)

client = boto3.client('route53')

if dns_ip != current_ip:
    response = client.change_resource_record_sets(
    HostedZoneId = hosted_zone_id,
    ChangeBatch = {'Comment': 'Updating VPN Record',
                 'Changes': [
                     {
                         'Action': 'UPSERT',
                         'ResourceRecordSet': {
                             'Name': target_record_name,
                             'Type': 'A',
                             'TTL': ttl,
                             'ResourceRecords': [
                                 {
                                     'Value': current_ip
                                 },
                             ],
                         }
                     },
                 ]
                 }
    )

print(response)
