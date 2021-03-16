import logging
import os
from queue import Queue
from threading import Thread
from time import time
import csv
import DataScraperKibana

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url, ip = self.queue.get()
            try:
                DataScraperKibana.searchKibana(url, ip)
            finally:
                self.queue.task_done()


def main():
    ts = time()
    queue = Queue()
    for x in range(100):
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()
    with open('data/Kibana.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            url = "http://" + row['IP'] + ':' + row['Port'] + "/api/console/proxy?path=_cat/indices&method=GET"
            ip = row['IP'] + ':' + row['Port']
            #logger.info('Queueing {}'.format(url))
            queue.put((url, ip))
    queue.join()
    logging.info('Took %s', time() - ts)


if __name__ == '__main__':
    main()