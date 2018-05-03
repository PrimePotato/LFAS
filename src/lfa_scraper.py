import yaml
import re


class LfaScraper(object):
    def __init__(self, file_location, scraper='Initial', cfg_location='cfg/scraper_config.yaml'):
        self.scraper = scraper
        self.file_location = file_location
        self.cfg_location = cfg_location

        with open(file_location, 'rb') as f:
            self.raw_txt = f.read().decode('ascii', errors='ignore')

        with open(cfg_location) as stream:
            self.cfg = yaml.load(stream)
            self.scraper_cfg = self.cfg[scraper]
            self.matches = {k: re.search(vals['regex'], self.raw_txt, re.DOTALL) for k, vals in
                            self.scraper_cfg['Variables'].items()}
        self.key_data = {k: v for k, v in self.matches.items()}

    def get_value(self, key):
        return self.matches[key].group(1)
