FROM python:3

ADD ddns-docker.py /

RUN pip install boto3

CMD [ "python3", "./ddns-docker.py" ]
