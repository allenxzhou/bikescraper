# UI Prompt for Bike Scrapy

import re
import requests
import sys

class BikeScrapy:

    def __init__(self, brand='Trek', size='52', shifters='Ultegra'):
        self.brand = brand
        self.size = size
        self.shifters = shifters


if __name__ == "__main__":
    print "Press CTRL+C at any time to exit."
    while True:
        try:
            print "*Currently customized primarily for road bikes"
            brand = raw_input('BRAND:\n')
            size = raw_input('FRAME SIZE:\n')
            shifters = raw_input('SHIFTERS:\n')
            print "Generating URLs..."
        except KeyboardInterrupt:
            sys.exit()
