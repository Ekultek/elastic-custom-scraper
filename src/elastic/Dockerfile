
FROM Python:3.8
ENV name John Dow
WORKDIR /coderun
COPY 00_MAINSCRAPER.py /coderun
COPY requirements.txt /coderun
RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/bash", "-c", "echo Hello, $name"]

