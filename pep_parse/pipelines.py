import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
FILE_NAME = 'status_summary_{time}.csv'


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_count = defaultdict(int)
        self.status_dir = BASE_DIR / 'results'
        self.status_dir.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        status_value = item['status']
        self.status_count[status_value] += 1
        return item

    def close_spider(self, spider):
        time = str(datetime.now().strftime(DATETIME_FORMAT))
        filename = self.status_dir / FILE_NAME.format(time=time)
        results = list(self.status_count.items())
        total = sum(self.status_count.values())

        with open(filename, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])
            writer.writerows(results)
            writer.writerow(['Total', total])
