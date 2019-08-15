#!/usr/bin/env python3

import boto3
import socket
import os
from requests import get
from time import sleep

# TODO: Proper logging

# Get config from environment variables:
hosted_zone_id = os.environ["HOSTED_ZONE_ID"]
target_record_name = os.environ["TARGET_RECORD_NAME"]  # your.site.com.
ttl = int(os.environ["TTL"])
interval_mins = int(os.environ["INTERVAL_MINS"])
    
client = boto3.client('route53')

while True:
    dns_ip = socket.gethostbyname(target_record_name[:-1])
    current_ip = get('https://api.ipify.org').text
    
    # Log
    print("DNS IP: " + dns_ip)
    print("Current IP: " + current_ip)

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
    else:
        print("IP is current, no changes made")
              
    sleep(60 * interval_mins)
