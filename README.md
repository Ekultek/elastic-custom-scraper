## 3K Toolkit 
*Tailored Data Collection for Eurasia* 

` gcloud components install docker-credential-gcr cloud-build-local beta alpha kubectl `

### Folder Structure
```
├── .gitignore
├── README.md
├── pyvenv.cfg
├── requirements.txt
├── results
│   ├── json
│   │   └── example.json
│   └── text
│       └── example.txt
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

1. Useful software, divided into different programs based on utility, is available under the `src` file.


2. `git pull` should take care of any updates most of the time. Run `git stash` if having any issues. Be aware local changes will be overwritten.


3. Remember to run `pip3 install -r requirements.txt`. If feeling special also spin up a `virtualenv`.


4. `README.md` can be found in every software folder for each utility.


5. Explanation of Utilities:
      - Dorks: useful queries for Shodan and BinaryEdge
      - Elastic: scraper for all elastic databases based on keywords
      - Elasticdump: download from a cluster selected indices as JSON
      - Kibana: [draft] kibana scraper
      - Miscprojects: [draft] 
      - Scrapy: [draft] advanced web/spider crawler 
      - Social: [draft] Instagram and Twitter scraping / analysis tools