FROM python:3

RUN pip install boto3 requests

ADD ddns-docker.py /

CMD [ "python3", "./ddns-docker.py" ]
