FROM marketplace.gcr.io/google/debian10:latest
RUN apt-get update && apt-get install --no-install-recommends --yes python3 python3-pip python3-setuptools
WORKDIR /coderun
COPY 00_MAINSCRAPER.py /coderun
COPY requirements.txt /coderun
RUN pip3 install -r requirements.txt