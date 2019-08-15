# simple_ddns_agent

## Purpose
Create a stable DNS record via AWS Route53 for a dynamic IP endpoint

Written for homelabs that don't want to pay for a static IP.

## Prerequisites / Preparing AWS and credentials

You will need a Route53 hosted zone if you don't already have one. You will need to know your hosted zone's ID, and you should have a DNS name in mind like "lab.mysite.com." (Be sure to include the final '.')

Create an IAM policy in AWS with the minimum necessary access:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
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

Create an IAM user and attach the policy created above. Generate access key/secret for this account.

[install awscli on your host](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
```
pip3 install awscli
```

[Configure awscli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration)
```
aws configure
```

## Running
### As a cron job every 15m:
```
0,15,30,45 * * * * python3 /path/to/repo/ddns-cron.py
```

### Via Docker Hub
```
docker pull nickgoeben/simple_ddns_agent

docker run -d --restart=unless-stopped -v $HOME/.aws:/root/.aws -e HOSTED_ZONE_ID="YOURHOSTEDZONEID" -e TARGET_RECORD_NAME="YOURLAB.YOURSITE.com." -e TTL="300" -e INTERVAL_MINS="20" --name ddns nickgoeben/simple_ddns_agent
```
