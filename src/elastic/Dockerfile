FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

RUN apt-get update && apt-get install --no-install-recommends --yes python3 python3-pip python3-setuptools

WORKDIR /coderun
COPY 00_MAINSCRAPER.py /coderun
COPY requirements.txt /coderun
COPY keywords.txt /coderun

RUN pip3 install -trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python", "00_MAINSCRAPER.py"]
