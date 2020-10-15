# A truly simple DDNS agent

- An alternative for homelabs that don't want to pay for a static IP or DDNS providers.
- Runs out of the box via python and docker. For helm charts pass your aws secrets as environment variables.
- Verified up to date: Sept 2020


## Prepare an AWS secret with limited privileges

You will need an AWS Route53 domain and hosted zone if you don't already have one. These are around $10/year

Create an IAM policy in AWS with the minimum necessary access to your DNS zone:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "route53:ChangeResourceRecordSets",
                "route53:ListResourceRecordSets"
            ],
            "Resource": "arn:aws:route53:::hostedzone/YOUR__HOSTED_ZONE_ID"
        }
    ]
}
```

Create an IAM user and attach the policy created above. Generate an access key and secret for this account.

[install awscli on your host](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
```
pip3 install awscli
```

[Configure awscli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration) on your local host or server
```
aws configure
```

## Deploy to your homelab
### As a python process:
```
export HOSTED_ZONE_ID="YOURHOSTEDZONEID"
export TARGET_RECORD_NAME="YOURLAB.YOURSITE.com."
python3 ddns.py
```

### Via [Docker Hub](https://hub.docker.com/repository/docker/nickgoeben/simple_ddns_agent)
```
docker run -d --restart=unless-stopped \
-v $HOME/.aws:/root/.aws \
-e HOSTED_ZONE_ID="YOURHOSTEDZONEID" \
-e TARGET_RECORD_NAME="YOURLAB.YOURSITE.com." \
--name ddns nickgoeben/simple_ddns_agent
```

Optional args:
```
-e TTL="300" 
-e INTERVAL_MINS="20"
```
