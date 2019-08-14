#!/usr/bin/env python3

import boto3
import socket
import os
from requests import get
from time import sleep

# TODO: Proper logging

# Get environment variables:
hosted_zone_id = os.environ["HOSTED_ZONE_ID"]
target_record = os.environ["TARGET_RECORD"]
ttl = int(os.environ["TTL"])
    
client = boto3.client('route53')

while True:
    dns_ip = socket.gethostbyname('vpn.nickgoeben.com')
    current_ip = get('https://api.ipify.org').text
    
    # Log
    print("DNS IP: " + dns_ip)
    print("Current IP: " + current_ip)

    if dns_ip != current_ip:
        response = client.change_resource_record_sets(
        HostedZoneId='Z1ZWJJNHMY2MAJ',
        ChangeBatch={'Comment': 'Updating VPN Record',
                     'Changes': [
                         {
                             'Action': 'UPSERT',
                             'ResourceRecordSet': {
                                 'Name': 'vpn.nickgoeben.com.',
                                 'Type': 'A',
                                 'TTL': 30,
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
    
    sleep_interval = 15  # In Minutes
    sleep(60 * sleep_interval)
