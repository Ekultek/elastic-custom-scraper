# 3K Toolkit 

### Tailored Data Collection for Eurasia 
```
3K Toolkit
├── .gitignore
├── README.md
├── pyvenv.cfg
├── requirements.txt
├── results
│   ├── json
│   │   ├── unicodetest002.json
│   │   ├── unicodetest003.json
│   │   ├── unicodetest004.json
│   │   └── unicodetest01.json
│   └── text
│       └── xiaomi.txt
└── src
    ├── dorks
    │   ├── BINARYEDGE.md
    │   └── SHODAN.md
    ├── elastic
    │   ├── 00_MAINSCRAPER.py
    │   ├── README.md
    │   └── keywords.txt
    ├── elasticdump
    │   ├── README.md
    │   ├── download_indices.sh
    │   └── index_names.txt
    ├── kibana
    │   ├── DataScraperKibana.py
    │   ├── DataSearchKibana.py
    │   └── README.md
    ├── miscprojects
    │   ├── crawler.py
    │   ├── requester.py
    │   └── shodan-utils.py
    └── scrapy
        ├── scraper
        │   ├── __init__.py
        │   ├── items.py
        │   ├── middlewares.py
        │   ├── pipelines.py
        │   ├── settings.py
        │   └── spiders
        │       ├── __init__.py
        │       └── bgpview.py
        └── scrapy.cfg
```

2. Run script every 8 hours on BinaryEdge.

3. All JSON should be uploaded to a Google Cloud bucket after completion. Consider splitting into 10 MB chunks each.

4. Work in parellism?
